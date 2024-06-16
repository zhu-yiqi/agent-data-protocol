# agent-data-collection

This is a repository for agent training data collection by CMU, OSU, and HKU.

- `datasets`: Contains datasets, each with at least the following elements
  - `README.md`: A description of the dataset
  - `sample_raw.jsonl`: 2-5 raw samples from the corpus in the original format, converted to JSONL
  - `sample_processed.jsonl`: 2-5 samples from the corpus in our unified format
  - `extract_raw.py`: A script that extracts the raw jsonl file from the corpus
  - `raw_to_processed.py`: A script that converts the raw jsonl file to our unified format
- `validator`: Contains scripts that validate the dataset format
