import snowflake.connector

class CDCDataLoader:
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

    def load_changes(self, changes):
        for change in changes:
            self._load_change(change)

    def _load_change(self, change):
        # Implement your loading logic here
        query = "INSERT INTO your_table (columns) VALUES (values)"
        self.cursor.execute(query)

    def close(self):
        self.cursor.close()
        self.conn.close()

# Example usage:
# from config.db_config import load_db_config
# config = load_db_config('config/config.yaml')
# loader = CDCDataLoader(config)
# loader.load_changes(transformed_changes)
# loader.close()
