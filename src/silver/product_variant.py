from pyspark.sql.functions import col, to_timestamp, lower
from src.schemas.product_variant_schema import PRODUCT_VARIANT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_product_variant(df):
    return df \
        .withColumn("unit_price", col("unit_price").cast("decimal(12,2)")) \
        .withColumn("cost_price", col("cost_price").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "variant_id",
            "product_id",
            "sku",
            "barcode",
            "color",
            "size",
            "unit_price",
            "cost_price",
            "currency_code",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="product_variants",
        bronze_schema=PRODUCT_VARIANT_BRONZE_SCHEMA,
        transform_func=transform_product_variant,
        table_name="product_variants",
        merge_key="variant_id"
    )
