# -*- coding: utf-8 -*-

# === Snowflake & Data Science Imports ===
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col, when, count, dense_rank
from snowflake.snowpark.window import Window
from snowflake.ml.modeling.metrics import accuracy_score, f1_score
from snowflake.ml.registry import Registry
from snowflake.ml.modeling.ensemble import RandomForestClassifier, GradientBoostingClassifier
from snowflake.ml.modeling.tree import DecisionTreeClassifier
from snowflake.ml.modeling.linear_model import RidgeClassifier, LogisticRegression
from snowflake.ml.modeling.neighbors import KNeighborsClassifier

import pandas as pd
import random
import warnings

# === Configuration ===
connection_param = {
    'user': 'trucnmt',
    'password': 'Thanhtruc28!',
    'account': 'WK90181.ap-southeast-1',
    'warehouse': 'ETL_WH',
    'database': 'STAGING',
    'schema': 'CLEAN',
    'role': 'TRANSFORM_ROLE'
}

CATEGORICAL_COLS = ['loan_purpose', 'trans_type', 'operation_type', 'trans_k_symbol', 'trans_bank', 'order_k_symbol', 'order_bank_to']
FEATURE_COLS = [
    'loan_amount', 'loan_duration', 'loan_payments', 'loan_year', 'loan_month', 'loan_day',
    'trans_type_idx', 'operation_type_idx', 'trans_amount', 'trans_balance',
    'trans_k_symbol_idx', 'trans_bank_idx', 'order_bank_to_idx', 'order_k_symbol_idx'
]
LABEL_COL = 'loan_status'


# === Helper Functions ===
def init_session():
    return Session.builder.configs(connection_param).create()


def load_data(session):
    trans_df = session.table('C_TRANSACTION')
    loan_df = session.table('LOAN')
    order_df = session.table('C_ORDER')
    return loan_df, trans_df, order_df


def preprocess_and_join(session, loan_df, trans_df, order_df):
    df = loan_df.join(trans_df, 'account_id').join(order_df, 'account_id')
    df = df.with_column("loan_status", when(col("loan_status").isin("C", "A"), 0).otherwise(1))

    for column in CATEGORICAL_COLS:
        window_spec = Window.order_by(col(column))
        df = df.with_column(f"{column}_idx", dense_rank().over(window_spec).cast("float"))

    return df


def balance_dataset(session, df, label_col):
    label_distribution = df.group_by(label_col).agg(count("*").alias("count"))
    max_count = label_distribution.select("count").agg({"count": "max"}).collect()[0][0]
    schema = df.schema
    balanced_df = session.create_dataframe([], schema=schema)

    for row in label_distribution.collect():
        label = row[label_col]
        count_label = row["COUNT"]
        subset_df = df.filter(col(label_col) == label)

        if count_label < max_count:
            oversampled_df = subset_df
            while oversampled_df.count() < (max_count - count_label):
                oversampled_df = oversampled_df.union_all(subset_df)
            oversampled_df = oversampled_df.limit(max_count - count_label)
            subset_df = subset_df.union_all(oversampled_df)

        balanced_df = balanced_df.union_all(subset_df)

    return balanced_df


def split_train_val(df, feature_cols, label_col):
    df_pandas = df.to_pandas()
    df_pandas['random_val'] = [random.random() for _ in range(len(df_pandas))]

    train_df = df_pandas[df_pandas['random_val'] < 0.7].reset_index(drop=True)
    val_df = df_pandas[df_pandas['random_val'] >= 0.7].reset_index(drop=True)

    all_cols = feature_cols + [label_col]
    return train_df[all_cols], val_df[all_cols]


def train_and_evaluate_models(session, train_df, val_df, feature_cols, label_col, registry):
    train_data = session.create_dataframe(train_df)
    val_data = session.create_dataframe(val_df)

    models = [
        LogisticRegression(input_cols=feature_cols, label_cols=label_col, max_iter=10000, C=0.01),
        DecisionTreeClassifier(input_cols=feature_cols, label_cols=label_col, max_depth=10, min_samples_split=20, min_samples_leaf=5),
        RandomForestClassifier(input_cols=feature_cols, label_cols=label_col, n_estimators=100, max_depth=10, min_samples_split=20, min_samples_leaf=5, max_features='sqrt'),
        RidgeClassifier(input_cols=feature_cols, label_cols=label_col, alpha=0.01),
        GradientBoostingClassifier(input_cols=feature_cols, label_cols=label_col, learning_rate=0.1),
        KNeighborsClassifier(input_cols=feature_cols, label_cols=label_col, n_neighbors=4)
    ]

    for model in models:
        print(f"\nTraining: {type(model).__name__}")
        warnings.filterwarnings("ignore", category=UserWarning)
        model.fit(train_data)
        predictions = model.predict(val_data)

        acc = accuracy_score(df=predictions, y_true_col_names=[label_col], y_pred_col_names=['PREDICTION'])
        f1 = f1_score(df=predictions, y_true_col_names=[label_col], y_pred_col_names=['PREDICTION'])
        print(f"Accuracy: {acc}, F1 Score: {f1}")

        registry.log_model(
            model,
            model_name=type(model).__name__,
            version_name="v2_fulldata",
            conda_dependencies=["scikit-learn"],
            comment="Auto-registered model",
            metrics={"score": model.score(val_data)},
            sample_input_data=train_df[feature_cols],
            options={"relax_version": False}
        )


# === Main Pipeline ===
def main():
    session = init_session()
    registry = Registry(session=session, database_name="STAGING", schema_name="CLEAN")

    loan_df, trans_df, order_df = load_data(session)
    joined_df = preprocess_and_join(session, loan_df, trans_df, order_df)
    balanced_df = balance_dataset(session, joined_df, LABEL_COL)
    train_df, val_df = split_train_val(balanced_df, FEATURE_COLS, LABEL_COL)

    train_and_evaluate_models(session, train_df, val_df, FEATURE_COLS, LABEL_COL, registry)


if __name__ == "__main__":
    main()
