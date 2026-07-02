def write_parquet_stream(
    dataframe,
    output_path,
    checkpoint_path,
):
    """
    Write a streaming DataFrame to Parquet format.

    Args:
        dataframe (DataFrame): The streaming DataFrame to write.
        output_path (str): The path where the Parquet files will be written.
        checkpoint_path (str): The path for storing checkpoint information.

    Returns:
        StreamingQuery: The streaming query object.
    """
    query = dataframe.writeStream \
        .format("parquet") \
        .option("path", output_path) \
        .option("checkpointLocation", checkpoint_path) \
        .outputMode("append") \
        .start()

    return query

def write_snowflake_batch(
    dataframe,
    sf_options,
    table_name,
):
    """
    Write a DataFrame to a Snowflake table.

    Args:
        dataframe (DataFrame): The DataFrame to write.
        sf_options (dict): A dictionary containing Snowflake connection options.
        table_name (str): The name of the Snowflake table to write to.

    Returns:
        None
    """
    dataframe.write \
        .format("snowflake") \
        .options(**sf_options) \
        .option("dbtable", table_name) \
        .mode("append") \
        .save()