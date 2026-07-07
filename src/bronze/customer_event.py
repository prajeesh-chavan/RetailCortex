from src.bronze.runner import run_bronze_pipeline
from src.schemas.customer_event_schema import CUSTOMER_EVENT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="customer_events",
        kafka_topic="telemetry.ecommerce.customer_events",
        schema=CUSTOMER_EVENT_SCHEMA
    )
