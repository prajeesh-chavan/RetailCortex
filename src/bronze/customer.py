from src.bronze.runner import run_bronze_pipeline
from src.schemas.customer_schema import CUSTOMER_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="customers",
        kafka_topic="telemetry.ecommerce.customers",
        schema=CUSTOMER_SCHEMA
    )

