from pydantic import Field

from schema.observation.image import ImageObservation
from schema.observation.observation import Observation

class WebObservation(Observation):
    url: str = Field(..., description="The URL of the web page")
    viewport_size: tuple[int, int] = Field(..., description="The size of the viewport")
    html: str = Field(..., description="The raw HTML of the web page")
    image_observation: ImageObservation = Field(
        ..., description="The image observation"
    )