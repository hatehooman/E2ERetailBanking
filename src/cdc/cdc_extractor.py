import json
from kafka import KafkaConsumer

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
            changes = json.loads(message.value)
            changes.append(changes)
        return changes
    

# Test usage:
# config = load_config('config/config.yaml')
# extractor = CDCExtractor(config)
# changes = extractor.extract_changes()