--------------------------------------------------------------------------
---- 3. CREATE REPORTING RESOURCES
--------------------------------------------------------------------------

--------------------------------------------------------------------------
--- REPORTING ROLES & USERS
--- CREATE A ROLE FOR REPORTING ON PROD DATA
--------------------------------------------------------------------------
use role ACCOUNTADMIN;
CREATE OR REPLACE ROLE identifier($V_ROLE_BI);
GRANT ROLE identifier($V_ROLE_BI) TO ROLE "SYSADMIN";



--------------------------------------------------------------------------
--- CREATE WAREHOUSE(SMALL - NO AUTO CLUSER) FOR INGESTING RAW DATA 
--- Multi Cluster up to 5 clusters for Concurrency
--- WAIT TO SUSPEND 15 mins (900 secs) after last query not to loose cache data 
--------------------------------------------------------------------------

use role SYSADMIN;

CREATE OR REPLACE WAREHOUSE identifier($V_WHNAME_BI) WITH WAREHOUSE_SIZE = 'SMALL' 
WAREHOUSE_TYPE = 'STANDARD' 
INITIALLY_SUSPENDED = TRUE  
AUTO_SUSPEND = 900 
AUTO_RESUME = TRUE 
MIN_CLUSTER_COUNT = 1 
-- MAX_CLUSTER_COUNT = 5 
-- SCALING_POLICY = 'STANDARD' 
COMMENT = 'Used only for BI Users';

--------------------------------------------------------------------------
--- SET REPORTING WAREHOUSE TIMEOUT AFTER 3 hours (10800 secs) 
--- to stop any run-away queries
--------------------------------------------------------------------------
ALTER WAREHOUSE identifier($V_WHNAME_BI) SET STATEMENT_TIMEOUT_IN_SECONDS=10800;


--------------------------------------------------------------------------
--- Assign Usage only access to REPORTING WAREHOUSE
--------------------------------------------------------------------------
GRANT USAGE ON WAREHOUSE identifier($V_WHNAME_BI) TO Role identifier($V_ROLE_BI);


--------------------------------------------------------------------------
----ASSIGN READ-ONLY SECURITY FOR REPORTING ROLE ON REPORTING DB, WH & SCHEMA
--------------------------------------------------------------------------
use role SYSADMIN;

GRANT USAGE ON WAREHOUSE identifier($V_WHNAME_BI)  TO Role identifier($V_ROLE_BI);
grant USAGE On database identifier($V_DBNAME_PROD) to role identifier($V_ROLE_BI);

use database identifier($V_DBNAME_PROD);
grant USAGE On schema identifier($V_SCHEMA_PROD) to role identifier($V_ROLE_BI);

grant SELECT on all tables in schema identifier($V_SCHEMA_PROD) to role identifier($V_ROLE_BI);
use role SECURITYADMIN;
use database identifier($V_DBNAME_PROD);
grant SELECT on FUTURE tables in schema identifier($V_SCHEMA_PROD) to role identifier($V_ROLE_BI);
use role SYSADMIN;



--------------------------------------------------------------------------
---- CREATE A TEST USER FOR REPORTING 
--------------------------------------------------------------------------

use role SECURITYADMIN;
CREATE OR REPLACE USER identifier($V_TESTUSER_BI) PASSWORD = $V_TESTUSER_BI 
LOGIN_NAME = $V_TESTUSER_BI EMAIL = 'UserBI@test.com' 
DEFAULT_ROLE = $V_ROLE_BI 
DEFAULT_WAREHOUSE = $V_WHNAME_BI MUST_CHANGE_PASSWORD = FALSE;

GRANT ROLE identifier($V_ROLE_BI) TO USER identifier($V_TESTUSER_BI);
