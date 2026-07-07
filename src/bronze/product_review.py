from src.bronze.runner import run_bronze_pipeline
from src.schemas.product_review_schema import PRODUCT_REVIEW_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="product_reviews",
        kafka_topic="telemetry.ecommerce.product_reviews",
        schema=PRODUCT_REVIEW_SCHEMA
    )
