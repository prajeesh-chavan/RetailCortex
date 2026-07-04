from pyspark.sql.functions import col, to_timestamp, lower, concat_ws, upper
from src.schemas.customer_schema import CUSTOMER_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_customer(df):
    clean_df = df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("registered_at", to_timestamp("registered_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("ingest_time", to_timestamp("ingest_time")) \
        .withColumn("email", lower(col("email"))) \
        .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name"))) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .withColumn("created_time", to_timestamp("created_time")) \
        .withColumn("customer_status", upper(col("customer_status")))

    return clean_df.select(
        "customer_id",
        "full_name",
        "email",
        "phone",
        "customer_status",
        "registered_at",
        "ingest_time",
        "is_deleted",
        "created_at",
        "updated_at"
    )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="customers",
        bronze_schema=CUSTOMER_BRONZE_SCHEMA,
        transform_func=transform_customer,
        table_name="customers",
        merge_key="customer_id"
    )