
from pydantic import BaseModel
from typing import List

class Conversation(BaseModel):
    from_: str
    value: str

class SchemaRaw(BaseModel):
    id: str
    conversations: List[Conversation]
    reward: float
    source: str
