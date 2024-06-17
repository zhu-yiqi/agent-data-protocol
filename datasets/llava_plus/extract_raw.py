from huggingface_hub import hf_hub_download
import json

# Using load_dataset() directly will lead to issues due to misaligned formats in llava plus
dataset_llava_plus_fname = hf_hub_download(
    repo_id="LLaVA-VL/llava-plus-data", 
    repo_type="dataset",
    filename="llava-plus-v1-117k-tool-merge.json", 
    local_dir="./"
)

with open(dataset_llava_plus_fname) as f:
    dataset_llava_plus = json.load(f)

dataset_llava_fname = hf_hub_download(
    repo_id="LLaVA-VL/llava-plus-data", 
    repo_type="dataset",
    filename="llava-150k-tool-aug.json", 
    local_dir="./"
)

with open(dataset_llava_fname) as f:
    dataset_llava = json.load(f)

# Cleaning llava plus data
# Removing attributes with both int and str values (causing PyArrow error) and get a unified format
dataset = []
useful_attrs = ['unique_id', 'image', 'conversations', 'data_source']

removed_num_examples = 0

for example in dataset_llava_plus:
    cleaned_example = {}
    for attr in useful_attrs:
        try:
            cleaned_example[attr] = example[attr]   
        except:
            if (
                attr == "image" and attr not in example and 
                "id" in example and example["id"].endswith(".png")
            ):
                cleaned_example[attr] = example["id"]
            else:
                # Should not happen; Number of removed examples should be 0
                removed_num_examples += 1
                break
    dataset.append(cleaned_example)

for example in dataset_llava:
    cleaned_example = {}
    for attr in useful_attrs:
        cleaned_example[attr] = example[attr]
    dataset.append(cleaned_example)

print("Final dataset size:", len(dataset))
print("Number of removed examples:", removed_num_examples)

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