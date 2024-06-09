import snowflake.connector

class DWLoader:
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

# Example usage:
# config = load_config('config/config.yaml')
# loader = DWLoader(config)
# loader.load_data(data)
# loader.close()
