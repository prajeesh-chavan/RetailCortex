from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

CUSTOMER_SCHEMA  = StructType([
    StructField("created_at", StringType()),
    StructField("customer_id", StringType()),
    StructField("customer_status", StringType()),
    StructField("email", StringType()),
    StructField("first_name", StringType()),
    StructField("is_deleted", StringType()),
    StructField("last_name", StringType()),
    StructField("phone", StringType()),
    StructField("registered_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("created_time", TimestampType())
])

CUSTOMER_BRONZE_SCHEMA = StructType([
    StructField("created_at", StringType()),
    StructField("customer_id", StringType()),
    StructField("customer_status", StringType()),
    StructField("email", StringType()),
    StructField("first_name", StringType()),
    StructField("is_deleted", StringType()),
    StructField("last_name", StringType()),
    StructField("phone", StringType()),
    StructField("registered_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("ingest_time", TimestampType()),
    StructField("ingest_date", DateType()),
    StructField("created_time", StringType()),
])