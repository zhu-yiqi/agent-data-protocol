from pydantic import Field
from typing import Literal

from schema.action.action import Action


class CodeAction(Action):
    language: str = Field(
        ..., description="The language of the code to execute" # code_feedback is multilingual
    )
    content: str = Field(..., description="The code to execute")
    description: str = Field(
        ..., description="The description/thought provided for the action"
    )
