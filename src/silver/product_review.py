from pyspark.sql.functions import col, to_timestamp, lower
from src.schemas.product_review_schema import PRODUCT_REVIEW_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_product_review(df):
    return df \
        .withColumn("rating", col("rating").cast("int")) \
        .withColumn("is_verified_purchase", lower(col("is_verified_purchase")).cast("boolean")) \
        .withColumn("is_approved", lower(col("is_approved")).cast("boolean")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "review_id",
            "product_id",
            "customer_id",
            "order_id",
            "rating",
            "review_title",
            "review_body",
            "is_verified_purchase",
            "is_approved",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="product_reviews",
        bronze_schema=PRODUCT_REVIEW_BRONZE_SCHEMA,
        transform_func=transform_product_review,
        table_name="product_reviews",
        merge_key="review_id"
    )
