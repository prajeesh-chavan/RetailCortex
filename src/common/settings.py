import os
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


class Settings:
    def __init__(self):
        self._project_root = _project_root()

    @property
    def project_root(self) -> Path:
        return self._project_root

    @property
    def snowflake_config(self) -> str:
        return os.environ.get(
            "SNOWFLAKE_CONFIG_PATH",
            str(self._project_root / "config" / "snowflake.yaml")
        )

    @property
    def kafka_config(self) -> str:
        return os.environ.get(
            "KAFKA_CONFIG_PATH",
            str(self._project_root / "config" / "kafka.yaml")
        )

    @property
    def bronze_dir(self) -> str:
        return os.environ.get(
            "BRONZE_DIR",
            str(self._project_root / "Data" / "bronze")
        )

    @property
    def checkpoint_dir(self) -> str:
        return os.environ.get(
            "CHECKPOINT_DIR",
            str(self._project_root / "Data" / "checkpoints")
        )


SETTINGS = Settings()
