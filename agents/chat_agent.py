from typing import Literal
from langgraph.types import Command
from state.state import State, Message
from config.model_config import llm
from prompts_library import chat_prompt

def chat_agent(state: State) -> Command[Literal["supervisor"]]:
    print("*****************************Entered CHAT AGENT****************************************************")
    messages = [chat_prompt.SYSTEM_PROMPT] + [{"role": "user", "content": state.query}]
    response = llm.invoke(messages)
    print(response.content)
    state.messages.append(Message(role="chat", content=response.content))
    print("*****************************END CHAT AGENT****************************************************")
    return Command(
        goto="supervisor", 
        update={
            "messages": state.messages,
            "next_agent": "FINISH"
        }
    )
 