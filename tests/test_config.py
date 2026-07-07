import pytest
from unittest.mock import patch
from pathlib import Path

from src.common.config import load_config


def test_load_config_returns_dict(tmp_path):
    config_file = tmp_path / "test.yaml"
    config_file.write_text("key: value\nnested:\n  inner: 42")
    result = load_config(str(config_file))
    assert result == {"key": "value", "nested": {"inner": 42}}


def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config(str(Path("/nonexistent/config.yaml")))


def test_load_config_empty_file(tmp_path):
    config_file = tmp_path / "empty.yaml"
    config_file.write_text("")
    result = load_config(str(config_file))
    assert result is None
