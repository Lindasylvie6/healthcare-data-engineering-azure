-- Create view for fact_claims
CREATE OR ALTER VIEW fact_claims AS
SELECT *
FROM OPENROWSET(
    BULK 'https://adlshospitaldwh.dfs.core.windows.net/gold/fact_claims/',
    FORMAT = 'DELTA'
) AS r;

-- Create view for fact_denials
CREATE OR ALTER VIEW fact_denials AS
SELECT *
FROM OPENROWSET(
    BULK 'https://adlshospitaldwh.dfs.core.windows.net/gold/fact_denials/',
    FORMAT = 'DELTA'
) AS r;

-- Create view for fact_encounters
CREATE OR ALTER VIEW fact_encounters AS
SELECT *
FROM OPENROWSET(
    BULK 'https://adlshospitaldwh.dfs.core.windows.net/gold/fact_encounters/',
    FORMAT = 'DELTA'
) AS r;

-- Create view for dim_patient
CREATE OR ALTER VIEW dim_patient AS
SELECT *
FROM OPENROWSET(
    BULK 'https://adlshospitaldwh.dfs.core.windows.net/gold/dim_patient/',
    FORMAT = 'DELTA'
) AS r;

-- Create view for dim_provider
CREATE OR ALTER VIEW dim_provider AS
SELECT *
FROM OPENROWSET(
    BULK 'https://adlshospitaldwh.dfs.core.windows.net/gold/dim_provider/',
    FORMAT = 'DELTA'
) AS r;

-- Create view for dim_date
CREATE OR ALTER VIEW dim_date AS
SELECT *
FROM OPENROWSET(
    BULK 'https://adlshospitaldwh.dfs.core.windows.net/gold/dim_date/',
    FORMAT = 'DELTA'
) AS r;
