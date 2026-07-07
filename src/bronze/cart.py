from src.bronze.runner import run_bronze_pipeline
from src.schemas.cart_schema import CART_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="carts",
        kafka_topic="telemetry.ecommerce.carts",
        schema=CART_SCHEMA
    )
