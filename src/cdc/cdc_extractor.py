from kafka import KafkaConsumer
from config.db_config import ConfigLoader

class CDCExtractor:
    def __init__(self, config):
        self.consumer = KafkaConsumer(
            config['kafka']['kafka_topic'], 
            bootstrap_servers=config['kafka']['kafka_bootstrap_servers']
        )

    def extract_changes(self):
        return self.consumer
    
# Main for test function

# if __name__ == "__main__":
#     config = ConfigLoader.load_db_config()
#     kafka_config = config['kafka']
#     extractor = CDCExtractor(kafka_config)
#     consumer = extractor.extract_changes()
#     for message in consumer:
#         print(f"Received message: {message.value}")