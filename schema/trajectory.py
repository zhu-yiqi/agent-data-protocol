from pydantic import BaseModel

from schema.action.action import Action
from schema.observation.observation import Observation


class Trajectory(BaseModel):
    id: str
    content: list[Action | Observation]
