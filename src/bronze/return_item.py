from src.bronze.runner import run_bronze_pipeline
from src.schemas.return_item_schema import RETURN_ITEM_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="return_items",
        kafka_topic="telemetry.ecommerce.return_items",
        schema=RETURN_ITEM_SCHEMA
    )
