import os
import json
import pytest
from jsonschema import validate, ValidationError
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "datasets"


def get_subdirectories(directory):
    return [
        d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))
    ]


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


@pytest.mark.parametrize("subdir", get_subdirectories(DATASET_PATH))
def test_sample_raw_against_schema(subdir):
    subdir_path = os.path.join(DATASET_PATH, subdir)

    schema_path = os.path.join(subdir_path, "schema_raw.json")
    sample_path = os.path.join(subdir_path, "sample_raw.json")

    assert os.path.exists(
        schema_path
    ), f"schema_raw.json not found in {subdir_path}"
    assert os.path.exists(
        sample_path
    ), f"sample_raw.json not found in {subdir_path}"

    schema = load_json(schema_path)
    samples = load_json(sample_path)

    assert isinstance(samples, list), "sample_raw.json should be a list"

    for sample in samples:
        try:
            validate(instance=sample, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Validation failed for {subdir}: {str(e)}")
