from fastapi import APIRouter
from pydantic import BaseModel
from state.state import State, Message
from orchestrator.coordinator import app


router = APIRouter()

class ChatRequest(BaseModel):
    query: str

# @router.post("/chat")
# async def sales_assistant(request: ChatRequest):
#     # response = handle_query(request.query)
#     response = "Hello World!"
#     return {"response": response}

@router.post("/chat")
async def sales_assistant(request: ChatRequest):
    query = request.query

    # Step 1: Build the initial state
    state = State(
        query=query,
        messages=[Message(role="user", content=query)],
        next_agent="supervisor",
        retrieval_attempts=0
    )

    # Step 2: Run LangGraph
    result = app.invoke(state)

    # Step 3: Format response
    final_response = result["messages"][-1].content if result["messages"] else "No response generated"
    # return {
    #     "final_message": final_response,
    #     "all_messages": [m.dict() for m in result.messages],
    #     "address_results": [r for r in result.address_results] if result.address_results else [],
    #     "retrieval_attempts": result.retrieval_attempts
    # }
    return { "response": final_response }