from pyspark.sql.functions import col, to_timestamp
from src.schemas.inventory_schema import INVENTORY_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_inventory(df):
    return df \
        .withColumn("quantity_on_hand", col("quantity_on_hand").cast("int")) \
        .withColumn("quantity_reserved", col("quantity_reserved").cast("int")) \
        .withColumn("reorder_level", col("reorder_level").cast("int")) \
        .withColumn("unit_cost", col("unit_cost").cast("decimal(12,2)")) \
        .withColumn("last_stock_update_at", to_timestamp("last_stock_update_at")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "inventory_id",
            "warehouse_id",
            "variant_id",
            "quantity_on_hand",
            "quantity_reserved",
            "reorder_level",
            "unit_cost",
            "last_stock_update_at",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="inventory",
        bronze_schema=INVENTORY_BRONZE_SCHEMA,
        transform_func=transform_inventory,
        table_name="inventory",
        merge_key="inventory_id"
    )
