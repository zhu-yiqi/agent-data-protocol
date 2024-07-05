from pydantic import BaseModel, Field

from schema.action.api import ApiAction
from schema.action.code import CodeAction
from schema.action.message import MessageAction
from schema.observation.image import ImageObservation
from schema.observation.text import TextObservation
from schema.observation.web import WebObservation


class Trajectory(BaseModel):
    id: str
    content: list[
        ApiAction | CodeAction | MessageAction | TextObservation | ImageObservation | WebObservation
    ]
