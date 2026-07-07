from src.bronze.runner import run_bronze_pipeline
from src.schemas.order_address_schema import ORDER_ADDRESS_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="order_addresses",
        kafka_topic="telemetry.ecommerce.order_addresses",
        schema=ORDER_ADDRESS_SCHEMA
    )
