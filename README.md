<h1 align="center">End to End Data Pipeline for Modern Data Analytics Platform in Retail Banking</h1>

<p align="center"><small>Faculty of Information Science and Engineering, University of Information Technology, Ho Chi Minh City, Viet Nam <br>
Vietnam National University, Ho Chi Minh City, Viet Nam <br> <strong>Instructor: PhD. Do Trong Hop</strong> 
</small></p>




Contributors
--------------------- 

<div align="center">
  <table>
    <tr>
      <th>Student's ID</th>
      <th>Fullname</th>
      <th>Contact</th>
      <th>Task Assignment</th>
    </tr>
    <tr>
      <td>21522721</td>
      <td>Nguyen Mai Thanh Truc</td>
      <td>21522721@gm.uit.edu.vn</td>
      <td>Pipeline, CDC, Data Warehouse</td>
    </tr>
    <tr>
      <td>21521937</td>
      <td>Nguyen Minh Dat</td>
      <td>21521937@gm.uit.edu.vn</td>
      <td>Analysis, Model Training</td>
    </tr>
  </table>
</div>


----------------
Description
----------------
The banking industry is a field that uses big data and is constantly growing under the push of the big data era. Exploring advanced big data analytics tools such as data mining (DM) techniques is key for the banking industry, which aims to reveal valuable information from huge volumes of data and achieve data management. In this project, we will build a Big Data Analytics System in the Retail Banking Industry.

-----------------
### Problem Statement
In the context of retail banking, it is crucial to automate the loan approval process to ensure efficient, accurate, and fair decision-making. This involves assessing various attributes of a customer's loan application and determining whether the loan should be approved or rejected.
* Input: Customer loan approval profile
* Output: Approved/Rejected
--------------
Retail Banking's Architecture
-------------
![Pipeline](./Architecture/Retail%20Banking%20System.png)


---------------
Entity Relationship Diagram of Retail Banking Database
---------------
![ER-Diagram](./ER%20Diagram/ER-Diagram.png)



-----------------
Main task in our project
-----------------
1. Change Data Capture (CDC)
2. Build Data Warehouse
3. Analysis and Model Training

Technologies
----------------
1. Apache Spark
2. Apache Kafka
3. Apache ZooKeeper
4. Debezium Connector
5. Snowflake - Cloud Data Warehouse
6. PostgreSQL
7. Docker
8. Python
---------------


Change Data Capture
----------------
![CDC](./Architecture/Change%20Data%20Capture.png)

* **Data Source**: Postgres
* **CDC Connector**: Debezium
* **Data Ingestion**: Kafka
* **Data Storage (Target)**: Snowflake Data Warehouse

#### Comparison of Change Data Capture (CDC), Batch Processing, and Real-Time Processing

| Feature          | Change Data Capture (CDC)       | Batch Processing                      | Real-Time Processing                  |
|------------------|---------------------------------|---------------------------------------|---------------------------------------|
| **Latency**      | Near real-time                  | High (scheduled intervals)            | Very low (milliseconds)               |
| **Granularity**  | Row-level changes               | Large batches                         | Individual events or small batches    |
| **Complexity**   | Moderate to high                | Low to moderate                       | High                                  |
| **Resource Usage** | Moderate                      | High during batch windows             | High                                  |
| **Use Cases**    | Data sync, real-time analytics  | Reporting, data warehousing           | Fraud detection, live dashboards      |
| **Advantages**   | Efficient data transfer         | Simple and efficient for large data   | Immediate insights and actions        |
| **Disadvantages**| Complexity, potential latency   | High latency, peak resource needs     | Complexity, cost                      |


Data Warehouse Architecture
----------------

![DataWarehouse](./Architecture/Data%20Warehouse%20Design.png)

#### Snowflake Data Warehouse Setup Detail

| Component   | Quantity | Detail                                                                                                                                     |
|-------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Databases   | 2        | STAGING, PROD                                                                                                                              |
| Schemas     | 3        | STAGING.RAW: Keep original raw data as it is ingested. <br> STAGING.CLEAN: Keep cleaned data for ETL & modeling. <br> PROD.REPORTING: Used by BI User & Data Analyst |
| Warehouses  | 3        | Import Warehouse <br> Transform Warehouse <br> Reporting Warehouse                                                                         |
| Roles       | 3        | Import Role: Can read from file stage & write to both schemas in StagingDB. No Access to Prod <br> Transform Role: Can read & write to STAGING DB.CLEAN + PROD.REPORTING, No Access to STAGING DB.RAW <br> Reporting Role: Read-only access to PROD.REPORTING schema & tables |
| Users       | 3        | UserReporting (belongs to REPORTING ROLE) <br> UserTransform (belongs to TRANSFORM ROLE) <br> UserImport (belongs to IMPORT ROLE)          |


Analysis and Model Training
-----------------
1. Process
2. Modeling
3. Evaluation

Project Organization
------------

```
└── 📁E2ERetailBanking
    └── .env
    └── 📁Architecture
        └── Change Data Capture.pdf
        └── Change Data Capture.png
        └── Data Warehouse Design.pdf
        └── Data Warehouse Design.png
        └── Retail Banking System.pdf
        └── Retail Banking System.png
    └── 📁Avro Schema
        └── account.avsc
        └── call_center_logs.avsc
        └── card.avsc
        └── client.avsc
        └── crm_events.avsc
        └── crm_reviews.avsc
        └── disposition.avsc
        └── district.avsc
        └── loan.avsc
        └── order.avsc
        └── transaction.avsc
    └── 📁Dataset
        └── data_combine_300.csv
        └── 📁Retail-Banking-Demo-Data
            └── completedacct.csv
            └── completedcard.csv
            └── completedclient.csv
            └── completeddisposition.csv
            └── completeddistrict.csv
            └── completedloan.csv
            └── completedorder.csv
            └── completedtrans.csv
            └── CRM Call Center Logs.csv
            └── CRM Events.csv
            └── CRM Reviews.csv
            └── LuxuryLoanPortfolio.csv
        └── Retail-Banking-Demo-Data.zip
    └── debezium.json
    └── docker_compose.yml
    └── 📁ER Diagram
        └── ER-Diagram.png
    └── LICENSE
    └── Makefile
    └── README.md
    └── requirements.txt
    └── 📁Snowflake Data Warehouse
        └── 0 - Postgres - Script.sql
        └── 1 - MODIFY.sql
        └── 2 - IMPORT RESOURCE.sql
        └── 3 - TRANSFORM RESOURCE.sql
        └── 4 - REPORTING RESOURCE.sql
        └── 5 - RESOURCE MONITORS.sql
    └── 📁src
        └── 📁cdc
            └── cdc_extractor.py
            └── cdc_handler.py
            └── cdc_loader.py
            └── cdc_transformer.py
            └── __init__.py
        └── 📁config
            └── config.yaml
            └── config_import.yaml
            └── config_reporting.yaml
            └── config_transform.yaml
            └── db_config.py
            └── log_config.py
            └── spark_config.py
            └── __init__.py
        └── 📁data_warehouse
            └── dw_loader.py
            └── dw_queries.py
            └── dw_schema.sql
            └── dw_snowflake_connection.py
            └── dw_transformer.py
            └── __init__.py
        └── 📁scripts
            └── run_cdc_pipeline.py
            └── run_dw_pipeline.py
            └── run_spark_job.py
            └── __init__.py
        └── 📁spark
            └── .gitignore
            └── spark_job.py
            └── spark_session.py
            └── spark_trainer.py
            └── spark_transformer.py
            └── __init__.py
            └── 📁__pycache__
                └── spark_session.cpython-311.pyc
                └── spark_transformer.cpython-311.pyc
        └── 📁utils
            └── db_utils.py
            └── file_utils.py
            └── kafka_utils.py
            └── logger.py
            └── spark_utils.py
            └── __init__.py
        └── __init__.py
```
--------
License
--------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---------------
<p><small>DS200.O21 - Modern Big Data Architecture in Retail Banking - Nguyen Mai Thanh Truc and Nguyen Minh Dat</small></p>
