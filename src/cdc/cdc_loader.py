import snowflake.connector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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