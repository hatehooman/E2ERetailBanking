# Spark utility functions
from pyspark.sql import SparkSession

def create_spark_session(app_name='Spark Application', config=None):
    """
    Create a Spark session
    :param app_name: Name of the Spark application
    :param config: Dictionary containing Spark configuration parameters
    :return: SparkSession object
    """
    builder = SparkSession.builder.appName(app_name)
    
    if config:
        for key, value in config.items():
            builder = builder.config(key, value)
    
    return builder.getOrCreate()

def read_from_snowflake(spark, config, query):
    """
    Read data from Snowflake using Spark
    :param spark: SparkSession object
    :param config: Dictionary containing Snowflake connection parameters
    :param query: SQL query to execute
    :return: DataFrame with the query result
    """
    return spark.read \
        .format("net.snowflake.spark.snowflake") \
        .options(**config) \
        .option("query", query) \
        .load()

def write_to_snowflake(df, config, table_name, mode="overwrite"):
    """
    Write data to Snowflake using Spark
    :param df: DataFrame to write
    :param config: Dictionary containing Snowflake connection parameters
    :param table_name: Target table name in Snowflake
    :param mode: Write mode (default is overwrite)
    """
    df.write \
        .format("net.snowflake.spark.snowflake") \
        .options(**config) \
        .option("dbtable", table_name) \
        .mode(mode) \
        .save()
