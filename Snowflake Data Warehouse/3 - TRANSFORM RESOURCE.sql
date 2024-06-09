--------------------------------------------------------------------------
---- 2. CREATE TRANSFORM RESOURCES
--------------------------------------------------------------------------

--------------------------------------------------------------------------
-- CREATE A ROLE FOR TRANSFORMING DATA
--------------------------------------------------------------------------

use role ACCOUNTADMIN;
CREATE ROLE identifier($V_ROLE_TRANSFORM);
GRANT ROLE identifier($V_ROLE_TRANSFORM) TO ROLE "SYSADMIN";

--------------------------------------------------------------------------
--- CREATE WAREHOUSE(SMALL - NO AUTO CLUSER) FOR INGESTING RAW DATA 
--- SUSPEND after 5 mins (300 secs) AFTER INGESTION JOBS ARE COMPLETE
--------------------------------------------------------------------------
use role SYSADMIN;

CREATE OR REPLACE WAREHOUSE identifier($V_WHNAME_TRANSFORM) WITH WAREHOUSE_SIZE = 'MEDIUM' 
WAREHOUSE_TYPE = 'STANDARD' 
INITIALLY_SUSPENDED = TRUE  
AUTO_SUSPEND = 300 
AUTO_RESUME = TRUE 
MIN_CLUSTER_COUNT = 1 
MAX_CLUSTER_COUNT = 1 
-- SCALING_POLICY = 'STANDARD' 
COMMENT = 'Used only for ETL/Transform';

GRANT USAGE ON WAREHOUSE identifier($V_WHNAME_TRANSFORM) TO Role identifier($V_ROLE_TRANSFORM);


--------------------------------------------------------------------------
--- CREATE PROD DB, SCHEMA, SAMPLE TABLE
--------------------------------------------------------------------------

use role SYSADMIN;
CREATE DATABASE identifier($V_DBNAME_PROD);

--------------------------------------------------------------------------
--- Default Data Retension is set to max 90 days for REPORTING Schema 
--- since this is used for prod reporting 
--------------------------------------------------------------------------
create schema identifier($V_SCHEMA_PROD) DATA_RETENTION_TIME_IN_DAYS = 1;
show schemas;

use DATABASE identifier($V_DBNAME_PROD);
use schema identifier($V_SCHEMA_PROD);
CREATE TABLE WEBLOGS ("IMPORTDATE" TIMESTAMP default current_timestamp(), "S1" STRING);

--------------------------------------------------------------------------
---- ASSIGN READ/WRITE SECURITY ON PROD FOR TRANSFORM ROLE
--------------------------------------------------------------------------

grant USAGE On database identifier($V_DBNAME_PROD) to role identifier($V_ROLE_TRANSFORM);
grant ALL privileges On schema identifier($V_SCHEMA_PROD) to role identifier($V_ROLE_TRANSFORM);

--------------------------------------------------------------------------
-- Full access for Transform Role to PROD schema & existing tables
--------------------------------------------------------------------------
grant ALL privileges on all tables in schema identifier($V_SCHEMA_PROD) to role identifier($V_ROLE_TRANSFORM);
use role SECURITYADMIN;


use role SYSADMIN;
grant ALL privileges on database identifier($V_DBNAME_PROD) to role SECURITYADMIN;
grant ALL privileges on schema identifier($V_SCHEMA_PROD) to role SECURITYADMIN;
use role securityadmin;

use DATABASE identifier($V_DBNAME_PROD);
use schema identifier($V_SCHEMA_PROD);

--------------------------------------------------------------------------
-- Full access for Transform Role to future tables
--------------------------------------------------------------------------
grant ALL privileges on FUTURE tables in schema identifier($V_SCHEMA_PROD) to role identifier($V_ROLE_TRANSFORM);
use role SYSADMIN;

--------------------------------------------------------------------------
-- Assign Usage Only access to Transform Warehouse (No resize or modifications)
-- Assign Usage on ETL database
-- Assign full access to CLEAN Schema under ETL dataabase
-- Assign full access to current & future tables in CLEAN Schema under ETL dataabase
--------------------------------------------------------------------------


GRANT USAGE ON WAREHOUSE identifier($V_WHNAME_TRANSFORM) TO Role identifier($V_ROLE_TRANSFORM);
grant USAGE On database identifier($V_DBNAME_ETL) to role identifier($V_ROLE_TRANSFORM);

use database identifier($V_DBNAME_ETL);
grant ALL privileges On schema identifier($V_SCHEMA_CLEAN) to role identifier($V_ROLE_TRANSFORM);
grant ALL privileges on all tables in schema identifier($V_SCHEMA_CLEAN) to role identifier($V_ROLE_TRANSFORM);
use role SECURITYADMIN;
grant ALL privileges on FUTURE tables in schema identifier($V_SCHEMA_CLEAN) to role identifier($V_ROLE_TRANSFORM);
use role SYSADMIN;

--------------------------------------------------------------------------
---- CREATE A TEST USER FOR TRANSFORM ROLE 
--------------------------------------------------------------------------

use role SECURITYADMIN;

CREATE OR REPLACE USER identifier($V_TESTUSER_TRANSFORM) PASSWORD = $V_TESTUSER_TRANSFORM
LOGIN_NAME = $V_TESTUSER_TRANSFORM EMAIL = 'UserETL@test.com' 
DEFAULT_ROLE = $V_ROLE_TRANSFORM
DEFAULT_WAREHOUSE = $V_WHNAME_TRANSFORM MUST_CHANGE_PASSWORD = FALSE;

GRANT ROLE identifier($V_ROLE_TRANSFORM) TO USER identifier($V_TESTUSER_TRANSFORM);