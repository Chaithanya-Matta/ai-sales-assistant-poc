from langgraph.types import Command
from state.state import State, Message
from typing import Literal
from config.model_config import llm
from prompts_library import address_prompt
from typing import Optional, List
from config.vector_store_config import vectorstore
from config.postgres_config import POSTGRES_ENGINE
from sqlalchemy import text
import json
from models.address import ParsedAddress, RetrievedAddress, RetrievedAddressScore
import logging

logger = logging.getLogger(__name__)


MAX_RETRIEVAL_ATTEMPTS = 2


def parse_user_address(query: str) -> ParsedAddress:
    messages = [
        address_prompt.PARSE_ADDRESS_SYSTEM_PROMPT,
        {"role": "user", "content": query}
    ]
    parser = llm.with_structured_output(ParsedAddress)
    return parser.invoke(messages)

def fetch_full_addresses_by_ids(ids: List[str]) -> List[RetrievedAddress]:
    if not ids:
        return []
    id_tuple = tuple(ids)
    query = text(f"""
        SELECT id, address1, address2, city, state, zip
        FROM addresses
        WHERE id IN :id_tuple
    """)
    with POSTGRES_ENGINE.connect() as conn:
        result = conn.execute(query, {"id_tuple": id_tuple})
        return [RetrievedAddress(**dict(row._mapping)) for row in result]

def llm_match_address(parsed_address: ParsedAddress, candidates: List[RetrievedAddress]) -> Optional[RetrievedAddress]:
    """
    Uses a Large Language Model to find the best matching address from a list of candidates.
    This function constructs a detailed prompt for the LLM, including the user's parsed
    address, the list of candidates, and explicit instructions to return the single best
    match in a structured format.
    """
    parsed_json = parsed_address.model_dump_json(indent=2)
    candidates_json = json.dumps([c.model_dump() for c in candidates], indent=2)
    logger.debug("****************************Parsed json*******************************")
    logger.debug(parsed_json)
    logger.debug("****************************Retrieved json***************************")
    logger.debug(candidates_json)

    user_msg = f"""
    You are an address matching expert. Your task is to find the single best match for a user's address from a list of candidate addresses retrieved from RAG similarity search.

    **1. User's Parsed Address (from their query):**
    This is the address we are trying to find. It may be incomplete or contain typos.
    ```json
    {parsed_json}
    ```

    **2. Candidate Addresses (retrieved from our vector store via RAG):**
    Here is a list of potential matches from our system.
    ```json
    {candidates_json}
    ```

    **3. Your Task & Output Instructions:**
    - Compare the "User's Parsed Address" with each "Candidate Address".
    - Identify the three best matching candidate address from the list. A match can be approximate (e.g., "St" vs "Street").
    - Score them according to their match probability like 3, 2, 1. 3 is highest score and 1 is the lowest score. There is a "score" field that you can use

    **Schema for your JSON output (`RetrievedAddressScore`):**
    ```json
    {{
        "id": "string",
        "address1": "string",
        "address2": "string (optional, can be null)",
        "city": "string",
        "state": "string",
        "zip": "string",
        "score": "string"
    }}
    ```
    """

    messages = [
        address_prompt.LLM_ADDRESS_MATCH_SYSTEM_PROMPT,
        {"role": "user", "content": user_msg}
    ]

    # Use structured output to get a predictable, parsed response
    llm_with_parser = llm.with_structured_output(RetrievedAddressScore)
    
    try:
        match = llm_with_parser.invoke(messages)
        # An empty model_dump (excluding unset fields) means the LLM returned an empty object `{}`, indicating no match.
        if not match.model_dump(exclude_unset=True):
            return None
        return match
    except Exception:
        # If the LLM output fails to parse into the Pydantic model, treat it as no match.
        return None

# Step 4: Address agent
def address_agent(state: State) -> Command[Literal["address", "supervisor"]]:
    logger.info("Entered Address Agent")
    query = state.query
    attempts = getattr(state, "retrieval_attempts", 0)
    parsed = parse_user_address(query)

    # Step 1: Retrieve from Pinecone
    filter_dict = {}
    if parsed.city:
        filter_dict["city"] = parsed.city
    if parsed.state:
        filter_dict["state"] = parsed.state
    if parsed.zip:
        filter_dict["zip"] = parsed.zip

    retrieved = vectorstore.similarity_search(query, k=10, filter=filter_dict)
    ids = [doc.id for doc in retrieved]
    retrieved = fetch_full_addresses_by_ids(ids)
    logger.debug("Parsed input address")
    logger.debug(parsed)
    logger.debug("Retrieved addresses")
    logger.debug(retrieved)

    # Step 2: LLM match
    llm_matches = llm_match_address(parsed, retrieved)
    logger.debug("LLM matches")
    logger.debug(llm_matches)

    if llm_matches:
        state.messages.append(Message(role="address", content=f"Found address matches (LLM): {llm_matches}"))
        return Command(goto="supervisor", update={
            "address_results": [llm_matches],
            "retrieval_attempts": 0,
            "messages": state.messages,
            "next_agent": "FINISH"
        })

    # Step 3: Retry or fail
    if attempts < MAX_RETRIEVAL_ATTEMPTS - 1:
        state.messages.append(Message(role="address", content=f"No match found. Retrying (attempt {attempts+2})..."))
        return Command(goto="address", update={
            "retrieval_attempts": attempts + 1,
            "messages": state.messages
        })

    state.messages.append(Message(role="address", content="No address match found after 2 attempts."))
    return Command(goto="supervisor", update={
        "address_results": [],
        "retrieval_attempts": 0,
        "messages": state.messages,
        "next_agent": "FINISH"
    })
