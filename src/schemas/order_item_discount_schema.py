from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

ORDER_ITEM_DISCOUNT_SCHEMA = StructType([
    StructField("order_item_discount_id", StringType()),
    StructField("order_item_id", StringType()),
    StructField("promotion_id", StringType(), True),
    StructField("discount_type", StringType()),
    StructField("discount_name", StringType()),
    StructField("discount_amount", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
])

ORDER_ITEM_DISCOUNT_BRONZE_SCHEMA = StructType([
    StructField("order_item_discount_id", StringType()),
    StructField("order_item_id", StringType()),
    StructField("promotion_id", StringType(), True),
    StructField("discount_type", StringType()),
    StructField("discount_name", StringType()),
    StructField("discount_amount", StringType()),
    StructField("created_at", StringType()),
    StructField("updated_at", StringType()),
    StructField("kafka_key", StringType()),
    StructField("kafka_topic", StringType()),
    StructField("kafka_partition", StringType()),
    StructField("kafka_offset", StringType()),
    StructField("ingestion_timestamp", TimestampType()),
    StructField("ingestion_date", DateType()),
])
