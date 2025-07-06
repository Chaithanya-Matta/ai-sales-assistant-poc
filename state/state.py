from pydantic import BaseModel
from typing import List, Dict, Any, Literal, Optional
from models.address import RetrievedAddress

class Message(BaseModel):
    role: Literal["user", "supervisor", "upsell", "chat", "address"]
    content: str

class State(BaseModel):
    query:str
    messages: List[Message] = []
    next_agent: Literal["supervisor", "upsell", "address", "chat", "FINISH"]
    upsell_data: Optional[Dict[str, Any]] = None
    address_results: Optional[List[RetrievedAddress]] = None
    retrieval_attempts: int = 0