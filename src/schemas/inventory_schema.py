from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

INVENTORY_SCHEMA = StructType([
    StructField("inventory_id", StringType()),
    StructField("warehouse_id", StringType()),
    StructField("variant_id", StringType()),
    StructField("quantity_on_hand", StringType()),
    StructField("quantity_reserved", StringType()),
    StructField("reorder_level", StringType()),
    StructField("unit_cost", StringType()),
    StructField("last_stock_update_at", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

INVENTORY_BRONZE_SCHEMA = StructType([
    StructField("inventory_id", StringType()),
    StructField("warehouse_id", StringType()),
    StructField("variant_id", StringType()),
    StructField("quantity_on_hand", StringType()),
    StructField("quantity_reserved", StringType()),
    StructField("reorder_level", StringType()),
    StructField("unit_cost", StringType()),
    StructField("last_stock_update_at", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
