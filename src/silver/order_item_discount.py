from pyspark.sql.functions import col, to_timestamp

from src.schemas.order_item_discount_schema import ORDER_ITEM_DISCOUNT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_order_item_discount(df):
    return df \
        .withColumn("discount_amount", col("discount_amount").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "order_item_discount_id",
            "order_item_id",
            "promotion_id",
            "discount_type",
            "discount_name",
            "discount_amount",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="order_item_discounts",
        bronze_schema=ORDER_ITEM_DISCOUNT_BRONZE_SCHEMA,
        transform_func=transform_order_item_discount,
        table_name="order_item_discounts",
        merge_key="order_item_discount_id"
    )
