from src.bronze.runner import run_bronze_pipeline
from src.schemas.payment_schema import PAYMENT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="payments",
        kafka_topic="telemetry.ecommerce.payments",
        schema=PAYMENT_SCHEMA
    )
