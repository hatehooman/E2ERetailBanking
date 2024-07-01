-- Set the initial role and warehouse for import
USE ROLE IMPORT_ROLE;
USE WAREHOUSE IMPORT_WH;
USE DATABASE STAGING;
USE SCHEMA RAW;

-- Example queries to select data (optional)
SELECT * FROM ACCOUNT;
SELECT * FROM C_TRANSACTION;
SELECT * FROM C_ORDER;
SELECT * FROM LOAN;
SELECT * FROM DISPOSITION;
SELECT * FROM CARD;

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

-- Verify the CLEAN.C_ORDER table
SELECT * FROM CLEAN.C_ORDER;

-- Create the CLEAN.C_TRANSACTION table
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

-- Create the CLEAN.DISPOSITION table
CREATE OR REPLACE TABLE CLEAN.DISPOSITION AS
SELECT
    disp_id,
    client_id,
    account_id,
    type AS disp_type
FROM
    RAW.DISPOSITION;

-- Verify the CLEAN.DISPOSITION table
SELECT * FROM CLEAN.DISPOSITION;

-- Create the CLEAN.ACCOUNT table
CREATE OR REPLACE TABLE CLEAN.ACCOUNT AS
SELECT
    account_id,
    district_id,
    frequency AS account_frequency,
    -- Drop parseddate if not needed
    year AS account_year,
    month AS account_month,
    day AS account_day
FROM
    RAW.ACCOUNT;

-- Verify the CLEAN.ACCOUNT table
SELECT * FROM CLEAN.ACCOUNT;

-- Create the CLEAN.CARD table
CREATE OR REPLACE TABLE CLEAN.CARD AS
SELECT
    card_id,
    disp_id,
    type AS card_type,
    year AS card_year,
    month AS card_month,
    day AS card_day
    -- Drop fulldate if not needed
FROM
    RAW.CARD;

-- Verify the CLEAN.CARD table
SELECT * FROM CLEAN.CARD;

-- Move the transformed tables to PROD.REPORTING
-- Set the appropriate role and warehouse for production schema access
USE ROLE TRANSFORM_ROLE;
USE WAREHOUSE ETL_WH;
USE DATABASE STAGING;
USE SCHEMA CLEAN;

-- Move the CLEAN.LOAN table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.LOAN AS
SELECT * FROM STAGING.CLEAN.LOAN;

-- Move the CLEAN.C_ORDER table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.C_ORDER AS
SELECT * FROM STAGING.CLEAN.C_ORDER;

-- Move the CLEAN.C_TRANSACTION table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.C_TRANSACTION AS
SELECT * FROM STAGING.CLEAN.C_TRANSACTION;

-- Move the CLEAN.DISPOSITION table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.DISPOSITION AS
SELECT * FROM STAGING.CLEAN.DISPOSITION;

-- Move the CLEAN.ACCOUNT table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.ACCOUNT AS
SELECT * FROM STAGING.CLEAN.ACCOUNT;

-- Move the CLEAN.CARD table to PROD.REPORTING
CREATE OR REPLACE TABLE PROD.REPORTING.CARD AS
SELECT * FROM STAGING.CLEAN.CARD;

-- Verify the moved tables in PROD.REPORTING
USE ROLE REPORTING_ROLE;
USE WAREHOUSE REPORTING_WH;
USE DATABASE PROD;
SELECT * FROM REPORTING.LOAN;
SELECT * FROM REPORTING.C_ORDER;
SELECT * FROM REPORTING.C_TRANSACTION;
SELECT * FROM REPORTING.DISPOSITION;
SELECT * FROM REPORTING.ACCOUNT;
SELECT * FROM REPORTING.CARD;
