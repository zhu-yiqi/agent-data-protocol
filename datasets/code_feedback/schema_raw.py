
from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class SchemaRaw(BaseModel):
    id: int
    messages: List[Message]
