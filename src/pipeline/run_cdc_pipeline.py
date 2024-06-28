import sys
sys.path.insert(0, 'D:\\Big Data\\DS200\\E2ERetailBanking\\src')
from concurrent.futures import ThreadPoolExecutor
from cdc.cdc_handler import CDCHandler

def main():
    configs = [
        {
            'kafka_topic': "postgres.public.account",
            'kafka_bootstrap_servers': ["localhost:29092"],
            'avro_schema_path': "./Avro Schema/account.avsc",
            'snowflake_user': 'trucnmt',
            'snowflake_password': 'Thanhtruc28!',
            'snowflake_account': 'WK90181.ap-southeast-1',
            'snowflake_warehouse': 'COMPUTE_WH',
            'snowflake_database': 'POSTGRES',
            'snowflake_schema': 'PUBLIC',
            'sql_file_path' : './Postgres/account.sql',
            'table_name' : 'account'
        },
        {
            'kafka_topic': "postgres.public.district",
            'kafka_bootstrap_servers': ["localhost:29092"],
            'avro_schema_path': "./Avro Schema/district.avsc",
            'snowflake_user': 'trucnmt',
            'snowflake_password': 'Thanhtruc28!',
            'snowflake_account': 'WK90181.ap-southeast-1',
            'snowflake_warehouse': 'COMPUTE_WH',
            'snowflake_database': 'POSTGRES',
            'snowflake_schema': 'PUBLIC',
            'sql_file_path' : './Postgres/district.sql',
            'table_name' : 'district'
        }
    ]

    with ThreadPoolExecutor() as executor:
        for config in configs:
            executor.submit(run_handler, config)

def run_handler(config):
    handler = CDCHandler(config)
    handler.process_changes()

if __name__ == "__main__":
    main()
