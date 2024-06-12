import yaml

class ConfigLoader:
    @staticmethod
    def load_config(file_path='config/config.yaml'):
        """
        Load configuration from a YAML file.
        :param file_path: Path to the YAML configuration file
        :return: Dictionary containing configuration
        """
        with open(file_path, 'r') as file:
            try:
                config = yaml.safe_load(file)
                return config['database']
            except yaml.YAMLError as exc:
                print(f"Error loading configuration: {exc}")
                return None
