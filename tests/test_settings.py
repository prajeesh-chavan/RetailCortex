import os
from pathlib import Path
from src.common.settings import Settings


def test_default_paths():
    s = Settings()
    root = s.project_root
    assert (root / "src").is_dir()
    assert s.snowflake_config == str(root / "config" / "snowflake.yaml")
    assert s.kafka_config == str(root / "config" / "kafka.yaml")
    assert s.bronze_dir == str(root / "data" / "bronze")
    assert s.checkpoint_dir == str(root / "data" / "checkpoints")


def test_env_overrides():
    s = Settings()
    root = s.project_root
    assert s.snowflake_config == str(root / "config" / "snowflake.yaml")

    with patch_os_environ("SNOWFLAKE_CONFIG_PATH", "/custom/snowflake.yaml"):
        assert s.snowflake_config == "/custom/snowflake.yaml"

    with patch_os_environ("BRONZE_DIR", "/data/bronze_custom"):
        assert s.bronze_dir == "/data/bronze_custom"


def patch_os_environ(key, value):
    import contextlib

    @contextlib.contextmanager
    def _patch():
        old = os.environ.get(key)
        os.environ[key] = value
        try:
            yield
        finally:
            if old is None:
                del os.environ[key]
            else:
                os.environ[key] = old
    return _patch()
