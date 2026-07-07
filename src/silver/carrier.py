from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.carrier_schema import CARRIER_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_carrier(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "carrier_id",
            "carrier_name",
            "carrier_code",
            "tracking_url_template",
            "is_active",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="carriers",
        bronze_schema=CARRIER_BRONZE_SCHEMA,
        transform_func=transform_carrier,
        table_name="carriers",
        merge_key="carrier_id"
    )
