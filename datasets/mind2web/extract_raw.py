from datasets import load_dataset
import json

dataset = load_dataset("osunlp/Mind2Web", split="train")

for sample in dataset:
    print(json.dumps(sample))
