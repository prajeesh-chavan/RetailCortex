from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CARRIER_SCHEMA = StructType([
    StructField("carrier_id", StringType()),
    StructField("carrier_name", StringType()),
    StructField("carrier_code", StringType()),
    StructField("tracking_url_template", StringType()),
    StructField("is_active", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

CARRIER_BRONZE_SCHEMA = StructType([
    StructField("carrier_id", StringType()),
    StructField("carrier_name", StringType()),
    StructField("carrier_code", StringType()),
    StructField("tracking_url_template", StringType()),
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
