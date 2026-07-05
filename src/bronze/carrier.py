from src.bronze.runner import run_bronze_pipeline
from src.schemas.carrier_schema import CARRIER_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="carriers",
        kafka_topic="telemetry.ecommerce.carriers",
        schema=CARRIER_SCHEMA
    )
