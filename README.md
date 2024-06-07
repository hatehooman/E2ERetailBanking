<h1 align="center">Modern Big Data Architecture in Retail Banking</h1>

<p align="center"><small>Faculty of Information Science and Engineering, University of Information Technology, Ho Chi Minh City, Viet Nam <br>
Vietnam National University, Ho Chi Minh City, Viet Nam
</small></p>




Contributors
--------------------- 

<div align="center">
  <table>
    <tr>
      <th>Student's ID</th>
      <th>Fullname</th>
      <th>Contact</th>
    </tr>
    <tr>
      <td>21522721</td>
      <td>Nguyen Mai Thanh Truc</td>
      <td>21522721@gm.uit.edu.vn</td>
    </tr>
    <tr>
      <td>21521937</td>
      <td>Nguyen Minh Dat</td>
      <td>21521937@gm.uit.edu.vn</td>
    </tr>
  </table>
</div>


----------------
Description
----------------

--------------
Retail Banking's Architecture
-------------
![Pipeline](./Architecture/Retail%20Banking%20System.png)
---------------
ER Diagram of Retail Banking Database
---------------
![ER-Diagram](./ER%20Diagram/ER-Diagram.png)

Technologies
----------------
1. Apache Spark
2. Apache Kafka
3. Apache ZooKeeper
4. Debezium Connetor
5. Snowflake - Cloud Data Warehouse
6. PostgreSQL
7. Docker
8. Python
---------------




Data Pipeline
----------------
1. Data Collection
2. Data Ingestion
3. Data Storage
4. Data Exploration
5. Data Analyzing
6. Model Training



Project Organization
------------


```
└── 📁Big-Data-Analytics-Final-Project
    └── .env
    └── 📁Architecture
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
        └── Retail-Banking-Demo-Data.zip
    └── docker_compose.yml
    └── 📁ER Diagram
        └── ER-Diagram.png
    └── LICENSE
    └── Makefile
    └── packages.txt
    └── README.md
    └── 📁Report
    └── requirements.txt
    └── 📁Snowflake Data Warehouse
        └── 1 - MODIFY.sql
        └── 2 - IMPORT RESOURCE.sql
        └── 3 - TRANSFORM RESOURCE.sql
        └── 4 - REPORTING RESOURCE.sql
        └── 5 - RESOURCE MONITORS.sql
    └── 📁src
        └── 📁components
        └── __init__.py
```

--------

<p><small>DS200.O21 - Modern Big Data Architecture in Retail Banking - Nguyen Mai Thanh Truc - Nguyen Minh Dat</small></p>
