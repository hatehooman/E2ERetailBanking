from dw_snowflake_connection import create_snowflake_connection
class DWLoader:

    def __init__(self, config_path):

        self.conn = create_snowflake_connection(config_path)
        self.cursor = self.conn.cursor()

    def load_data(self, data):

        for record in data:
            self._load_record(record)

    def _load_record(self, record):
        # Implement loading logic here
        query = "INSERT INTO your_table (columns) VALUES (values)"
        self.cursor.execute(query)

    def close(self):

        self.cursor.close()
        self.conn.close()


