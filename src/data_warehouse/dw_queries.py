import snowflake.connector
from dw_snowflake_connection import create_snowflake_connection
class DWQueries:
    def __init__(self, config_path):

        self.conn = create_snowflake_connection(config_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# Example usage:
# config = load_config('config/config.yaml')
# queries = DWQueries(config)
# results = queries.execute_query("SELECT * FROM your_table")
# queries.close()
