from pyspark.sql.functions import col, lower, to_timestamp

from src.schemas.warehouse_schema import WAREHOUSE_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_warehouse(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .withColumn("is_deleted", lower(col("is_deleted")).cast("boolean")) \
        .select(
            "warehouse_id",
            "warehouse_code",
            "warehouse_name",
            "address_id",
            "warehouse_status",
            "created_at",
            "updated_at",
            "is_deleted",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="warehouses",
        bronze_schema=WAREHOUSE_BRONZE_SCHEMA,
        transform_func=transform_warehouse,
        table_name="warehouses",
        merge_key="warehouse_id"
    )
