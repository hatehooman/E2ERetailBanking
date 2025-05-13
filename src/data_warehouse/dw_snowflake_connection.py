# snowflake_connection.py

from snowflake.connector import connect, ProgrammingError

class SnowflakeConnection:
    def __init__(self, user, password, account, warehouse, database, schema):
        self.user = user
        self.password = password
        self.account = account
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.conn = None
        self.cursor = None

    def connect(self):
        conn_params = {
            'user': self.user,
            'password': self.password,
            'account': self.account,
            'warehouse': self.warehouse,
            'database': self.database,
            'schema': self.schema
        }
        try:
            self.conn = connect(**conn_params)
            self.cursor = self.conn.cursor()
            print("Connected to Snowflake")
        except ProgrammingError as e:
            print(f"Error connecting to Snowflake: {e}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("Snowflake connection closed")
        except ProgrammingError as e:
            print(f"Error closing Snowflake connection: {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            print(f"Executed query: {query}")
        except ProgrammingError as e:
            print(f"Error executing query: {e}")
