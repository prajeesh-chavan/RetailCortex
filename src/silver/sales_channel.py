from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.sales_channel_schema import SALES_CHANNEL_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_sales_channel(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "channel_id",
            "channel_name",
            "channel_type",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="sales_channels",
        bronze_schema=SALES_CHANNEL_BRONZE_SCHEMA,
        transform_func=transform_sales_channel,
        table_name="sales_channels",
        merge_key="channel_id"
    )
