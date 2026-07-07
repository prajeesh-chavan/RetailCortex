from pyspark.sql.functions import col, to_timestamp, lower
from src.schemas.product_schema import PRODUCT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_product(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "product_id",
            "vendor_id",
            "brand_id",
            "category_id",
            "product_name",
            "description",
            "product_status",
            "tax_class",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="products",
        bronze_schema=PRODUCT_BRONZE_SCHEMA,
        transform_func=transform_product,
        table_name="products",
        merge_key="product_id"
    )
