from src.bronze.runner import run_bronze_pipeline
from src.schemas.inventory_movement_schema import INVENTORY_MOVEMENT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="inventory_movements",
        kafka_topic="telemetry.ecommerce.inventory_movements",
        schema=INVENTORY_MOVEMENT_SCHEMA
    )
