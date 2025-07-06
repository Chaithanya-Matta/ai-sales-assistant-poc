from pydantic import BaseModel
from typing import Optional

class ParsedAddress(BaseModel):
    """Represents a structured address parsed from the user's free-form text input."""
    street: str
    unit: str = ""
    city: str
    state: str
    zip: str = ""

class RetrievedAddress(BaseModel):
    """Represents a complete address record retrieved from the database."""
    id: str
    address1: str
    address2: Optional[str]
    city: str
    state: str
    zip: str

class RetrievedAddressScore(RetrievedAddress):
    score: str