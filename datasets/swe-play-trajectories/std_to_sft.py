#!/usr/bin/env python3
"""Convert standardized format to SFT format for swe-play-trajectories dataset."""

import json
import sys


def standardized_to_sft(trajectory):
    """
    Convert a standardized trajectory to SFT format.

    The SFT format has:
    - id: trajectory ID
    - system: system prompt (includes the first user message which contains examples/instructions)
    - conversations: list of turns with "from" and "value" fields
    """
    conversations = []
    system_prompt = ""
    first_user_message = True

    for item in trajectory["content"]:
        class_name = item["class_"]

        # Convert based on class type
        if class_name == "text_observation":
            if item.get("source") == "user":
                # The first user message contains examples and should go to system prompt
                if first_user_message:
                    system_prompt = item["content"]
                    first_user_message = False
                else:
                    conversations.append({"from": "human", "value": item["content"]})
            elif item.get("source") == "environment":
                conversations.append({"from": "observation", "value": item["content"]})

        elif class_name == "code_action":
            # Format code action as a function call
            description = item.get("description", "")
            content = item["content"]
            language = item.get("language", "bash")

            # Format similar to other datasets
            value = ""
            if description:
                value += f"{description}\n\n"
            value += f"```{language}\n{content}\n```"

            conversations.append({"from": "function_call", "value": value})

        elif class_name == "api_action":
            # Format API action as a function call
            description = item.get("description", "")
            function = item["function"]
            kwargs = item.get("kwargs", {})

            value = ""
            if description:
                value += f"{description}\n\n"
            value += f"<function={function}>"
            if kwargs:
                for key, val in kwargs.items():
                    value += f"\n<parameter={key}>{val}</parameter>"
            value += "\n</function>"

            conversations.append({"from": "function_call", "value": value})

        elif class_name == "message_action":
            # Format message action as a function call
            conversations.append({"from": "function_call", "value": item["content"]})

    return {"id": trajectory["id"], "system": system_prompt, "conversations": conversations}


def main():
    """Read JSONL from stdin and write JSONL to stdout."""
    for line in sys.stdin:
        if not line.strip():
            continue

        trajectory = json.loads(line)
        sft_trajectory = standardized_to_sft(trajectory)
        print(json.dumps(sft_trajectory))


if __name__ == "__main__":
    main()
