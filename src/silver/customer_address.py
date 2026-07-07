from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.customer_address_schema import CUSTOMER_ADDRESS_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_customer_address(df):
    return df \
        .withColumn("is_default", lower(col("is_default")).cast("boolean")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "customer_address_id",
            "customer_id",
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
        entity="customer_addresses",
        bronze_schema=CUSTOMER_ADDRESS_BRONZE_SCHEMA,
        transform_func=transform_customer_address,
        table_name="customer_addresses",
        merge_key="customer_address_id"
    )
