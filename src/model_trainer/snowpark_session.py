from pyspark import SparkConf
from pyspark.sql import SparkSession


def create_spark_session(app_name: str, local_mode: bool = False) -> SparkSession:
    if local_mode:
        print("Local mode started")
        conf = (SparkConf().set("spark.driver.memory", "8g")
                            .set("spark.sql.session.timeZone", "UTC"))
        spark_session = SparkSession.builder \
                                    .master("local[*]") \
                                    .config(conf=conf) \
                                    .appName(app_name) \
                                    .getOrCreate()
    else:
        print("Cluster started")
        spark_session = SparkSession.builder \
                                    .appName(app_name) \
                                    .getOrCreate()
    return spark_session

