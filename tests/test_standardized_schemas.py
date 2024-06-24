import os
import json
from pydantic import ValidationError
import pytest
from pathlib import Path

from schema.trajectory import Trajectory

DATASET_PATH = Path(__file__).parent.parent / "datasets"


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
    samples = load_json(sample_path)
    assert isinstance(samples, list), "sample.json should be a list"

    for sample in samples:
        try:
            Trajectory(**sample)
        except ValidationError as e:
            pytest.fail(f"Validation failed for {sample_path}: {str(e)}")
