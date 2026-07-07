from src.bronze.runner import run_bronze_pipeline
from src.schemas.inventory_schema import INVENTORY_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="inventory",
        kafka_topic="telemetry.ecommerce.inventory",
        schema=INVENTORY_SCHEMA
    )
