from pyspark.sql.functions import col, to_timestamp, lower
from src.schemas.vendor_address_schema import VENDOR_ADDRESS_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_vendor_address(df):
    return df \
        .withColumn("is_default", lower(col("is_default")).cast("boolean")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "vendor_address_id",
            "vendor_id",
            "address_id",
            "address_type",
            "is_default",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="vendor_addresses",
        bronze_schema=VENDOR_ADDRESS_BRONZE_SCHEMA,
        transform_func=transform_vendor_address,
        table_name="vendor_addresses",
        merge_key="vendor_address_id"
    )
