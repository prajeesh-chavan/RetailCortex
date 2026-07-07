from src.bronze.runner import run_bronze_pipeline
from src.schemas.shipment_item_schema import SHIPMENT_ITEM_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="shipment_items",
        kafka_topic="telemetry.ecommerce.shipment_items",
        schema=SHIPMENT_ITEM_SCHEMA
    )
