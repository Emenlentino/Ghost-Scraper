# tests/test_data_handler.py
import os
import tempfile
import pytest
from myproject.data_handler import save_data, load_data, compare_and_save

@pytest.fixture
def sample_data():
    return {"CountryA": [{"City": "CityA", "Population": 1000, "Area": 100, "Population Density": 10}]}

def test_save_and_load_data(sample_data):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        filename = tmp_file.name
    try:
        save_data(sample_data, filename)
        loaded = load_data(filename)
        assert loaded == sample_data
    finally:
        os.remove(filename)

def test_compare_and_save(sample_data):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        filename = tmp_file.name
    try:
        # If no data exists, an update should occur.
        result = compare_and_save(sample_data, {}, filename)
        assert result is True

        # With data unchanged, no update should occur.
        loaded = load_data(filename)
        result = compare_and_save(sample_data, loaded, filename)
        assert result is False
    finally:
        os.remove(filename)
