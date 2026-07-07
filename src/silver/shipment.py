from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.shipment_schema import SHIPMENT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_shipment(df):
    return df \
        .withColumn("shipped_at", to_timestamp("shipped_at")) \
        .withColumn("estimated_delivery_at", to_timestamp("estimated_delivery_at")) \
        .withColumn("delivered_at", to_timestamp("delivered_at")) \
        .withColumn("shipping_charge", col("shipping_charge").cast("decimal(12,2)")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "shipment_id",
            "order_id",
            "carrier_id",
            "warehouse_id",
            "shipment_number",
            "tracking_number",
            "shipment_status",
            "shipped_at",
            "estimated_delivery_at",
            "delivered_at",
            "shipping_charge",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="shipments",
        bronze_schema=SHIPMENT_BRONZE_SCHEMA,
        transform_func=transform_shipment,
        table_name="shipments",
        merge_key="shipment_id"
    )
