import json
import sys
import re


def convert_step(step: dict[str, str]) -> list[dict[str, str]]:
    system_regex = re.match(
        r"(You are an assistant.*\n\nNow, my problem is:|Now, I will start a new problem in a new OS. My problem is:)\n\n(.*)",
        step["content"],
        re.DOTALL,
    )
    code_act_regex = re.match(r"Think: (.*)\n\nAct: (.*)", step["content"], re.DOTALL)
    code_obs_regex = re.match(
        r"The output of the OS:\n(.*)", step["content"], re.DOTALL
    )
    if system_regex:
        return [
            {
                "class": "text_observation",
                "content": system_regex.group(1),
                "source": "system",
            },
            {
                "class": "text_observation",
                "content": system_regex.group(2),
                "source": "user",
            },
        ]
    elif code_act_regex:
        code_extract_regex = re.match(
            r"bash\n\n```bash\n(.*)\n```", code_act_regex.group(2), re.DOTALL
        )
        answer_extract_regex = re.match(
            r"answer\((.*)\)", code_act_regex.group(2), re.DOTALL
        )
        if code_extract_regex:
            return [
                {
                    "class": "code_action",
                    "language": "bash",
                    "content": code_extract_regex.group(1),
                    "description": code_act_regex.group(1),
                }
            ]
        elif answer_extract_regex:
            return [
                {
                    "class": "message_action",
                    "content": answer_extract_regex.group(1),
                    "description": code_act_regex.group(1),
                }
            ]
        else:
            raise ValueError(
                "Could not extract code from code action in"
                f" {json.dumps(step, indent=2)}"
            )
    elif code_obs_regex:
        return [
            {
                "class": "text_observation",
                "content": code_obs_regex.group(1),
                "source": "os",
            }
        ]
    else:
        return [
            {
                "class": "text_observation",
                "content": step["content"],
                "source": "user",
            }
        ]


for line in sys.stdin:
    raw_data = json.loads(line)

    content = []
    for step in raw_data["conversations"]:
        content.extend(convert_step(step))

    # Standardize the data
    standardize_data = {
        "id": raw_data["id"],
        "content": content,
    }

    # Print the standardized data
    print(json.dumps(standardize_data))
