from pyspark.sql.functions import col, to_timestamp

from src.schemas.return_item_schema import RETURN_ITEM_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_return_item(df):
    return df \
        .withColumn("quantity_returned", col("quantity_returned").cast("int")) \
        .withColumn("refund_amount", col("refund_amount").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "return_item_id",
            "return_id",
            "order_item_id",
            "quantity_returned",
            "return_reason",
            "item_condition",
            "disposition",
            "refund_amount",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="return_items",
        bronze_schema=RETURN_ITEM_BRONZE_SCHEMA,
        transform_func=transform_return_item,
        table_name="return_items",
        merge_key="return_item_id"
    )
