from pyspark.ml.classification import MultilayerPerceptronClassifier, LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, LinearSVC, GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from spark_transformer import LoanDataTransformer
from spark_session import create_spark_session
from pyspark.sql import SparkSession

class ModelTrainer:
    def __init__(self, spark_session, transformer, train_data):

        self.input_size = len(train_data.select("features").first()[0])
        self.num_classes = train_data.select("loan_status_idx").distinct().count()
        self.spark = spark_session
        self.transformer = transformer
        self.classifiers = {
            "LogisticRegression": LogisticRegression(labelCol="loan_status_idx", featuresCol="features"),
            "DecisionTreeClassifier": DecisionTreeClassifier(labelCol="loan_status_idx", featuresCol="features"),
            "RandomForestClassifier": RandomForestClassifier(labelCol="loan_status_idx", featuresCol="features"),
            "MultilayerPerceptronClassifier" : MultilayerPerceptronClassifier(labelCol="loan_status_idx", featuresCol="features", layers=[self.input_size, 5, 4, self.num_classes])
        }

    def train_model(self, model, train_data, test_data):
        trained_model = model.fit(train_data)
        predictions = trained_model.transform(test_data)
        evaluator = MulticlassClassificationEvaluator(labelCol="loan_status_idx", predictionCol="prediction")
        
        accuracy = evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"})
        f1 = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
        weightedPrecision = evaluator.evaluate(predictions, {evaluator.metricName: "weightedPrecision"})
        weightedRecall = evaluator.evaluate(predictions, {evaluator.metricName: "weightedRecall"})
        
        # Print evaluation metrics
        print(f"Model: {type(model).__name__}")
        print(f"Accuracy = {accuracy}")
        print(f"F1 score = {f1}")
        print(f"Weighted Precision = {weightedPrecision}")
        print(f"Weighted Recall = {weightedRecall}")
        print()

    def train_models(self, train_data, test_data):
        for name, model in self.classifiers.items():
            print(f"Training {name}...")
            self.train_model(model, train_data, test_data)

if __name__ == "__main__":
    spark = create_spark_session('Loan Approved')

    transformer = LoanDataTransformer(spark)
    trans_file_path = "Dataset/Retail-Banking-Demo-Data/completedtrans.csv"
    loan_file_path = "Dataset/Retail-Banking-Demo-Data/completedloan.csv"
    

    # Read CSV with explicitly specified schema
    trans_df = spark.read.option("header", "true").csv(trans_file_path)

    # Read the completedtrans.csv and completedloan.csv files into DataFrames
    loan_df = spark.read.option("header", "true").csv(loan_file_path)

    trans_df.show(5)
    loan_df.show(5)
    # Load and preprocess data
    transformer.load_data(loan_df, trans_df)
    transformer.preprocess_data()
    transformed_data = transformer.get_assembled_data()

    print(transformed_data.columns)
    

    # Split data into train and test sets
    train_data, test_data = transformed_data.randomSplit([0.8, 0.2], seed=123)
    # Initialize trainer
    trainer = ModelTrainer(spark, transformer, train_data)
    # Train models
    trainer.train_models(train_data, test_data)

    # Stop Spark session
    spark.stop()
