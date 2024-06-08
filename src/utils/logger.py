import logging
import logging.config
import yaml

def setup_logging(config_path='config/log_config.yaml', default_level=logging.INFO):
    """
    Setup logging configuration
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    except Exception as e:
        print(f"Error in Logging Configuration. Using default configs. Error: {e}")
        logging.basicConfig(level=default_level)

# Example usage
# logger = logging.getLogger(__name__)
