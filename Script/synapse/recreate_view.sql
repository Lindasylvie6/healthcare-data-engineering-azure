USE gold_synapse;

-- Create master key first
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Alpha1&omega123!';


CREATE DATABASE SCOPED CREDENTIAL adls_credential
WITH 
    IDENTITY = 'ad3497a3-a8be-4251-8e01-4b7bc1c781b4@https://login.microsoftonline.com/2be11f7b-4e63-4e64-b8a4-992816fe3359/oauth2/token',
    SECRET = 'r.Z8Q~dtPdES3m64J_CgHnb1-AsUfe6L8tDBma4f';



-- Create external data source with credential
CREATE EXTERNAL DATA SOURCE adls_gold_source
WITH (
    LOCATION = 'https://adlshospitaldwh.dfs.core.windows.net',
    CREDENTIAL = adls_credential
);

-- Recreate all views with credential
USE gold_synapse;

CREATE OR ALTER VIEW fact_claims AS
SELECT * FROM OPENROWSET(
    BULK 'gold/fact_claims/',
    DATA_SOURCE = 'adls_gold_source',
    FORMAT = 'DELTA'
) AS r;

CREATE OR ALTER VIEW fact_denials AS
SELECT * FROM OPENROWSET(
    BULK 'gold/fact_denials/',
    DATA_SOURCE = 'adls_gold_source',
    FORMAT = 'DELTA'
) AS r;

CREATE OR ALTER VIEW fact_encounters AS
SELECT * FROM OPENROWSET(
    BULK 'gold/fact_encounters/',
    DATA_SOURCE = 'adls_gold_source',
    FORMAT = 'DELTA'
) AS r;

CREATE OR ALTER VIEW dim_patient AS
SELECT * FROM OPENROWSET(
    BULK 'gold/dim_patient/',
    DATA_SOURCE = 'adls_gold_source',
    FORMAT = 'DELTA'
) AS r;

CREATE OR ALTER VIEW dim_provider AS
SELECT * FROM OPENROWSET(
    BULK 'gold/dim_provider/',
    DATA_SOURCE = 'adls_gold_source',
    FORMAT = 'DELTA'
) AS r;

CREATE OR ALTER VIEW dim_date AS
SELECT * FROM OPENROWSET(
    BULK 'gold/dim_date/',
    DATA_SOURCE = 'adls_gold_source',
    FORMAT = 'DELTA'
) AS r;
