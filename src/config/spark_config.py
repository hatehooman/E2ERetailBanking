import yaml

def load_spark_config(config_path='config/config.yaml'):
    """
    Load Spark configuration from a YAML file.
    :param config_path: Path to the YAML configuration file
    :return: Dictionary containing Spark configuration
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['spark']

# Example usage:
# spark_config = load_spark_config()
# print(spark_config['app_name'])
