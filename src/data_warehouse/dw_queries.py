import snowflake.connector

class DWQueries:
    def __init__(self, config):
        self.config = config
        self.conn = snowflake.connector.connect(
            user=config['database']['snowflake']['user'],
            password=config['database']['snowflake']['password'],
            account=config['database']['snowflake']['account'],
            warehouse=config['database']['snowflake']['warehouse'],
            database=config['database']['snowflake']['database'],
            schema=config['database']['snowflake']['schema']
        )
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
