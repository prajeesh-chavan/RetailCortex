from pyspark.sql.functions import col, to_timestamp, lower
from src.schemas.vendor_schema import VENDOR_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_vendor(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("email", lower(col("email"))) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "vendor_id",
            "vendor_name",
            "legal_name",
            "vendor_code",
            "primary_contact_name",
            "email",
            "phone",
            "tax_registration_number",
            "vendor_status",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="vendors",
        bronze_schema=VENDOR_BRONZE_SCHEMA,
        transform_func=transform_vendor,
        table_name="vendors",
        merge_key="vendor_id"
    )
