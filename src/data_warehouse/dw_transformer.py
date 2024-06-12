import yaml
from snowflake.connector import connect

class DWTransformer:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.conn = self.connect_to_snowflake()

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def connect_to_snowflake(self):
        return connect(
            user=self.config['snowflake']['user'],
            password=self.config['snowflake']['password'],
            account=self.config['snowflake']['account'],
            warehouse=self.config['snowflake']['warehouse'],
            database=self.config['snowflake']['database'],
            schema=self.config['snowflake']['schema']
        )

    def transform_data(self, source_table, target_table, transformation_query):
        # Load data from source_table
        data = self.load_data(source_table)
        
        # Apply transformation
        transformed_data = self.apply_transformation(data, transformation_query)
        
        # Save transformed data to target_table
        self.save_data(transformed_data, target_table)

    def load_data(self, source_table):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {source_table}")
        data = cursor.fetchall()
        cursor.close()
        return data

    def apply_transformation(self, data, transformation_query):
        cursor = self.conn.cursor()
        cursor.execute(transformation_query)
        transformed_data = cursor.fetchall()
        cursor.close()
        return transformed_data

    def save_data(self, transformed_data, target_table):
        cursor = self.conn.cursor()
        # Assume transformed_data is a list of tuples matching the target_table schema
        insert_query = f"INSERT INTO {target_table} VALUES " + ",".join(
            str(tuple(record)) for record in transformed_data
        )
        cursor.execute(insert_query)
        cursor.close()

    def close_connection(self):
        self.conn.close()

# Example usage:
# config_path = 'config/config.yaml'
# source_table = 'STAGING.RAW.raw_table'
# target_table = 'STAGING.CLEAN.cleaned_table'
# transformation_query = '''
#     SELECT col1, col2, col3 * 2 as col3
#     FROM STAGING.RAW.raw_table
# '''
# transformer = DWTransformer(config_path)
# transformer.transform_data(source_table, target_table, transformation_query)
# transformer.close_connection()
