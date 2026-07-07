from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

ORDER_STATUS_HISTORY_SCHEMA = StructType([
    StructField("order_status_history_id", StringType()),
    StructField("order_id", StringType()),
    StructField("status", StringType()),
    StructField("status_timestamp", StringType()),
    StructField("status_reason", StringType(), True),
    StructField("changed_by", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

ORDER_STATUS_HISTORY_BRONZE_SCHEMA = StructType([
    StructField("order_status_history_id", StringType()),
    StructField("order_id", StringType()),
    StructField("status", StringType()),
    StructField("status_timestamp", StringType()),
    StructField("status_reason", StringType(), True),
    StructField("changed_by", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
