from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CUSTOMER_ADDRESS_SCHEMA = StructType([
    StructField("customer_address_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("address_id", StringType()),
    StructField("address_type", StringType()),
    StructField("is_default", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

CUSTOMER_ADDRESS_BRONZE_SCHEMA = StructType([
    StructField("customer_address_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("address_id", StringType()),
    StructField("address_type", StringType()),
    StructField("is_default", StringType()),
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
