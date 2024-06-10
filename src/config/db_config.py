import yaml

class ConfigLoader:
    @staticmethod
    def load_db_config(file_path='configs/config.yaml'):
        """
        Load database configuration from a YAML file.
        :param file_path: Path to the YAML configuration file
        :return: Dictionary containing database configuration
        """
        with open(file_path, 'r') as file:
            try:
                config = yaml.safe_load(file)
                return config['database']
            except yaml.YAMLError as exc:
                print(exc)
                return None