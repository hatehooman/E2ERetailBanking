from kafka import KafkaConsumer

class CDCExtractor:
    def __init__(self, config):
        self.consumer = KafkaConsumer(
            config['kafka_topic'],
            bootstrap_servers=config['kafka_bootstrap_servers'],
            value_deserializer=None
        )

    def extract_changes(self):
        return self.consumer