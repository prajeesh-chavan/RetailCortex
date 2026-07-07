from src.bronze.runner import run_bronze_pipeline
from src.schemas.order_status_history_schema import ORDER_STATUS_HISTORY_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="order_status_history",
        kafka_topic="telemetry.ecommerce.order_status_history",
        schema=ORDER_STATUS_HISTORY_SCHEMA
    )
