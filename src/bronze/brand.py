from src.bronze.runner import run_bronze_pipeline
from src.schemas.brand_schema import BRAND_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="brands",
        kafka_topic="telemetry.ecommerce.brands",
        schema=BRAND_SCHEMA
    )
