Data Warehouse Set Up Detail
----------------
### How to set up

Put all the .sql script which we have provide in `./Snowflake Data Warehouse` folder into SQL Worksheet in Snowflake Data Warehouse Workspace and compile its.
- `1 - MODIFY.sql` : Modify Warehouses, Databases, Schemas, Users, Roles.
- `2 - IMPORT RESOURCE.sql`: Set up IMPORT WAREHOUSE.
- `3 - TRANSFORM RESOURCE.sql`: Set up TRANSFORM WAREHOUSE.
- `4 - REPORTING RESOURCE.sql`: Set up REPORTING WAREHOUSE.
- `5 - RESOURCE MONITOR.sql`: Handle credit usage & abort.

### After set up, we have 3-stage Data Warehouse which show below:
     
### 1. STAGING DATABASE
![Stage](./Warehouse/1%20-%20STAGING%20DETAIL.png)
### 1.1. SCHEMA: STAGING.RAW
![RAW](./Warehouse/1.1%20-%20RAW.png)
### 1.2. SCHEMA: STAGING.CLEAN
![CLEAN](./Warehouse/1.2%20-%20CLEAN.png)
### 2. PROB DATABASE
![PROD](./Warehouse/2%20-%20PROD%20DETAIL.png)
### 2.1. SCHEMA: PROD.REPORTING
![REPORTING](./Warehouse/2.1%20-%20REPORTING.png)

### 3. ALL WAREHOUSE CREATED
![WH](./Warehouse/3%20-%20Warehouse%20Created.png)
