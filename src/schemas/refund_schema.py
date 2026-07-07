from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

REFUND_SCHEMA = StructType([
    StructField("refund_id", StringType()),
    StructField("order_id", StringType()),
    StructField("payment_id", StringType()),
    StructField("refund_reference", StringType()),
    StructField("refund_status", StringType()),
    StructField("refund_reason", StringType(), True),
    StructField("refund_amount", StringType()),
    StructField("currency_code", StringType()),
    StructField("processed_at", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

REFUND_BRONZE_SCHEMA = StructType([
    StructField("refund_id", StringType()),
    StructField("order_id", StringType()),
    StructField("payment_id", StringType()),
    StructField("refund_reference", StringType()),
    StructField("refund_status", StringType()),
    StructField("refund_reason", StringType(), True),
    StructField("refund_amount", StringType()),
    StructField("currency_code", StringType()),
    StructField("processed_at", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
