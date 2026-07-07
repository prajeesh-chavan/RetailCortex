from pyspark.sql.functions import col, to_timestamp
from src.schemas.order_status_history_schema import ORDER_STATUS_HISTORY_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_order_status_history(df):
    return df \
        .withColumn("status_timestamp", to_timestamp("status_timestamp")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "order_status_history_id",
            "order_id",
            "status",
            "status_timestamp",
            "status_reason",
            "changed_by",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="order_status_history",
        bronze_schema=ORDER_STATUS_HISTORY_BRONZE_SCHEMA,
        transform_func=transform_order_status_history,
        table_name="order_status_history",
        merge_key="order_status_history_id"
    )
