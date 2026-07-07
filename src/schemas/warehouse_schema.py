from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

WAREHOUSE_SCHEMA = StructType([
    StructField("warehouse_id", StringType()),
    StructField("warehouse_code", StringType()),
    StructField("warehouse_name", StringType()),
    StructField("address_id", StringType()),
    StructField("warehouse_status", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

WAREHOUSE_BRONZE_SCHEMA = StructType([
    StructField("warehouse_id", StringType()),
    StructField("warehouse_code", StringType()),
    StructField("warehouse_name", StringType()),
    StructField("address_id", StringType()),
    StructField("warehouse_status", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
