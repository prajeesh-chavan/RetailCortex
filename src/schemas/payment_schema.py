from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

PAYMENT_SCHEMA = StructType([
    StructField("payment_id", StringType()),
    StructField("order_id", StringType()),
    StructField("payment_provider", StringType()),
    StructField("provider_payment_reference", StringType()),
    StructField("payment_method", StringType()),
    StructField("payment_status", StringType()),
    StructField("amount", StringType()),
    StructField("currency_code", StringType()),
    StructField("failure_code", StringType(), True),
    StructField("failure_reason", StringType(), True),
    StructField("processed_at", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

PAYMENT_BRONZE_SCHEMA = StructType([
    StructField("payment_id", StringType()),
    StructField("order_id", StringType()),
    StructField("payment_provider", StringType()),
    StructField("provider_payment_reference", StringType()),
    StructField("payment_method", StringType()),
    StructField("payment_status", StringType()),
    StructField("amount", StringType()),
    StructField("currency_code", StringType()),
    StructField("failure_code", StringType(), True),
    StructField("failure_reason", StringType(), True),
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
