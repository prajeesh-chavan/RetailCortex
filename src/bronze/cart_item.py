from src.bronze.runner import run_bronze_pipeline
from src.schemas.cart_item_schema import CART_ITEM_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="cart_items",
        kafka_topic="telemetry.ecommerce.cart_items",
        schema=CART_ITEM_SCHEMA
    )
