from pyspark.sql.functions import col, to_timestamp

from src.schemas.order_item_schema import ORDER_ITEM_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_order_item(df):
    return df \
        .withColumn("quantity_ordered", col("quantity_ordered").cast("int")) \
        .withColumn("quantity_cancelled", col("quantity_cancelled").cast("int")) \
        .withColumn("quantity_fulfilled", col("quantity_fulfilled").cast("int")) \
        .withColumn("quantity_returned", col("quantity_returned").cast("int")) \
        .withColumn("unit_price", col("unit_price").cast("decimal(12,2)")) \
        .withColumn("line_discount_amount", col("line_discount_amount").cast("decimal(12,2)")) \
        .withColumn("line_tax_amount", col("line_tax_amount").cast("decimal(12,2)")) \
        .withColumn("line_shipping_amount", col("line_shipping_amount").cast("decimal(12,2)")) \
        .withColumn("line_total_amount", col("line_total_amount").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "order_item_id",
            "order_id",
            "variant_id",
            "vendor_id",
            "product_name_snapshot",
            "sku_snapshot",
            "quantity_ordered",
            "quantity_cancelled",
            "quantity_fulfilled",
            "quantity_returned",
            "unit_price",
            "line_discount_amount",
            "line_tax_amount",
            "line_shipping_amount",
            "line_total_amount",
            "currency_code",
            "item_status",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="order_items",
        bronze_schema=ORDER_ITEM_BRONZE_SCHEMA,
        transform_func=transform_order_item,
        table_name="order_items",
        merge_key="order_item_id"
    )
