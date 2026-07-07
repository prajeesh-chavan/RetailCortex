from src.bronze.runner import run_bronze_pipeline
from src.schemas.shipment_schema import SHIPMENT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="shipments",
        kafka_topic="telemetry.ecommerce.shipments",
        schema=SHIPMENT_SCHEMA
    )
