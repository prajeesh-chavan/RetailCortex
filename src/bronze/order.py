from src.bronze.runner import run_bronze_pipeline
from src.schemas.order_schema import ORDER_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="orders",
        kafka_topic="telemetry.ecommerce.orders",
        schema=ORDER_SCHEMA
    )
