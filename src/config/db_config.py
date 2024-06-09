import yaml

def load_db_config(config_path='config/config.yaml'):
    """
    Load database configuration from a YAML file.
    :param config_path: Path to the YAML configuration file
    :return: Dictionary containing database configuration
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['database']

# Example usage:
# db_config = load_db_config()
# print(db_config['postgres']['dbname'])
