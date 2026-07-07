from src.bronze.runner import run_bronze_pipeline
from src.schemas.refund_schema import REFUND_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="refunds",
        kafka_topic="telemetry.ecommerce.refunds",
        schema=REFUND_SCHEMA
    )
