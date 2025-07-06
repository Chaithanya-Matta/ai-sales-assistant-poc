from typing import Dict, List
from state.state import Message


def convert_state_messages_to_llm_format(state_messages: List[Message]) -> List[Dict[str, str]]:
    """Convert state message roles to LLM-compatible format."""
    valid_roles = {"user": "user", "chat": "user", "upsell": "assistant", "address": "assistant"}

    llm_messages = []
    for msg in state_messages:
        if msg["role"] in valid_roles:
            llm_messages.append({
                "role": valid_roles[msg["role"]],
                "content": msg["content"]
            })
        # Skip roles like 'supervisor' or any others
    return llm_messages
