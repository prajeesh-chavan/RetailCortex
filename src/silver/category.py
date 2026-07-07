from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.category_schema import CATEGORY_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_category(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "category_id",
            "category_name",
            "parent_category_id",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="categories",
        bronze_schema=CATEGORY_BRONZE_SCHEMA,
        transform_func=transform_category,
        table_name="categories",
        merge_key="category_id"
    )
