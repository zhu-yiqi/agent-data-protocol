import os
import json
import pytest
from jsonschema import validate, ValidationError, RefResolver
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "datasets"
TRAJECTORY_SCHEMA = Path(__file__).parent.parent / "schema" / "trajectory.json"


def get_sample_jsons(directory):
    # get DATASET_PATH/*/sample.json files
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        sample_path = os.path.join(subdir_path, "sample.json")
        if os.path.exists(sample_path):
            yield sample_path


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


@pytest.mark.parametrize("sample_path", get_sample_jsons(DATASET_PATH))
def test_sample_raw_against_schema(sample_path):
    schema = load_json(TRAJECTORY_SCHEMA)
    samples = load_json(sample_path)
    schema_path = f'file:///{os.path.dirname(TRAJECTORY_SCHEMA)}/'
    resolver = RefResolver(base_uri=schema_path, referrer=schema)
    assert isinstance(samples, list), "sample.json should be a list"

    for sample in samples:
        try:
            validate(instance=sample, schema=schema, resolver=resolver)
        except ValidationError as e:
            pytest.fail(f"Validation failed for {sample_path}: {str(e)}")
