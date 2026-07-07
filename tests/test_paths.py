from pathlib import Path
from src.common.paths import bronze_path, checkpoint_path


def test_bronze_path():
    p = bronze_path("customer")
    assert isinstance(p, Path)
    assert p.name == "customer"
    assert "bronze" in str(p)


def test_checkpoint_path():
    p = checkpoint_path("customer")
    assert isinstance(p, Path)
    assert p.name == "customer"
    assert "checkpoints" in str(p)
