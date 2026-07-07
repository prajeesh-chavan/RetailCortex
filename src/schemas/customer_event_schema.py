from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CUSTOMER_EVENT_SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("event_type", StringType()),
    StructField("event_data", StringType(), True),
    StructField("page_url", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_timestamp", StringType()),
    StructField("created_at", StringType()),
])

CUSTOMER_EVENT_BRONZE_SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("event_type", StringType()),
    StructField("event_data", StringType(), True),
    StructField("page_url", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_timestamp", StringType()),
    StructField("created_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
