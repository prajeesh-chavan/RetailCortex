from pyspark.sql import SparkSession

def create_spark_session(app_name: str) -> SparkSession:
    spark = (
        SparkSession.builder
        .appName(app_name)
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
            "net.snowflake:spark-snowflake_2.12:3.1.9",
            "net.snowflake:snowflake-jdbc:3.24.2"
        ])
    )
        .config("spark.sql.streaming.schemaInference", "true")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark