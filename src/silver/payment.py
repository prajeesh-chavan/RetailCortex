from pyspark.sql.functions import col, to_timestamp
from src.schemas.payment_schema import PAYMENT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_payment(df):
    return df \
        .withColumn("amount", col("amount").cast("decimal(12,2)")) \
        .withColumn("processed_at", to_timestamp("processed_at")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "payment_id",
            "order_id",
            "payment_provider",
            "provider_payment_reference",
            "payment_method",
            "payment_status",
            "amount",
            "currency_code",
            "failure_code",
            "failure_reason",
            "processed_at",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="payments",
        bronze_schema=PAYMENT_BRONZE_SCHEMA,
        transform_func=transform_payment,
        table_name="payments",
        merge_key="payment_id"
    )
