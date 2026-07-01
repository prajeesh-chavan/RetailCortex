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