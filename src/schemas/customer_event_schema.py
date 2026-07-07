from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

CUSTOMER_EVENT_SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("customer_id", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_type", StringType()),
    StructField("event_timestamp", StringType()),
    StructField("page_url", StringType(), True),
    StructField("referrer_url", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("variant_id", StringType(), True),
    StructField("event_metadata", StringType(), True),
    StructField("created_at", StringType()),
])

CUSTOMER_EVENT_BRONZE_SCHEMA = StructType([
    StructField("event_id", StringType()),
    StructField("customer_id", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_type", StringType()),
    StructField("event_timestamp", StringType()),
    StructField("page_url", StringType(), True),
    StructField("referrer_url", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("variant_id", StringType(), True),
    StructField("event_metadata", StringType(), True),
    StructField("created_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
