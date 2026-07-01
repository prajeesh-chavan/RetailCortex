from pathlib import Path


PROJECT_ROOT = Path.cwd()

def bronze_path(entity):
    """
    Get the path for the bronze layer of a given entity.

    Args:
        entity (str): The name of the entity.

    Returns:
        Path: The path for the bronze layer of the given entity.
    """
    return PROJECT_ROOT / "Data" / "bronze" / entity

def checkpoint_path(entity):
    """
    Get the path for the checkpoint files of a given entity.

    Args:
        entity (str): The name of the entity.

    Returns:
        Path: The path for the checkpoint files of the given entity.
    """
    return PROJECT_ROOT / "Data" / "checkpoints" / entity