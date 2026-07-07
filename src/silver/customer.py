from pyspark.sql.functions import col, concat_ws, lower, to_date, to_timestamp, upper

from src.schemas.customer_schema import CUSTOMER_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_customer(df):
    clean_df = df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("registered_at", to_timestamp("registered_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("date_of_birth", to_date("date_of_birth")) \
        .withColumn("email", lower(col("email"))) \
        .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name"))) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .withColumn("customer_status", upper(col("customer_status"))) \
        .withColumn("customer_type", upper(col("customer_type"))) \
        .withColumn("registered_date", to_date("registered_at"))

    return clean_df.select(
        "customer_id",
        "first_name",
        "last_name",
        "full_name",
        "email",
        "phone",
        "date_of_birth",
        "customer_status",
        "customer_type",
        "registered_date",
        "registered_at",
        "created_at",
        "updated_at",
        "is_deleted",
        "ingestion_timestamp",
    )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="customers",
        bronze_schema=CUSTOMER_BRONZE_SCHEMA,
        transform_func=transform_customer,
        table_name="customers",
        merge_key="customer_id"
    )
