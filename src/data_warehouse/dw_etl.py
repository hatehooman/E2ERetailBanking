import os
from src.data_warehouse.dw_snowflake_connection import SnowflakeConnection

class ETL:
    def __init__(self, user, password, account, warehouse, database, schema):
        self.user = user
        self.password = password
        self.account = account
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.conn = None

    def connect(self):
        try:
            conn_params = {
                'user': self.user,
                'password': self.password,
                'account': self.account,
                'warehouse': self.warehouse,
                'database': self.database,
                'schema': self.schema
            }
            self.conn = SnowflakeConnection(**conn_params)
            self.conn.connect()
            print("Connected to Snowflake")
        except Exception as e:
            print(f"Error connecting to Snowflake: {e}")

    def close(self):
        try:
            if self.conn:
                self.conn.close()
                print("Connection to Snowflake closed")
        except Exception as e:
            print(f"Error closing Snowflake connection: {e}")

    def read_sql_queries_from_file(self, file_path):
        with open(file_path, 'r') as file:
            sql_queries = file.read().split(';')
        # Remove empty strings and extra whitespaces
        sql_queries = [query.strip() for query in sql_queries if query.strip()]
        return sql_queries

    def execute_queries_from_file(self, file_path):
        sql_queries = self.read_sql_queries_from_file(file_path)
        try:
            for query in sql_queries:
                self.conn.execute_query(query)
        except Exception as e:
            print(f"Error executing queries from file: {e}")

    def transform_and_move_tables(self, file_path):
        try:
            self.connect()
            # Execute queries from file
            self.execute_queries_from_file(file_path)
        finally:
            self.close()


