from fastapi import APIRouter, Request
from pydantic import BaseModel
# from agents.supervisor_agent import handle_query

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def sales_assistant(request: ChatRequest):
    # response = handle_query(request.query)
    response = "Hello World!"
    return {"response": response}