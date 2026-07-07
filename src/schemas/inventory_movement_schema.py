from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

INVENTORY_MOVEMENT_SCHEMA = StructType([
    StructField("movement_id", StringType()),
    StructField("inventory_id", StringType()),
    StructField("movement_type", StringType()),
    StructField("movement_quantity", StringType()),
    StructField("reference_type", StringType()),
    StructField("reference_id", StringType()),
    StructField("movement_timestamp", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

INVENTORY_MOVEMENT_BRONZE_SCHEMA = StructType([
    StructField("movement_id", StringType()),
    StructField("inventory_id", StringType()),
    StructField("movement_type", StringType()),
    StructField("movement_quantity", StringType()),
    StructField("reference_type", StringType()),
    StructField("reference_id", StringType()),
    StructField("movement_timestamp", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
