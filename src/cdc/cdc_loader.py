import snowflake.connector

class CDCDataLoader:
    def __init__(self, config):
        self.config = config
        self.conn = snowflake.connector.connect(
            user=config['database']['snowflake']['user'],
            password=config['database']['snowflake']['password'],
            account=config['database']['snowflake']['account']
        )
        self.cursor = self.conn.cursor()

    def load_changes(self, changes):
        for change in changes:
            self._load_change(change)

    def _load_change(self, change):
        # Implement loading logic here
        # Phan nay sua sau
        query = "INSERT INTO your_table (columns) VALUES (values)"
        self.cursor.execute(query)

    def close(self):
        self.cursor.close()
        self.conn.close()

# Example usage:
# config = load_config('config/config.yaml')
# loader = CDCDataLoader(config)
# loader.load_changes(transformed_changes)
# loader.close()
