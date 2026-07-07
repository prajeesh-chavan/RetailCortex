import os

from dotenv import load_dotenv

load_dotenv()

import yaml  # noqa: E402 — intentional: load_dotenv before yaml


def load_config(config_path: str) -> dict:
    """
    Load a YAML configuration file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_snowflake_options():
    from src.common.settings import SETTINGS
    config = load_config(SETTINGS.snowflake_config)
    return {
        "sfURL": os.environ.get("SNOWFLAKE_URL"),
        "sfDatabase": config["database"],
        "sfSchema": config["schema"],
        "sfWarehouse": config["warehouse"],
        "sfRole": config["role"],
        "sfUser": os.environ.get("SNOWFLAKE_USER"),
        "sfPassword": os.environ.get("SNOWFLAKE_PASSWORD")
    }

def get_kafka_config():
    from src.common.settings import SETTINGS
    config = load_config(SETTINGS.kafka_config)
    return config
