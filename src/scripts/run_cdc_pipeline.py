from cdc.cdc_handler import CDCHandler

def main():
    config = {
        'kafka_topic': "postgres.public.ingredients",
        'kafka_bootstrap_servers': ["localhost:29092"],
        'avro_schema_path': "./schema.avsc",
        'snowflake_user': 'trucnmt',
        'snowflake_password': 'Thanhtruc28!',
        'snowflake_account': 'WK90181.ap-southeast-1',
        'snowflake_warehouse': 'COMPUTE_WH',
        'snowflake_database': 'POSTGRES',
        'snowflake_schema': 'PUBLIC'
    }

    handler = CDCHandler(config)
    handler.process_changes()

if __name__ == "__main__":
    main()