
from pydantic import BaseModel
from typing import List, Optional

class APIParams(BaseModel):
    boxes: Optional[List[List[float]]]
    prompt: Optional[str]

class Action(BaseModel):
    API_name: str
    API_params: APIParams

class Conversation(BaseModel):
    from_: str
    value: str
    thoughts: Optional[str]
    actions: Optional[List[Action]]

class SchemaRaw(BaseModel):
    unique_id: str
    image: str
    conversations: List[Conversation]
    data_source: str
