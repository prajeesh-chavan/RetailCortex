from src.bronze.runner import run_bronze_pipeline
from src.schemas.sales_channel_schema import SALES_CHANNEL_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="sales_channels",
        kafka_topic="telemetry.ecommerce.sales_channels",
        schema=SALES_CHANNEL_SCHEMA
    )
