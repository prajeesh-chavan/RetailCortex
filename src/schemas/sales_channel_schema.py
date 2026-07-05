from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

SALES_CHANNEL_SCHEMA = StructType([
    StructField("channel_id", StringType()),
    StructField("channel_name", StringType()),
    StructField("channel_type", StringType()),
    StructField("is_active", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

SALES_CHANNEL_BRONZE_SCHEMA = StructType([
    StructField("channel_id", StringType()),
    StructField("channel_name", StringType()),
    StructField("channel_type", StringType()),
    StructField("is_active", StringType()),
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
