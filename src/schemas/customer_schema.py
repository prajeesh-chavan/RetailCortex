from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CUSTOMER_SCHEMA  = StructType([
    StructField("customer_id", StringType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
    StructField("date_of_birth", StringType(), True),
    StructField("customer_status", StringType()),
    StructField("customer_type", StringType()),
    StructField("registered_at", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("is_deleted", StringType()),
])

CUSTOMER_BRONZE_SCHEMA = StructType([
    StructField("customer_id", StringType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
    StructField("date_of_birth", StringType(), True),
    StructField("customer_status", StringType()),
    StructField("customer_type", StringType()),
    StructField("registered_at", StringType()),
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
