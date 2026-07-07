from src.bronze.runner import run_bronze_pipeline
from src.schemas.order_item_discount_schema import ORDER_ITEM_DISCOUNT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="order_item_discounts",
        kafka_topic="telemetry.ecommerce.order_item_discounts",
        schema=ORDER_ITEM_DISCOUNT_SCHEMA
    )
