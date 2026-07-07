from src.bronze.runner import run_bronze_pipeline
from src.schemas.address_schema import ADDRESS_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="addresses",
        kafka_topic="telemetry.ecommerce.addresses",
        schema=ADDRESS_SCHEMA
    )
