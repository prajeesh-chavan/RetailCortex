from pyspark.sql.functions import to_timestamp

from src.schemas.order_address_schema import ORDER_ADDRESS_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_order_address(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "order_address_id",
            "order_id",
            "customer_address_id",
            "address_type",
            "recipient_name",
            "recipient_phone",
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
        entity="order_addresses",
        bronze_schema=ORDER_ADDRESS_BRONZE_SCHEMA,
        transform_func=transform_order_address,
        table_name="order_addresses",
        merge_key="order_address_id"
    )
