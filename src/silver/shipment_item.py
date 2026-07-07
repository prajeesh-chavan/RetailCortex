from pyspark.sql.functions import col, to_timestamp

from src.schemas.shipment_item_schema import SHIPMENT_ITEM_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_shipment_item(df):
    return df \
        .withColumn("quantity_shipped", col("quantity_shipped").cast("int")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "shipment_item_id",
            "shipment_id",
            "order_item_id",
            "quantity_shipped",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="shipment_items",
        bronze_schema=SHIPMENT_ITEM_BRONZE_SCHEMA,
        transform_func=transform_shipment_item,
        table_name="shipment_items",
        merge_key="shipment_item_id"
    )
