from src.bronze.runner import run_bronze_pipeline
from src.schemas.warehouse_schema import WAREHOUSE_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="warehouses",
        kafka_topic="telemetry.ecommerce.warehouses",
        schema=WAREHOUSE_SCHEMA
    )
