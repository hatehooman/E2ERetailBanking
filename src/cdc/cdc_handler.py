from cdc.cdc_extractor import CDCExtractor
from cdc.cdc_transformer import CDCTransformer
from cdc.cdc_loader import CDCDataLoader

class CDCHandler:
    def __init__(self, config):
        self.extractor = CDCExtractor(config)
        self.transformer = CDCTransformer(config)
        self.loader = CDCDataLoader(config)

    def process_changes(self):
        changes = self.extractor.extract_changes()
        transformed_changes = self.transformer.transform_changes(changes)
        self.loader.load_changes(transformed_changes)

# Example usage:
# from config.db_config import load_db_config
# config = load_db_config('config/config.yaml')
# handler = CDCHandler(config)
# handler.process_changes()
