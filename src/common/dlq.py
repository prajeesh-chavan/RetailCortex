from pathlib import Path

from src.common.logger import setup_logger
from src.common.settings import SETTINGS

logger = setup_logger("dlq")


def dead_letter_path(layer, entity):
    return (
        Path(SETTINGS.bronze_dir).parent
        / "dead_letter"
        / layer
        / entity
    )


def write_bronze_dlq(bad_df, entity):
    dlq_path = str(dead_letter_path("bronze", entity))
    count = bad_df.count() if not bad_df.isEmpty() else 0

    if count > 0:
        bad_df.write.mode("append").json(dlq_path)
        logger.warning(f"{count} malformed records routed to DLQ {dlq_path}")

    return count


def write_silver_dlq(batch_df, entity, error):
    dlq_path = str(dead_letter_path("silver", entity))
    count = batch_df.count() if not batch_df.isEmpty() else 0

    if count > 0:
        batch_df.write.mode("append").json(dlq_path)
        logger.error(f"{count} records routed to DLQ {dlq_path} | reason: {error}")

    return count
