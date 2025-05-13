# -*- coding: utf-8 -*-

# Snowpark imports
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col, when, count, dense_rank
from snowflake.snowpark.window import Window
from snowflake.ml.modeling.xgboost import XGBClassifier
from snowflake.ml.utils.connection_params import SnowflakeLoginOptions
from snowflake.ml.modeling.preprocessing import StandardScaler
from snowflake.ml.modeling.impute import SimpleImputer
from snowflake.ml.modeling.pipeline import Pipeline
from snowflake.ml.modeling.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from snowflake.ml.registry import Registry

# Visualization and Data Handling
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import random
import warnings

# Connection parameters
connection_param = {
    'user': 'trucnmt',
    'password': 'Thanhtruc28!',
    'account': 'WK90181.ap-southeast-1',
    'warehouse': 'ETL_WH',
    'database': 'STAGING',
    'schema': 'CLEAN',
    'role': 'TRANSFORM_ROLE'
}

session = Session.builder.configs(connection_param).create()

# Load tables
trans_df = session.table('C_TRANSACTION')
loan_df = session.table('LOAN')
account_df = session.table('ACCOUNT')
order_df = session.table('C_ORDER')

# Join tables
joined_df = loan_df.join(trans_df, 'account_id').join(order_df, 'account_id')
joined_df = joined_df.withColumn("loan_status", when(col("loan_status").isin("C", "A"), 0).otherwise(1))

# Encode categorical features
categorical_columns = ['loan_purpose', 'trans_type', 'OPERATION_TYPE', 'trans_k_symbol', 'trans_bank', 'order_k_symbol', 'order_bank_to']
for column in categorical_columns:
    window_spec = Window.order_by(col(column))
    joined_df = joined_df.with_column(f"{column}_idx", dense_rank().over(window_spec).cast("float"))

# Balance dataset
label_col = "LOAN_STATUS"
label_distribution = joined_df.group_by(label_col).agg(count("*").alias("count"))
max_count = label_distribution.select("count").agg({"count": "max"}).collect()[0][0]
schema = joined_df.schema
balanced_df = session.create_dataframe([], schema=schema)

for row in label_distribution.collect():
    label = row[label_col]
    count1 = row["COUNT"]
    subset_df = joined_df.filter(col(label_col) == label)
    if count1 < max_count:
        additional_count = max_count - count1
        oversampled_df = subset_df
        while oversampled_df.count() < additional_count:
            oversampled_df = oversampled_df.union_all(subset_df)
        oversampled_df = oversampled_df.limit(additional_count)
        balanced_subset = subset_df.union_all(oversampled_df)
    else:
        balanced_subset = subset_df
    balanced_df = balanced_df.union_all(balanced_subset)

joined_df = balanced_df

# Train-test split
joined_df_pandas = joined_df.to_pandas()
joined_df_pandas['random_val'] = [random.random() for _ in range(len(joined_df_pandas))]
train_df = joined_df_pandas[joined_df_pandas['random_val'] < 0.7].reset_index(drop=True)
val_df = joined_df_pandas[joined_df_pandas['random_val'] >= 0.7].reset_index(drop=True)

# Drop unused column and keep features/labels
feature_cols = ['LOAN_AMOUNT', 'LOAN_DURATION', 'LOAN_PAYMENTS', 'LOAN_YEAR', 'LOAN_MONTH', 'LOAN_DAY',
                'TRANS_TYPE_IDX', 'OPERATION_TYPE_IDX', 'TRANS_AMOUNT', 'TRANS_BALANCE',
                'TRANS_K_SYMBOL_IDX', 'TRANS_BANK_IDX', 'ORDER_BANK_TO_IDX', 'ORDER_K_SYMBOL_IDX']
feature_cols_1 = feature_cols + ['LOAN_STATUS']
train_df = train_df.drop(columns=['random_val'])[feature_cols_1]
val_df = val_df.drop(columns=['random_val'])[feature_cols_1]
train_data = session.create_dataframe(train_df)
val_data = session.create_dataframe(val_df)

# Model registry
reg = Registry(session=session, database_name="STAGING", schema_name="CLEAN")

def registry_model(model):
    reg.log_model(
        model,
        model_name=f"{type(model).__name__}",
        version_name="v2_fulldata",
        conda_dependencies=["scikit-learn"],
        comment="OK",
        metrics={"score": model.score(val_data)},
        sample_input_data=joined_df_pandas[feature_cols],
        options={'relax_version': False}
    )
    print("Model registered")

# Train multiple models
from snowflake.ml.modeling.ensemble import RandomForestClassifier, GradientBoostingClassifier
from snowflake.ml.modeling.tree import DecisionTreeClassifier
from snowflake.ml.modeling.linear_model import RidgeClassifier
from snowflake.ml.modeling.neighbors import KNeighborsClassifier
from snowflake.ml.modeling.linear_model import LogisticRegression

models = [
    LogisticRegression(input_cols=feature_cols, label_cols='LOAN_STATUS', max_iter=10000, C=0.01),
    DecisionTreeClassifier(input_cols=feature_cols, label_cols='LOAN_STATUS', max_depth=10, min_samples_split=20, min_samples_leaf=5),
    RandomForestClassifier(input_cols=feature_cols, label_cols='LOAN_STATUS', n_estimators=100, max_depth=10, min_samples_split=20, min_samples_leaf=5, max_features='sqrt'),
    RidgeClassifier(input_cols=feature_cols, label_cols='LOAN_STATUS', alpha=0.01),
    GradientBoostingClassifier(input_cols=feature_cols, label_cols='LOAN_STATUS', learning_rate=0.1),
    KNeighborsClassifier(input_cols=feature_cols, label_cols='LOAN_STATUS', n_neighbors=4)
]

# Evaluation loop
for model in models:
    print(f"Training: {type(model).__name__}")
    warnings.filterwarnings("ignore", category=UserWarning)
    model.fit(train_data)
    predictions = model.predict(val_data)
    acc = accuracy_score(df=predictions, y_true_col_names=['LOAN_STATUS'], y_pred_col_names=['PREDICTION'])
    f1 = f1_score(df=predictions, y_true_col_names=['LOAN_STATUS'], y_pred_col_names=['PREDICTION'])
    print(f"Accuracy: {acc}, F1 Score: {f1}")
    registry_model(model)