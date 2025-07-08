from typing import Literal
from langgraph.types import Command
from state.state import State, Message
from config.model_config import llm
from prompts_library import chat_prompt
import logging

logger = logging.getLogger(__name__)

def chat_agent(state: State) -> Command[Literal["supervisor"]]:
    logger.info("Entered CHAT AGENT")
    messages = [chat_prompt.SYSTEM_PROMPT] + [{"role": "user", "content": state.query}]
    response = llm.invoke(messages)
    logger.info(response.content)
    state.messages.append(Message(role="chat", content=response.content))
    logger.info("END CHAT AGENT")
    return Command(
        goto="supervisor", 
        update={
            "messages": state.messages,
            "next_agent": "FINISH"
        }
    )
 