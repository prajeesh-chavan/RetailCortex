from pyspark.sql.functions import col, to_timestamp, to_date, lower
from src.schemas.promotion_schema import PROMOTION_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_promotion(df):
    return df \
        .withColumn("discount_percentage", col("discount_percentage").cast("decimal(10,2)")) \
        .withColumn("discount_amount", col("discount_amount").cast("decimal(12,2)")) \
        .withColumn("minimum_purchase_amount", col("minimum_purchase_amount").cast("decimal(12,2)")) \
        .withColumn("maximum_discount_cap", col("maximum_discount_cap").cast("decimal(12,2)")) \
        .withColumn("usage_limit", col("usage_limit").cast("int")) \
        .withColumn("usage_count_per_customer", col("usage_count_per_customer").cast("int")) \
        .withColumn("valid_from", to_timestamp("valid_from")) \
        .withColumn("valid_until", to_timestamp("valid_until")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "promotion_id",
            "promotion_name",
            "promotion_code",
            "promotion_type",
            "discount_percentage",
            "discount_amount",
            "minimum_purchase_amount",
            "maximum_discount_cap",
            "applicable_to",
            "applicable_entity_id",
            "usage_limit",
            "usage_count_per_customer",
            "valid_from",
            "valid_until",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="promotions",
        bronze_schema=PROMOTION_BRONZE_SCHEMA,
        transform_func=transform_promotion,
        table_name="promotions",
        merge_key="promotion_id"
    )
