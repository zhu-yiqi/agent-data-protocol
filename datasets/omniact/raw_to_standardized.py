import json
import sys
import re

from schema.action.action import Action
from schema.action.code import CodeAction
from schema.observation.observation import Observation
from schema.observation.text import TextObservation
from schema.observation.image import BoundingBox, ImageObservation, ImageAnnotation
from schema.trajectory import Trajectory


def convert_example(example: dict[str, str]) -> list[Action | Observation]:
    task_regex = re.match(
        r"Task: (.*)\nOutput Script:\n(.*)", example["task"], re.DOTALL
    )
    annotations = [
        ImageAnnotation(
            text=example["box"]["label"][index],
            element_type="button",
            bounding_box=BoundingBox(
                x=example["box"]["top_left"][index][0],
                y=example["box"]["top_left"][index][1],
                width=example["box"]["bottom_right"][index][0]
                - example["box"]["top_left"][index][0],
                height=example["box"]["bottom_right"][index][1]
                - example["box"]["top_left"][index][1],
            ),
        )
        for index in range(len(example["box"]))
    ]
    return [
        ImageObservation(
            content=example["image"],
            annotations=annotations,
            source="os",
        ),
        TextObservation(content=task_regex.group(1), source="user"),
        CodeAction(
            language="python",
            content=task_regex.group(2),
            description="Output Script",
        ),
    ]


for line in sys.stdin:
    raw_example = json.loads(line)
    example = convert_example(raw_example)

    traj: Trajectory = Trajectory(
        id=raw_example["id"],
        content=example,
    )
    print(traj.model_dump_json())
