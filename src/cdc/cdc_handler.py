import snowflake.connector
from cdc.cdc_extractor import CDCExtractor
from cdc.cdc_transformer import CDCTransformer
from cdc.cdc_loader import CDCDataLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
                database=self.config['snowflake_database'],
                schema=self.config['snowflake_schema']
            )

            # Create the database if it doesn't exist
            conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {self.config['snowflake_database']}")

            # Use the database
            conn.cursor().execute(f"USE DATABASE {self.config['snowflake_database']}")

            # Create the schema if it doesn't exist
            conn.cursor().execute(f"CREATE SCHEMA IF NOT EXISTS {self.config['snowflake_schema']}")

            logger.info("Database and schema are ready.")
            conn.close()
        except Exception as e:
            logger.error(f"Error creating database and schema: {e}")

    def process_changes(self):
        changes = self.extractor.extract_changes()
        transformed_changes = self.transformer.transform_changes(changes)
        self.loader.load_changes(transformed_changes)


