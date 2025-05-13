import sys
sys.path.insert(0, 'D:\\Big Data\\DS200\\E2ERetailBanking\\src')

from data_warehouse.dw_etl import ETL


# Entry point for running ETL
if __name__ == "__main__":

    etl = ETL(
        user='trucnmt',
        password='Thanhtruc28!',
        account='WK90181.ap-southeast-1',
        warehouse='IMPORT_WH',
        database='STAGING',
        schema='RAW'
    )
    etl.transform_and_move_tables('./Snowflake Data Warehouse/6 - ETL.sql')