from src.bronze.runner import run_bronze_pipeline
from src.schemas.promotion_schema import PROMOTION_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="promotions",
        kafka_topic="telemetry.ecommerce.promotions",
        schema=PROMOTION_SCHEMA
    )
