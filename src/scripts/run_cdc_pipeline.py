from cdc.cdc_handler import CDCHandler
from config.db_config import load_db_config
def main():
    config = load_db_config('config/config.yaml')
    handler = CDCHandler(config)
    handler.process_changes()
if __name__ == "__main__":
    main()