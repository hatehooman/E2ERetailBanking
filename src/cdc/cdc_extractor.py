from kafka import KafkaConsumer
from config.db_config import ConfigLoader

class CDCExtractor:
    def __init__(self, config):
        self.consumer = KafkaConsumer(
            config['kafka_topic'],
            bootstrap_servers=config['kafka_bootstrap_servers']
        )

    def extract_changes(self):
        return self.consumer
