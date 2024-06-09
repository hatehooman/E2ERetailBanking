from cdc_extractor import CDCExtractor
from cdc_transformer import CDCTransformer
from cdc_loader import CDCDataLoader
import snowflake.connector

class CDCHandler:
    def __init__(self, config):
        self.config = config
        self.create_database_and_schema()
        self.extractor = CDCExtractor(config)
        self.transformer = CDCTransformer(config)
        self.loader = CDCDataLoader(config)

    def create_database_and_schema(self):
        try:
            conn = snowflake.connector.connect(
                user=self.config['snowflake_user'],
                password=self.config['snowflake_password'],
                account=self.config['snowflake_account'],
                warehouse=self.config['snowflake_warehouse'],
                database='snowflake',
                schema='public'
            )

            # Create the database if it doesn't exist
            conn.cursor().execute("CREATE DATABASE IF NOT EXISTS POSTGRES")

            # Use the database
            conn.cursor().execute("USE DATABASE POSTGRES")

            # Create the schema if it doesn't exist
            conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS PUBLIC")

            print("Database and schema are ready.")
            conn.close()
        except Exception as e:
            print("Error creating database and schema:", e)

    def process_changes(self):
        changes = self.extractor.extract_changes()
        transformed_changes = self.transformer.transform_changes(changes)
        self.loader.load_changes(transformed_changes)