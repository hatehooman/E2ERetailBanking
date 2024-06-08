# Database and Data Warehouse utility functions (Postgres, Snowflake)
import psycopg2
from psycopg2 import sql
import snowflake.connector

def get_pg_connection(config):

    """
    Create a PostgreSQL database connection
    :param config: Dictionary containing database connection parameters
    :return: Connection object
    """

    '''
        *dbname*: the database name
        *database*: the database name (only as keyword argument)
        *user*: user name used to authenticate
        *password*: password used to authenticate
        *host*: database host address (defaults to UNIX socket if not provided)
        *port*: connection port number (defaults to 5432 if not provided)
    '''
    return psycopg2.connect(
        dbname=config['dbname'],
        database=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )

def get_snowflake_connection(config):

    """
    Create a Snowflake database connection
    :param config: Dictionary containing database connection parameters
    :return: Connection object
    """

    return snowflake.connector.connect(
        user=config['user'],
        password=config['password'],
        account=config['account'],
        role=config['role'],
        warehouse=config['warehouse'],
        database=config['database'],
        schema=config['schema']
    )

def execute_query(connection, query,params = None):
    """
    Execute a SQL query
    :param connection: Database connection object
    :param query: SQL query string
    :param params: Query parameters
    :return: Query result
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.commit()

def fetch_results(connection ,query, params = None):
    """
    Fetch results from a SQL query
    :param connection: Database connection object
    :param query: SQL query string
    :param params: Query parameters
    :return: Query results
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.fetchall()