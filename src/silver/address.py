from pyspark.sql.functions import col, to_timestamp
from src.schemas.address_schema import ADDRESS_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_address(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "address_id",
            "address_line_1",
            "address_line_2",
            "locality",
            "administrative_area",
            "postal_code",
            "country_code",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="addresses",
        bronze_schema=ADDRESS_BRONZE_SCHEMA,
        transform_func=transform_address,
        table_name="addresses",
        merge_key="address_id"
    )
