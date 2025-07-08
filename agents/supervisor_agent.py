from langgraph.types import Command
from pydantic import BaseModel
from typing import Literal
from state.state import State, Message
from datetime import datetime
from prompts_library import supervisor_prompt
from config.model_config import llm
from langgraph.graph import END
import logging

from utils.message_converter import convert_state_messages_to_llm_format

logger = logging.getLogger(__name__)

class RouteDecision(BaseModel):
    next: Literal["upsell", "address", "chat", "FINISH"]

def supervisor_agent(state: State) -> Command[Literal["upsell", "address", "chat", "__end__"]]:

    logger.info("Entered Supervisor Agent")

    if state.next_agent == "FINISH":
        logger.info("✅ Received FINISH signal. Exiting...")
        return Command(goto=END, update={"messages": state.messages})

    messages = [{"role": m.role, "content": m.content} for m in state.messages]
    # messages = [supervisor_prompt.SYSTEM_PROMPT] + [{"role": m.role, "content": m.content} for m in state.messages]
    messages = [supervisor_prompt.SYSTEM_PROMPT] + convert_state_messages_to_llm_format(messages)

    router_llm = llm.with_structured_output(RouteDecision)
    result = router_llm.invoke(messages)
    
    logger.debug("*"*60)
    logger.debug(result)
    logger.debug("*"*60)
    next_agent = result.next

    state.messages.append(
        Message(role="supervisor", content=f"Routing to '{next_agent}' based on user input.")
    )

    logger.debug("Below is next agent")
    logger.debug(next_agent)

    if next_agent == "FINISH":
        next_agent = END

    return Command(
        goto=next_agent,
        update={
            "next_agent": next_agent,
            "messages": state.messages
        }
    )
