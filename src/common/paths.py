from pathlib import Path
from src.common.settings import SETTINGS


def bronze_path(entity):
    """
    Get the path for the bronze layer of a given entity.

    Args:
        entity (str): The name of the entity.

    Returns:
        Path: The path for the bronze layer of the given entity.
    """
    return Path(SETTINGS.bronze_dir) / entity

def checkpoint_path(entity):
    """
    Get the path for the checkpoint files of a given entity.

    Args:
        entity (str): The name of the entity.

    Returns:
        Path: The path for the checkpoint files of the given entity.
    """
    return Path(SETTINGS.checkpoint_dir) / entity