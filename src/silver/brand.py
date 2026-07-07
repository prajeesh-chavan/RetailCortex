from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.brand_schema import BRAND_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_brand(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "brand_id",
            "brand_name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="brands",
        bronze_schema=BRAND_BRONZE_SCHEMA,
        transform_func=transform_brand,
        table_name="brands",
        merge_key="brand_id"
    )
