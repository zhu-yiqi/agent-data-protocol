import json
import sys
from typing import Any


prev_id = None
content = []


def flush_episode(curr_data: dict[str, Any]):
    if content:
        print(json.dumps(content))
        content.clear()
    content.append(
        {
            "class": "message_action",
            "content": curr_data["goal_info"],
        }
    )


for line in sys.stdin:
    data = json.loads(line)
    if prev_id != data["episode_id"]:
        flush_episode(data)
        prev_id = data["episode_id"]
    # Create the image observation
    raise NotImplementedError
    # Create the action
    content.append({})


if content:
    print(json.dumps(content))
