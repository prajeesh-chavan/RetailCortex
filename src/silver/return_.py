from pyspark.sql.functions import col, to_timestamp, lower
from src.schemas.return_schema import RETURN_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_return(df):
    return df \
        .withColumn("return_timestamp", to_timestamp("return_timestamp")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "return_id",
            "order_id",
            "customer_id",
            "return_number",
            "return_reason",
            "return_status",
            "return_timestamp",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="returns",
        bronze_schema=RETURN_BRONZE_SCHEMA,
        transform_func=transform_return,
        table_name="returns",
        merge_key="return_id"
    )
