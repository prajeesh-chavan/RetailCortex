from src.bronze.runner import run_bronze_pipeline
from src.schemas.product_schema import PRODUCT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="products",
        kafka_topic="telemetry.ecommerce.products",
        schema=PRODUCT_SCHEMA
    )
