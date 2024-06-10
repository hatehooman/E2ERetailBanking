from cdc.cdc_handler import CDCHandler
from config.db_config import ConfigLoader
import sys

def main(config_file):
    # config = ConfigLoader.load_db_config('config/config.yaml')
    config = ConfigLoader.load_db_config(config_file)
    handler = CDCHandler(config)
    handler.process_changes()
    
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python src/run_cdc_pipeline.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)

# Run .bash
# python src/run_cdc_pipeline.py config/config_import.yaml
# python src/run_cdc_pipeline.py config/config_transform.yaml
# python src/run_cdc_pipeline.py config/config_reporting.yaml