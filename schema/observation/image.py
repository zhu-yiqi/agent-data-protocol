from pydantic import HttpUrl, Field

from schema.observation.observation import Observation


class ImageObservation(Observation):
    class_: str = Field("image_observation", description="The class of the observation")
    content: HttpUrl = Field(..., description="A URI to the image content")
    source: str = Field(None, description="The source of the observation (e.g. 'user')")
