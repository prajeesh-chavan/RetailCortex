from pyspark.sql.functions import col, to_timestamp

from src.schemas.inventory_movement_schema import INVENTORY_MOVEMENT_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_inventory_movement(df):
    return df \
        .withColumn("movement_quantity", col("movement_quantity").cast("int")) \
        .withColumn("movement_timestamp", to_timestamp("movement_timestamp")) \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "movement_id",
            "inventory_id",
            "movement_type",
            "movement_quantity",
            "reference_type",
            "reference_id",
            "movement_timestamp",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="inventory_movements",
        bronze_schema=INVENTORY_MOVEMENT_BRONZE_SCHEMA,
        transform_func=transform_inventory_movement,
        table_name="inventory_movements",
        merge_key="movement_id"
    )
