import avro.schema
import io
from avro.io import DatumReader, BinaryDecoder
from kafka import KafkaConsumer
import snowflake.connector
import logging
import datetime
from concurrent.futures import ThreadPoolExecutor
import json

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
        self.schema = avro.schema.parse(open(config['avro_schema_path'], 'rb').read())
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
        try:
            return datetime.datetime.strptime(date_obj, "%Y-%m-%d").date().isoformat()
        except (ValueError, TypeError):
            return None

    def format_datetime(self, datetime_obj):
        try:
            return datetime.datetime.strptime(datetime_obj, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError):
            return None

    def handle_date_field(self, decoded_message, date_field):
        if date_field in decoded_message and decoded_message[date_field]:
            if date_field == 'fulldatewithtime':
                formatted_datetime = self.format_datetime(decoded_message[date_field])
                if formatted_datetime:
                    decoded_message['fulldatewithtime'] = formatted_datetime
                else:
                    logger.error(f"Invalid datetime found: {decoded_message[date_field]}")
            else:
                parsed_date = self.format_date(decoded_message[date_field])
                if parsed_date:
                    year, month, day = map(int, parsed_date.split('-'))
                    decoded_message['year'] = year
                    decoded_message['month'] = month
                    decoded_message['day'] = day
                    decoded_message[date_field] = parsed_date
                else:
                    logger.error(f"Invalid date found: {decoded_message[date_field]}")

    def transform_changes(self, changes):
        date_fields = ['parseddate', 'Date_recieved', 'Date', 'fulldate', 'fulldatewithtime']
        for msg in changes:
            decoded_message = self.decode(msg.value)
            if decoded_message:
                for date_field in date_fields:
                    self.handle_date_field(decoded_message, date_field)
                yield decoded_message


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
        self.table_name = config['table_name']
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
                logger.info(f"Table {self.table_name} is ready.")
            except Exception as e:
                logger.error(f"Error creating table {self.table_name}: {e}")
                if cursor:
                    cursor.close()
                self.conn.close()
                exit(1)

    def insert_data(self, data):
        cursor = self.conn.cursor()
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(data.values()))
            cursor.close()
            self.conn.commit()
            logger.info(f"Data inserted successfully into {self.table_name}.")
        except Exception as e:
            logger.error(f"Error inserting data into {self.table_name}: {e}")
            if cursor:
                cursor.close()

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

def main():
    with open('./src/config/config_cdc.json', 'r') as f:
        config_data = json.load(f)
    
    configs = config_data['configs']

    with ThreadPoolExecutor() as executor:
        for config in configs:
            executor.submit(run_handler, config)

def run_handler(config):
    handler = CDCHandler(config)
    handler.process_changes()

if __name__ == "__main__":
    main()