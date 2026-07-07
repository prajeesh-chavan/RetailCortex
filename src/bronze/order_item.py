from src.bronze.runner import run_bronze_pipeline
from src.schemas.order_item_schema import ORDER_ITEM_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="order_items",
        kafka_topic="telemetry.ecommerce.order_items",
        schema=ORDER_ITEM_SCHEMA
    )
