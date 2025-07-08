from langgraph.types import Command
from state.state import State, Message
from typing import Literal
import random
import json
import os
import re
from config.model_config import llm
import logging

logger = logging.getLogger(__name__)

# Load synthetic upsell data
UPS_DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/synthetic_upsell_data.json")
with open(UPS_DATA_PATH, "r") as f:
    UPS_DATA = json.load(f)

# Upsell Agent Node using synthetic data

def upsell_recommendation_agent(state: State) -> Command[Literal["supervisor"]]:
    """
    Uses synthetic upsell data to suggest relevant services based on customer ID extracted via LLM.
    """
    # Step 1: Use LLM to extract customer ID from user message
    latest_user_message = next((m.content for m in reversed(state.messages) if m.role == "user"), "")

    extract_prompt = [
        {"role": "system", "content": "You are an assistant that extracts structured information from user input."},
        {"role": "user", "content": f"Extract the customer ID in the format CUST_XXXX from the following message. If not found, respond with NONE:\n\n{latest_user_message}"}
    ]

    customer_id = llm.invoke(extract_prompt).content.strip()
    if not re.match(r"CUST_\d+", customer_id):
        customer_id = None

    # Step 2: Match or fallback
    if customer_id:
        match = next((rec for rec in UPS_DATA if rec["customer_id"] == customer_id), None)
    else:
        match = None

    selected = match if match else random.choice(UPS_DATA)

    upsell_message = (
        f"For customer ID **{selected['customer_id']}**, located in {selected['location']} (ZIP: {selected['zip']}), "
        f"we recommend our **{selected['recommended_upsell']}**. Reason: {selected['reason']}"
    )

    logger.debug("Upsell recommendation selected: %s", selected)

    state.messages.append(Message(role="upsell", content=upsell_message))

    return Command(
        goto="supervisor",
        update={
            "messages": state.messages,
            "upsell_data": selected,
            "next_agent": "FINISH"
        }
    )
