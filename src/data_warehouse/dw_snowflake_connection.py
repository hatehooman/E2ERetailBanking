from config.db_config import ConfigLoader
import snowflake.connector

def create_snowflake_connection(config_path):
    """
    Create a connection to Snowflake using the provided configuration file.
    :param config_path: Path to the YAML configuration file
    :return: Snowflake connection object
    """
    config = ConfigLoader(config_path)
    db_config = config['snowflake']
    
    return snowflake.connector.connect(
        user=config['user'],
        password=config['password'],
        account=config['account'],
        warehouse=config['warehouse'],
        database=config['database'],
        shema=config['schema']
    )
