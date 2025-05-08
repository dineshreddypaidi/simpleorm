import pytest

import tempfile
import json
from simpleorm.config import load_from_json, load_from_url  # Replace with actual module name

def test_load_from_json():
    # Create a temporary JSON file
    data = {"engine": "sqlite", "database": "test.db"}
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        json.dump(data, tmp)
        tmp.seek(0)
        file_path = tmp.name

    result = load_from_json(file_path)
    assert result == data


def test_load_from_url():
    url = "postgresql://user:pass@localhost:5432/mydatabase"
    expected = {
        "engine": "postgresql",
        "user": "user",
        "password": "pass",
        "host": "localhost",
        "database": "mydatabase",
    }
    result = load_from_url(url)
    assert result == expected
