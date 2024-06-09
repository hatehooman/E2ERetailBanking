import snowflake.connector

class CDCDataLoader:
    def __init__(self, config):
        self.conn = snowflake.connector.connect(
            user=config['snowflake_user'],
            password=config['snowflake_password'],
            account=config['snowflake_account'],
            warehouse=config['snowflake_warehouse'],
            database=config['snowflake_database'],
            schema=config['snowflake_schema']
        )

        self.create_table_query = """
        CREATE TABLE IF NOT EXISTS INGREDIENTS (
            ingredient_id INT,
            ingredient_name STRING,
            ingredient_price FLOAT
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.create_table_query)
            self.conn.commit()
            cursor.close()
            print("Table INGREDIENTS is ready.")
        except Exception as e:
            print("Error creating table:", e)
            cursor.close()
            self.conn.close()
            exit(1)

    def insert_data(self, data):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO INGREDIENTS (ingredient_id, ingredient_name, ingredient_price)
                VALUES (%s, %s, %s)
            """, (data['ingredient_id'], data['ingredient_name'], data['ingredient_price']))
            cursor.close()
            self.conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("Error inserting data:", e)

    def load_changes(self, transformed_changes):
        for data in transformed_changes:
            self.insert_data(data)
