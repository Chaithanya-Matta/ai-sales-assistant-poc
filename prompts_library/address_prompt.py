from langchain_core.messages import SystemMessage

PARSE_ADDRESS_SYSTEM_PROMPT = SystemMessage(
    content="""
    Extract the address components from the following user input. 
    Return in JSON format with keys: street, unit, city, state, zip.
    """
)

LLM_ADDRESS_MATCH_SYSTEM_PROMPT = SystemMessage(
    content="""You are a smart address-matching assistant.
    Given a user-entered address and a list of retrieved addresses, 
    identify which ones refer to the same location, even if formatting or parts are different.
    """
)