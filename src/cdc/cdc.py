import avro.schema
import io
from avro.io import DatumReader, BinaryDecoder
from kafka import KafkaConsumer
import snowflake.connector
import logging
import datetime
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CDCExtractor:
    def __init__(self, config):
        self.consumer = KafkaConsumer(
            config['kafka_topic'],
            bootstrap_servers=config['kafka_bootstrap_servers'],
            value_deserializer=None
        )

    def extract_changes(self):
        return self.consumer

class CDCTransformer:
    def __init__(self, config):
        self.schema = avro.schema.parse(open(config['avro_schema_path'], "rb").read())
        self.reader = DatumReader(self.schema)

    def decode(self, msg_value):
        message_bytes = io.BytesIO(msg_value)
        message_bytes.seek(7)  # Skip the magic byte and schema ID
        decoder = BinaryDecoder(message_bytes)
        try:
            event_dict = self.reader.read(decoder)
            return event_dict
        except Exception as e:
            logger.error(f"Error decoding message: {e}")
            logger.error(f"Message value: {msg_value}")
            return None

    def format_date(self, date_obj):
        if isinstance(date_obj, datetime.date):
            return date_obj.isoformat()
        return None

    def transform_changes(self, changes):
        for msg in changes:
            decoded_message = self.decode(msg.value)
            if decoded_message:
                # Ensure proper date handling
                if 'parseddate' in decoded_message and decoded_message['parseddate']:
                    parsed_date = self.format_date(decoded_message['parseddate'])
                    if parsed_date:
                        year, month, day = map(int, parsed_date.split('-'))
                        decoded_message['year'] = year
                        decoded_message['month'] = month
                        decoded_message['day'] = day
                        decoded_message['parseddate'] = parsed_date
                        yield decoded_message
                    else:
                        logger.error(f"Invalid date found: {decoded_message['parseddate']}")
                else:
                    logger.error(f"Missing or empty 'parseddate' field in message: {decoded_message}")

class CDCDataLoader:
    def __init__(self, config):
        self.conn = snowflake.connector.connect(
            user=config['snowflake_user'],
            password=config['snowflake_password'],
            account=config['snowflake_account'],
            warehouse=config['snowflake_warehouse'],
            database=config['snowflake_database'],
            schema=config['snowflake_schema']
        )
        self.create_table_query = self.read_sql_file(config['sql_file_path'])
        self.create_table()
        
    def read_sql_file(self, sql_file_path):
        try:
            with open(sql_file_path, 'r') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading SQL file {sql_file_path}: {e}")
            return None

    def create_table(self):
        if self.create_table_query:
            try:
                cursor = self.conn.cursor()
                cursor.execute(self.create_table_query)
                self.conn.commit()
                cursor.close()
                logger.info("Table account is ready.")
            except Exception as e:
                logger.error(f"Error creating table: {e}")
                if cursor:
                    cursor.close()
                self.conn.close()
                exit(1)

    def insert_data(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO account (account_id, district_id, frequency, parseddate, year, month, day)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data['account_id'], data['district_id'], data['frequency'], data['parseddate'], data['year'], data['month'], data['day']))
            cursor.close()
            self.conn.commit()
            logger.info("Data inserted successfully.")
        except Exception as e:
            logger.error(f"Error inserting data: {e}")

    def load_changes(self, transformed_changes):
        for data in transformed_changes:
            self.insert_data(data)

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

            logger.info("Database and schema are ready.")
            conn.close()
        except Exception as e:
            logger.error(f"Error creating database and schema: {e}")

    def process_changes(self):
        changes = self.extractor.extract_changes()
        transformed_changes = self.transformer.transform_changes(changes)
        self.loader.load_changes(transformed_changes)

def main():
    config = {
        'kafka_topic': "postgres.public.account",
        'kafka_bootstrap_servers': ["localhost:29092"],
        'avro_schema_path': "./Avro Schema/account.avsc",
        'snowflake_user': 'trucnmt',
        'snowflake_password': 'Thanhtruc28!',
        'snowflake_account': 'WK90181.ap-southeast-1',
        'snowflake_warehouse': 'COMPUTE_WH',
        'snowflake_database': 'POSTGRES',
        'snowflake_schema': 'PUBLIC',
        'sql_file_path' : './Postgres/account.sql'
    }

    handler = CDCHandler(config)
    handler.process_changes()

if __name__ == "__main__":
    main()
