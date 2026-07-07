from pyspark.sql.functions import col, to_timestamp
from src.schemas.customer_event_schema import CUSTOMER_EVENT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_customer_event(df):
    return df \
        .withColumn("event_timestamp", to_timestamp("event_timestamp")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .select(
            "event_id",
            "customer_id",
            "session_id",
            "event_type",
            "event_timestamp",
            "page_url",
            "referrer_url",
            "product_id",
            "variant_id",
            "event_metadata",
            "created_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="customer_events",
        bronze_schema=CUSTOMER_EVENT_BRONZE_SCHEMA,
        transform_func=transform_customer_event,
        table_name="customer_events",
        merge_key="event_id"
    )
