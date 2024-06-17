from datasets import load_dataset
import json

dataset = load_dataset("m-a-p/Code-Feedback", split="train")

sample_raw = []
out_fname = open("sample_raw.json", "w+")

i = 0
for sample in dataset:
    sample_raw.append(sample)
    print(json.dumps(sample))
    i += 1
    
    if i >= 5:
        break

json.dump(sample_raw, out_fname, indent=2)