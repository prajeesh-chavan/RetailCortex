from pyspark.sql.functions import col, to_timestamp
from src.schemas.refund_schema import REFUND_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_refund(df):
    return df \
        .withColumn("refund_amount", col("refund_amount").cast("decimal(12,2)")) \
        .withColumn("processed_at", to_timestamp("processed_at")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "refund_id",
            "order_id",
            "payment_id",
            "refund_reference",
            "refund_status",
            "refund_reason",
            "refund_amount",
            "currency_code",
            "processed_at",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="refunds",
        bronze_schema=REFUND_BRONZE_SCHEMA,
        transform_func=transform_refund,
        table_name="refunds",
        merge_key="refund_id"
    )
