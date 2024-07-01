-- Set the initial role and warehouse for import
USE ROLE IMPORT_ROLE;
USE WAREHOUSE IMPORT_WH;
USE DATABASE STAGING;
USE SCHEMA RAW;

-- Example query to select data from ACCOUNT (optional)
SELECT * FROM ACCOUNT;
SELECT * FROM C_TRANSACTION;
SELECT * FROM C_ORDER;
SELECT * FROM LOAN;
-- Switch to the CLEAN schema for data transformation
USE SCHEMA CLEAN;

-- Create the CLEAN.LOAN table
CREATE OR REPLACE TABLE CLEAN.LOAN AS
SELECT
    loan_id,
    account_id,
    duration AS loan_duration,
    payments AS loan_payments,
    status AS loan_status,
    year AS loan_year,
    month AS loan_month,
    day AS loan_day,
    -- Drop fulldate if not needed
    location AS district_id,
    purpose AS loan_purpose
FROM
    RAW.LOAN;

-- Verify the CLEAN.LOAN table
SELECT * FROM CLEAN.LOAN;

-- Create the CLEAN.C_ORDER table
CREATE OR REPLACE TABLE CLEAN.C_ORDER AS
SELECT
    order_id,
    account_id,
    bank_to AS order_bank_to,
    account_to AS order_account_to,
    amount AS order_amount,
    k_symbol AS order_k_symbol
FROM
    RAW.C_ORDER;

-- Verify the CLEAN.ORDER table
SELECT * FROM CLEAN.C_ORDER;

-- Create the CLEAN.TRANSACTION table
CREATE OR REPLACE TABLE CLEAN.C_TRANSACTION AS
SELECT
    trans_id,
    account_id,
    type AS trans_type,
    operation AS operation_type,
    amount AS trans_amount,
    balance AS trans_balance,
    k_symbol AS trans_k_symbol,
    bank AS trans_bank,
    account AS trans_account,
    year AS trans_year,
    month AS trans_month,
    day AS trans_day,
    -- Drop fulldate if not needed
    -- Split fulltime into three columns: trans_hour, trans_min, trans_sec
    SPLIT_PART(fulltime, ':', 1) AS trans_hour,
    SPLIT_PART(fulltime, ':', 2) AS trans_min,
    SPLIT_PART(fulltime, ':', 3) AS trans_sec
    -- Drop fulldatewithtime if not needed
FROM
    RAW.C_TRANSACTION;

-- Verify the CLEAN.C_TRANSACTION table
SELECT * FROM CLEAN.C_TRANSACTION;

-- Move the transformed tables to PROD.REPORTING
-- Set the appropriate role for production schema access
USE ROLE TRANSFORM_ROLE;
USE WAREHOUSE ETL_WH;
-- Switch to the production database and schema
USE DATABASE STAGING;
USE SCHEMA CLEAN;

-- Move the CLEAN.LOAN table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.LOAN AS
SELECT * FROM STAGING.CLEAN.LOAN;

-- Move the CLEAN.ORDER table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.C_ORDER AS
SELECT * FROM STAGING.CLEAN.C_ORDER;

-- Move the CLEAN.TRANSACTION table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.C_TRANSACTION AS
SELECT * FROM STAGING.CLEAN.C_TRANSACTION;

USE ROLE REPORTING_ROLE;
USE WAREHOUSE REPORTING_WH;
USE DATABASE PROD;
-- Verify the moved tables in PROD.REPORTING
SELECT * FROM REPORTING.LOAN;
SELECT * FROM REPORTING.C_ORDER;
SELECT * FROM REPORTING.C_TRANSACTION;
