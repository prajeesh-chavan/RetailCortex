from src.bronze.runner import run_bronze_pipeline
from src.schemas.product_variant_schema import PRODUCT_VARIANT_SCHEMA

if __name__ == "__main__":
    run_bronze_pipeline(
        entity="product_variants",
        kafka_topic="telemetry.ecommerce.product_variants",
        schema=PRODUCT_VARIANT_SCHEMA
    )
