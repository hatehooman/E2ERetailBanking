import json
from kafka import KafkaConsumer
import psycopg2

class CDCExtractor:
    def __init__(self, config):
        self.config = config
        self.consumer = KafkaConsumer(
            config['kafka']['topic'],
            bootstrap_servers=config['kafka']['bootstrap_servers'],
            group_id=config['kafka']['group_id'],
            auto_offset_reset=config['kafka']['auto_offset_reset'],
            enable_auto_commit=config['kafka']['enable_auto_commit']
        )

    def extract_changes(self):
        changes = []
        for message in self.consumer:
            change = json.loads(message.value)
            changes.append(change)
        return changes

    def extract_initial_snapshot(self):
        conn = psycopg2.connect(
            dbname=self.config['database']['postgres']['dbname'],
            user=self.config['database']['postgres']['user'],
            password=self.config['database']['postgres']['password'],
            host=self.config['database']['postgres']['host'],
            port=self.config['database']['postgres']['port']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM your_table")
        snapshot = cursor.fetchall()
        cursor.close()
        conn.close()
        return snapshot

# Example usage:
# from config.db_config import load_db_config
# config = load_db_config('config/config.yaml')
# extractor = CDCExtractor(config)
# changes = extractor.extract_changes()
