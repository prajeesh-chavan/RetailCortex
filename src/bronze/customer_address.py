from src.bronze.runner import run_bronze_pipeline
from src.schemas.customer_address_schema import CUSTOMER_ADDRESS_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="customer_addresses",
        kafka_topic="telemetry.ecommerce.customer_addresses",
        schema=CUSTOMER_ADDRESS_SCHEMA
    )
