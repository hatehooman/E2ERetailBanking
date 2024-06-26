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

        self.create_table_queries = {
            "district": """
                CREATE TABLE IF NOT EXISTS district (
                    district_id INTEGER NOT NULL PRIMARY KEY,
                    city VARCHAR(50) NOT NULL,
                    state_name VARCHAR(50) NOT NULL,
                    state_abbrev VARCHAR(50) NOT NULL,
                    region VARCHAR(50) NOT NULL,
                    division VARCHAR(50) NOT NULL
                );
            """,
            "account": """
                CREATE TABLE IF NOT EXISTS account (
                    account_id VARCHAR(20) NOT NULL PRIMARY KEY,
                    district_id INTEGER NOT NULL,
                    frequency VARCHAR(50) NOT NULL,
                    parseddate DATE NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL
                );
            """,
            "client": """
                CREATE TABLE IF NOT EXISTS client (
                    client_id VARCHAR(50) NOT NULL PRIMARY KEY,
                    sex VARCHAR(10) NOT NULL,
                    fulldate DATE NOT NULL,
                    day INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    social VARCHAR(15) NOT NULL,
                    first VARCHAR(50) NOT NULL,
                    middle VARCHAR(50),
                    last VARCHAR(50) NOT NULL,
                    phone VARCHAR(15) NOT NULL,
                    email VARCHAR(50) NOT NULL,
                    address_1 VARCHAR(100) NOT NULL,
                    address_2 VARCHAR(100),
                    city VARCHAR(50) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    zipcode INTEGER NOT NULL,
                    district_id INTEGER NOT NULL
                );
            """,
            "card": """
                CREATE TABLE IF NOT EXISTS card (
                    card_id VARCHAR(50) NOT NULL PRIMARY KEY,
                    disp_id VARCHAR(50) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    fulldate DATE NOT NULL
                );
            """,
            "disposition": """
                CREATE TABLE IF NOT EXISTS disposition (
                    disp_id VARCHAR(20) NOT NULL PRIMARY KEY,
                    client_id VARCHAR(20) NOT NULL,
                    account_id VARCHAR(20) NOT NULL,
                    type VARCHAR(50) NOT NULL
                );
            """,
            "loan": """
                CREATE TABLE IF NOT EXISTS loan (
                    loan_id VARCHAR(20) NOT NULL PRIMARY KEY,
                    account_id VARCHAR(20) NOT NULL,
                    amount FLOAT NOT NULL,
                    duration INTEGER NOT NULL,
                    payments INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    fulldate DATE NOT NULL,
                    location INTEGER NOT NULL,
                    purpose VARCHAR(20) NOT NULL
                );
            """,
            "order": """
                CREATE TABLE IF NOT EXISTS "order" (
                    order_id INTEGER NOT NULL PRIMARY KEY,
                    account_id VARCHAR(50) NOT NULL,
                    bank_to VARCHAR(50) NOT NULL,
                    account_to INTEGER NOT NULL,
                    amount FLOAT NOT NULL,
                    k_symbol VARCHAR(50)
                );
            """,
            "transaction": """
                CREATE TABLE IF NOT EXISTS transaction (
                    index INTEGER,
                    trans_id VARCHAR(50) NOT NULL PRIMARY KEY,
                    account_id VARCHAR(50) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    operation VARCHAR(50),
                    amount FLOAT NOT NULL,
                    balance FLOAT NOT NULL,
                    k_symbol VARCHAR(50),
                    bank VARCHAR(50),
                    account VARCHAR(50),
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    fulldate DATE NOT NULL,
                    fulltime VARCHAR(50) NOT NULL,
                    fulldatewithtime VARCHAR(50) NOT NULL
                );
            """,
            "CRMCallCenterLogs": """
                CREATE TABLE IF NOT EXISTS CRMCallCenterLogs (
                    Date_recieved DATE NOT NULL,
                    Complaint_id VARCHAR(50),
                    Rand_client VARCHAR(50),
                    Phonefinal VARCHAR(50) NOT NULL,
                    Vru_line VARCHAR(50),
                    Call_id INTEGER,
                    Priority INTEGER,
                    Type VARCHAR(50),
                    Outcome VARCHAR(50),
                    Server VARCHAR(50),
                    Ser_start VARCHAR(50) NOT NULL,
                    Ser_exit VARCHAR(50) NOT NULL,
                    Ser_time VARCHAR(50) NOT NULL
                );
            """,
            "CRMReviews": """
                CREATE TABLE IF NOT EXISTS CRMReviews (
                    Date DATE NOT NULL,
                    Stars INTEGER NOT NULL,
                    Reviews VARCHAR,
                    Product VARCHAR(50) NOT NULL,
                    district_id INTEGER NOT NULL
                );
            """,
            "CRMEvents": """
                CREATE TABLE IF NOT EXISTS CRMEvents (
                    Date_received DATE NOT NULL,
                    Product VARCHAR(50) NOT NULL,
                    Sub_product VARCHAR(50),
                    Issue VARCHAR(50) NOT NULL,
                    Sub_issue VARCHAR(20),
                    Consumer_complaint_narrative VARCHAR,
                    Tags VARCHAR(50),
                    Consumer_consent_provided VARCHAR(20),
                    Submitted_via VARCHAR(20) NOT NULL,
                    Date_sent_to_company DATE NOT NULL,
                    Company_response_to_consumer VARCHAR(50) NOT NULL,
                    Timely_response VARCHAR(20) NOT NULL,
                    Consumer_disputed VARCHAR(20),
                    Complaint_ID VARCHAR(20) NOT NULL PRIMARY KEY,
                    Client_ID VARCHAR(20) NOT NULL
                );
            """
        }

        try:
            cursor = self.conn.cursor()
            for table, query in self.create_table_queries.items():
                cursor.execute(query)
            self.conn.commit()
            cursor.close()
            print("All tables are ready.")
        except Exception as e:
            print("Error creating tables:", e)
            cursor.close()
            self.conn.close()
            exit(1)

    def insert_data(self, table, data):
        cursor = self.conn.cursor()
        insert_queries = {
            "district": """
                INSERT INTO district (district_id, city, state_name, state_abbrev, region, division)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            "account": """
                INSERT INTO account (account_id, district_id, frequency, parseddate, year, month, day)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            "client": """
                INSERT INTO client (client_id, sex, fulldate, day, month, year, age, social, first, middle, last, phone, email, address_1, address_2, city, state, zipcode, district_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            "card": """
                INSERT INTO card (card_id, disp_id, type, year, month, day, fulldate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            "disposition": """
                INSERT INTO disposition (disp_id, client_id, account_id, type)
                VALUES (%s, %s, %s, %s)
            """,
            "loan": """
                INSERT INTO loan (loan_id, account_id, amount, duration, payments, status, year, month, day, fulldate, location, purpose)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            "order": """
                INSERT INTO "order" (order_id, account_id, bank_to, account_to, amount, k_symbol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            "transaction": """
                INSERT INTO transaction (index, trans_id, account_id, type, operation, amount, balance, k_symbol, bank, account, year, month, day, fulldate, fulltime, fulldatewithtime)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            "CRMCallCenterLogs": """
                INSERT INTO CRMCallCenterLogs (Date_recieved, Complaint_id, Rand_client, Phonefinal, Vru_line, Call_id, Priority, Type, Outcome, Server, Ser_start, Ser_exit, Ser_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            "CRMReviews": """
                INSERT INTO CRMReviews (Date, Stars, Reviews, Product, district_id)
                VALUES (%s, %s, %s, %s, %s)
            """,
            "CRMEvents": """
                INSERT INTO CRMEvents (Date_received, Product, Sub_product, Issue, Sub_issue, Consumer_complaint_narrative, Tags, Consumer_consent_provided, Submitted_via, Date_sent_to_company, Company_response_to_consumer, Timely_response, Consumer_disputed, Complaint_ID, Client_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        }
        
        cursor.execute(insert_queries[table], data)
        self.conn.commit()
        cursor.close()
    
    def close_connection(self):
        self.conn.close()