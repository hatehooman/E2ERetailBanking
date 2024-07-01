from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.sql.functions import col

class LoanDataTransformer:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.assembler = None

    def load_data(self, loan_df, trans_df):
        # Rename columns in loan_df
        loan_df = loan_df.withColumnRenamed("amount", "loan_amount") \
                         .withColumnRenamed("duration", "loan_duration") \
                         .withColumnRenamed("payments", "loan_payments") \
                         .withColumnRenamed("status", "loan_status") \
                         .withColumnRenamed("year", "loan_year") \
                         .withColumnRenamed("month", "loan_month") \
                         .withColumnRenamed("day", "loan_day") \
                         .withColumnRenamed("fulldate", "loan_fulldate") \
                         .withColumnRenamed("location", "loan_location") \
                         .withColumnRenamed("purpose", "loan_purpose")

        # Rename columns in trans_df
        trans_df = trans_df.withColumnRenamed("type", "trans_type") \
                           .withColumnRenamed("operation", "trans_operation") \
                           .withColumnRenamed("amount", "trans_amount") \
                           .withColumnRenamed("balance", "trans_balance") \
                           .withColumnRenamed("k_symbol", "trans_k_symbol") \
                           .withColumnRenamed("bank", "trans_bank") \
                           .withColumnRenamed("account", "trans_account") \
                           .withColumnRenamed("year", "trans_year") \
                           .withColumnRenamed("month", "trans_month") \
                           .withColumnRenamed("day", "trans_day") \
                           .withColumnRenamed("fulldate", "trans_fulldate") \
                           .withColumnRenamed("fulltime", "trans_fulltime") \
                           .withColumnRenamed("fulldatewithtime", "trans_fulldatewithtime")

        # Join loan_df and trans_df
        self.joined_df = loan_df.join(trans_df, on='account_id', how='inner')

    def preprocess_data(self):
        # Convert columns to double type
        columns_to_convert = ['loan_amount', 'loan_duration', 'loan_payments', 
                              'loan_year', 'loan_month', 'loan_day', 
                              'trans_amount', 'trans_balance']
        
        for col_name in columns_to_convert:
            self.joined_df = self.joined_df.withColumn(col_name, col(col_name).cast("double"))

        # Index categorical columns
        indexers = [
            StringIndexer(inputCol="loan_status", outputCol="loan_status_idx", handleInvalid="keep"),
            StringIndexer(inputCol="loan_purpose", outputCol="loan_purpose_idx", handleInvalid="keep"),
            StringIndexer(inputCol="trans_type", outputCol="trans_type_idx", handleInvalid="keep"),
            StringIndexer(inputCol="trans_operation", outputCol="trans_operation_idx", handleInvalid="keep"),
            StringIndexer(inputCol="trans_k_symbol", outputCol="trans_k_symbol_idx", handleInvalid="keep"),
            StringIndexer(inputCol="trans_bank", outputCol="trans_bank_idx", handleInvalid="keep")
        ]

        for indexer in indexers:
            self.joined_df = indexer.fit(self.joined_df).transform(self.joined_df)

        # Assemble features
        feature_columns = ['loan_amount', 'loan_duration', 'loan_payments', 
                   'loan_year', 'loan_month', 'loan_day', 
                   'trans_type_idx', 'trans_operation_idx', 'trans_amount', 'trans_balance',
                   'trans_k_symbol_idx', 'trans_bank_idx']

        self.assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
        self.assembled_data = self.assembler.transform(self.joined_df)

    def transform_data(self, data):
        return self.assembler.transform(data)

    def get_assembled_data(self):
        return self.assembled_data

# if __name__ == "__main__":
#     # Initialize Spark session
#     spark = SparkSession.builder \
#                         .appName("Loan Classification Transformer") \
#                         .getOrCreate()

#     # Example usage
#     transformer = LoanDataTransformer(spark)
#     trans_file_path = "Dataset/Retail-Banking-Demo-Data/completedtrans.csv"
#     loan_file_path = "Dataset/Retail-Banking-Demo-Data/completedloan.csv"

#     # Read the completedtrans.csv and completedloan.csv files into DataFrames
#     trans_df = spark.read.option("header", "true").csv(trans_file_path)
#     loan_df = spark.read.option("header", "true").csv(loan_file_path)
#     # Load and preprocess data
#     transformer.load_data(loan_df, trans_df)
#     transformer.preprocess_data()

#     # Get transformed data
#     transformed_data = transformer.get_assembled_data()
#     print(transformed_data.columns)
#     # Stop Spark session
#     spark.stop()
