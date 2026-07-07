from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.order_schema import ORDER_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_order(df):
    return df \
        .withColumn("order_timestamp", to_timestamp("order_timestamp")) \
        .withColumn("subtotal_amount", col("subtotal_amount").cast("decimal(12,2)")) \
        .withColumn("discount_amount", col("discount_amount").cast("decimal(12,2)")) \
        .withColumn("tax_amount", col("tax_amount").cast("decimal(12,2)")) \
        .withColumn("shipping_amount", col("shipping_amount").cast("decimal(12,2)")) \
        .withColumn("total_amount", col("total_amount").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "order_id",
            "customer_id",
            "sales_channel_id",
            "order_number",
            "order_status",
            "fulfillment_status",
            "payment_status",
            "order_timestamp",
            "currency_code",
            "subtotal_amount",
            "discount_amount",
            "tax_amount",
            "shipping_amount",
            "total_amount",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="orders",
        bronze_schema=ORDER_BRONZE_SCHEMA,
        transform_func=transform_order,
        table_name="orders",
        merge_key="order_id"
    )
