from src.bronze.runner import run_bronze_pipeline
from src.schemas.return_schema import RETURN_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="returns",
        kafka_topic="telemetry.ecommerce.returns",
        schema=RETURN_SCHEMA
    )
