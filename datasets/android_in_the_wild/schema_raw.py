
from pydantic import BaseModel
from typing import List

class SchemaRaw(BaseModel):
    image_width: int
    image_height: int
    results_yx_touch: List[float]
    results_type_action: str
    android_api_level: int
    image_ui_annotations_text: List[str]
    results_yx_lift: List[float]
    image_ui_annotations_ui_types: List[str]
    current_activity: str
    step_id: int
    image_channels: int
    episode_length: int
    image_encoded: str
    results_action_type: str
    goal_info: str
    image_ui_annotations_positions: List[List[float]]
    episode_id: str
    device_type: str
