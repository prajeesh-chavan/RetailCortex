from pyspark.sql.functions import col, to_timestamp

from src.schemas.cart_item_schema import CART_ITEM_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_cart_item(df):
    return df \
        .withColumn("quantity", col("quantity").cast("int")) \
        .withColumn("unit_price", col("unit_price").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "cart_item_id",
            "cart_id",
            "variant_id",
            "quantity",
            "unit_price",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="cart_items",
        bronze_schema=CART_ITEM_BRONZE_SCHEMA,
        transform_func=transform_cart_item,
        table_name="cart_items",
        merge_key="cart_item_id"
    )
