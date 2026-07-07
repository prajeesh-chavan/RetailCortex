from pyspark.sql.types import DateType, StructField, StructType, StringType, TimestampType

RETURN_ITEM_SCHEMA = StructType([
    StructField("return_item_id", StringType()),
    StructField("return_id", StringType()),
    StructField("order_item_id", StringType()),
    StructField("quantity_returned", StringType()),
    StructField("return_reason", StringType(), True),
    StructField("item_condition", StringType()),
    StructField("disposition", StringType()),
    StructField("refund_amount", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

RETURN_ITEM_BRONZE_SCHEMA = StructType([
    StructField("return_item_id", StringType()),
    StructField("return_id", StringType()),
    StructField("order_item_id", StringType()),
    StructField("quantity_returned", StringType()),
    StructField("return_reason", StringType(), True),
    StructField("item_condition", StringType()),
    StructField("disposition", StringType()),
    StructField("refund_amount", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
