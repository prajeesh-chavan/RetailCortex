from src.bronze.runner import run_bronze_pipeline
from src.schemas.vendor_schema import VENDOR_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="vendors",
        kafka_topic="telemetry.ecommerce.vendors",
        schema=VENDOR_SCHEMA
    )
