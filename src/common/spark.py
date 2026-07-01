from pyspark.sql import SparkSession

def create_spark_session(app_name: str) -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("Customer Stream")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
        )
        .config("spark.sql.streaming.schemaInference", "true")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    return spark