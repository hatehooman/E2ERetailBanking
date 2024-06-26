from cdc.cdc_extractor import CDCExtractor
from cdc.cdc_loader import CDCDataLoader
from cdc.cdc_transformer import CDCTransformer

if __name__ == "__main__":
    import json

    with open('config.json', 'r') as f:
        config = json.load(f)

    extractor = CDCExtractor(config)
    transformer = CDCTransformer(config['avro_schema_paths'])  # Updated to use a mapping of schemas
    loader = CDCDataLoader(config)

    changes = extractor.extract_changes()
    transformed_changes = transformer.transform_changes(changes)

    for table, data in transformed_changes:
        loader.insert_data(table, data)

    loader.close_connection()

    
