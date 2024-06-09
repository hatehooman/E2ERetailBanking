import yaml
import logging.config

def setup_logging(config_path='config/config.yaml'):
    """
    Setup logging configuration from a YAML file.
    :param config_path: Path to the YAML configuration file
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    logging.config.dictConfig(config['logging'])

# Example usage:
# setup_logging()
# logger = logging.getLogger(__name__)
# logger.debug('This is a debug message')
