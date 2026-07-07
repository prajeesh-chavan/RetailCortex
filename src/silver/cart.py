from pyspark.sql.functions import col, to_timestamp
from src.schemas.cart_schema import CART_BRONZE_SCHEMA
from src.silver.runner import run_silver_pipeline


def transform_cart(df):
    return df \
        .withColumn("created_at", to_timestamp("created_at")) \
        .withColumn("updated_at", to_timestamp("updated_at")) \
        .select(
            "cart_id",
            "customer_id",
            "session_id",
            "cart_status",
            "created_at",
            "updated_at",
            "ingestion_timestamp",
        )


if __name__ == "__main__":
    run_silver_pipeline(
        entity="carts",
        bronze_schema=CART_BRONZE_SCHEMA,
        transform_func=transform_cart,
        table_name="carts",
        merge_key="cart_id"
    )
