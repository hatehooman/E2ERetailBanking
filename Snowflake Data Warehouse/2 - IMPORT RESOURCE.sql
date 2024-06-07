--------------------------------------------------------------------------
---    1. CREATE IMPORT RESOURCES    
--------------------------------------------------------------------------


-- CREATE A ROLE FOR INGESTING DATA
use role ACCOUNTADMIN;
CREATE OR REPLACE ROLE identifier($V_ROLE_IMPORT);
GRANT ROLE identifier($V_ROLE_IMPORT) TO ROLE "SYSADMIN";


--------------------------------------------------------------------------
--- CREATE WAREHOUSE(MEDIUM - NO AUTO CLUSER) FOR INGESTING RAW DATA 
--- SUSPEND after 5 mins (300 secs) AFTER INGESTION JOBS ARE COMPLETE
--------------------------------------------------------------------------

use role SYSADMIN;

CREATE OR REPLACE WAREHOUSE identifier($V_WHNAME_IMPORT) WITH WAREHOUSE_SIZE = 'MEDIUM' 
WAREHOUSE_TYPE = 'STANDARD' 
INITIALLY_SUSPENDED = TRUE  
AUTO_SUSPEND = 300 
AUTO_RESUME = TRUE 
MIN_CLUSTER_COUNT = 1 
MAX_CLUSTER_COUNT = 1 
-- SCALING_POLICY = 'STANDARD' 
COMMENT = 'Used only for ingesting raw data';

GRANT USAGE ON WAREHOUSE identifier($V_WHNAME_IMPORT) TO Role identifier($V_ROLE_IMPORT);



--------------------------------------------------------------------------
--- CREATE DB, SCHEMA, TABLE, STAGE & CUSTOM_FILEFORMAT  
--- Default Data Retension for Import Schema is 3 days. 
--------------------------------------------------------------------------

use role SYSADMIN;
CREATE DATABASE identifier($V_DBNAME_ETL);

create schema identifier($V_SCHEMA_IMPORT) DATA_RETENTION_TIME_IN_DAYS = 1;

use database identifier($V_DBNAME_ETL);
use schema identifier($V_SCHEMA_IMPORT);



--------------------------------------------------------------------------
--- CREATE SAMPLE TABLE  
--------------------------------------------------------------------------
CREATE TABLE JSON_WEBLOGS ("IMPORTDATE" TIMESTAMP default current_timestamp(), "CONTENT" VARIANT);

--------------------------------------------------------------------------
--- CREATE IMPORT STAGE & SAMPLE JSON FILE FORMAT
--------------------------------------------------------------------------

--create or replace stage IMPORT_STAGE
--url='azure://something.blob.core.windows.net/somefolder'
--credentials=(azure_sas_token='YourSasToken')
--file_format = (type = 'CSV');




CREATE FILE FORMAT MYJSON 
TYPE = 'JSON' 
COMPRESSION = 'AUTO' 
ENABLE_OCTAL = FALSE 
ALLOW_DUPLICATE = FALSE 
STRIP_OUTER_ARRAY = TRUE 
STRIP_NULL_VALUES = FALSE 
IGNORE_UTF8_ERRORS = TRUE;




--------------------------------------------------------------------------
---     CREATE CLEAN SCHEMA UNDER STAGING
---     DEFAULT DATA_RETENSION for CLEAN Schema is 3 days
--------------------------------------------------------------------------

create schema identifier($V_SCHEMA_CLEAN) DATA_RETENTION_TIME_IN_DAYS = 1;
use schema identifier($V_SCHEMA_CLEAN) ;


--------------------------------------------------------------------------
--- CREATE SAMPLE TABLE UNDER CLEAN SCHEMA
--------------------------------------------------------------------------
CREATE TABLE WEBLOGS ("IMPORTDATE" TIMESTAMP , C1 STRING, C2 STRING);

--------------------------------------------------------------------------
----        ASSIGN SECURITY ON OBJECTS
--------------------------------------------------------------------------


GRANT USAGE ON WAREHOUSE identifier($V_WHNAME_IMPORT) TO Role identifier($V_ROLE_IMPORT);
grant USAGE On database identifier($V_DBNAME_ETL) to role identifier($V_ROLE_IMPORT);

use schema identifier($V_SCHEMA_IMPORT) ;
grant ALL privileges On schema identifier($V_SCHEMA_IMPORT) to role identifier($V_ROLE_IMPORT);

use schema identifier($V_SCHEMA_CLEAN) ;
grant ALL privileges On schema identifier($V_SCHEMA_CLEAN) to role identifier($V_ROLE_IMPORT);

--use schema identifier($V_SCHEMA_IMPORT) ;
--grant USAGE On stage IMPORT_STAGE to role identifier($V_ROLE_IMPORT);

use schema identifier($V_SCHEMA_IMPORT) ;
grant USAGE On FILE FORMAT MYJSON  to role identifier($V_ROLE_IMPORT);

--------------------------------------------------------------------------
-- GIVE IMPORT_ROLE FULL ACCESS TO ANY EXITING TABLES 
--------------------------------------------------------------------------

grant ALL privileges on all tables in schema identifier($V_SCHEMA_IMPORT) to role identifier($V_ROLE_IMPORT);
grant ALL privileges on all tables in schema identifier($V_SCHEMA_CLEAN) to role identifier($V_ROLE_IMPORT);
use role SYSADMIN;

--------------------------------------------------------------------------
--- GIVE FULL ACESS TO SECURITYADMIN
--------------------------------------------------------------------------

grant ALL privileges on database identifier($V_DBNAME_ETL) to role SECURITYADMIN;
grant ALL privileges on schema identifier($V_SCHEMA_CLEAN) to role SECURITYADMIN;
grant ALL privileges on schema identifier($V_SCHEMA_IMPORT) to role SECURITYADMIN;
use role securityadmin;
use database identifier($V_DBNAME_ETL);

--------------------------------------------------------------------------
-- GIVE IMPORT_ROLE FULL ACCESS TO ANY FUTURE TABLES 
--------------------------------------------------------------------------

grant ALL privileges on FUTURE tables in schema identifier($V_SCHEMA_IMPORT) to role identifier($V_ROLE_IMPORT);
grant ALL privileges on FUTURE tables in schema identifier($V_SCHEMA_CLEAN) to role identifier($V_ROLE_IMPORT);
use role SYSADMIN;

--------------------------------------------------------------------------
---- CREATE A TEST IMPORT USER 
--------------------------------------------------------------------------

use role SECURITYADMIN;
CREATE OR REPLACE USER identifier($V_TESTUSER_IMPORT) PASSWORD = $V_TESTUSER_IMPORT
LOGIN_NAME = $V_TESTUSER_IMPORT EMAIL = 'userimport@test.com' 
DEFAULT_ROLE = $V_ROLE_IMPORT
DEFAULT_WAREHOUSE = $V_WHNAME_IMPORT MUST_CHANGE_PASSWORD = FALSE;

GRANT ROLE identifier($V_ROLE_IMPORT) TO USER identifier($V_TESTUSER_IMPORT) ;
