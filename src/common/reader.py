from pyspark.sql import SparkSession

def read_kafka_stream(
    spark: SparkSession,
    bootstrap_servers: str,
    topic: str
):
    """
    Read a streaming DataFrame from a Kafka topic.

    Args:
        spark (SparkSession): The Spark session.
        bootstrap_servers (str): The Kafka bootstrap servers.
        topic (str): The Kafka topic to read from.

    Returns:
        DataFrame: The streaming DataFrame read from the Kafka topic.
    """
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .load()

    return df

def read_parquet_batch(
    spark: SparkSession,
    path: str
):
    """
    Read a batch DataFrame from a Parquet file.

    Args:
        spark (SparkSession): The Spark session.
        path (str): The path to the Parquet file.

    Returns:
        DataFrame: The batch DataFrame read from the Parquet file.
    """
    df = spark.read.parquet(path)
    return df