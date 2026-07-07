from src.bronze.runner import run_bronze_pipeline
from src.schemas.vendor_address_schema import VENDOR_ADDRESS_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="vendor_addresses",
        kafka_topic="telemetry.ecommerce.vendor_addresses",
        schema=VENDOR_ADDRESS_SCHEMA
    )
