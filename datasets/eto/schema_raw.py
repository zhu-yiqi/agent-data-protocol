from pydantic import BaseModel, Field
from typing import List


class Conversation(BaseModel):
    from_: str = Field(..., alias='from')
    value: str


class SchemaRaw(BaseModel):
    id: str
    conversations: List[Conversation]
    reward: float
    source: str
