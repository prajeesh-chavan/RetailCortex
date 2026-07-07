from src.bronze.runner import run_bronze_pipeline
from src.schemas.category_schema import CATEGORY_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="categories",
        kafka_topic="telemetry.ecommerce.categories",
        schema=CATEGORY_SCHEMA
    )
