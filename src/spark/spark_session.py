from pyspark import SparkConf
from pyspark.sql import SparkSession
import shutil
import tempfile
import os
import pickle

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
        conf = (SparkConf().set("spark.sql.session.timeZone", "UTC"))
        spark_session = SparkSession.builder \
                                    .config(conf=conf) \
                                    .appName(app_name) \
                                    .getOrCreate()
    return spark_session

# if __name__ == "__main__":
#     spark = create_spark_session("Test")
#     temp_dir = tempfile.mkdtemp()

#     file_loc = "Dataset/Retail-Banking-Demo-Data"
#     paths = [os.path.join(file_loc, filename) for filename in [
#         "completedacct.csv",
#         "completedcard.csv",
#         "completedclient.csv",
#         "completeddisposition.csv",
#         "completeddistrict.csv",
#         "completedloan.csv",
#         "completedorder.csv",
#         "completedtrans.csv",
#         "CRM Call Center Logs.csv",
#         "CRM Events.csv",
#         "CRM Reviews.csv"
#     ]]

#     dfs = {}  # Dictionary to store DataFrames

#     try:
#         for p in paths:
#             filename = os.path.basename(p)
#             df = spark.read.option("header", True).csv(p)
#             print(f"Showing first 5 records from {filename}:")
#             df.show(5)
#             dfs[filename] = df  # Store DataFrame in the dictionary
#         print(dfs.items())

#         for filename, df in dfs.items():
#             print(f"DataFrame '{filename}':")
#             df.show(5) 


#     finally:
#         spark.stop()
#         try:
#             shutil.rmtree(temp_dir)
#         except FileNotFoundError:
#             print(f"Temporary directory {temp_dir} already deleted.")
#         except Exception as e:
#             print(f"Error while deleting temporary directory {temp_dir}: {e}")

