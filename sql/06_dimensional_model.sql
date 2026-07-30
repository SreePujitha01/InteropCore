USE DATABASE INTEROPCORE;
CREATE SCHEMA IF NOT EXISTS INTEROPCORE.ANALYTICS;
USE SCHEMA ANALYTICS;

CREATE OR REPLACE TABLE DIM_PATIENT AS
SELECT
    Id AS patient_id, FIRST AS first_name, LAST AS last_name, BIRTHDATE AS birth_date,
    GENDER AS gender, RACE AS race, ETHNICITY AS ethnicity, CITY AS city, STATE AS state,
    ZIP AS zip_code, MARITAL AS marital_status
FROM RAW.RAW_PATIENTS;

CREATE OR REPLACE TABLE DIM_DATE AS
SELECT
    DATEADD(day, seq4(), '2000-01-01') AS date_key,
    YEAR(DATEADD(day, seq4(), '2000-01-01')) AS year,
    MONTH(DATEADD(day, seq4(), '2000-01-01')) AS month,
    DAY(DATEADD(day, seq4(), '2000-01-01')) AS day,
    DAYNAME(DATEADD(day, seq4(), '2000-01-01')) AS day_name,
    QUARTER(DATEADD(day, seq4(), '2000-01-01')) AS quarter
FROM TABLE(GENERATOR(ROWCOUNT => 10950));

CREATE OR REPLACE TABLE DIM_PROVIDER AS
SELECT
    Id AS provider_id, ORGANIZATION AS organization_id, NAME AS provider_name,
    GENDER AS gender, SPECIALITY AS speciality
FROM RAW.RAW_PROVIDERS;

CREATE OR REPLACE TABLE DIM_ORGANIZATION AS
SELECT
    Id AS organization_id, NAME AS organization_name, CITY AS city, STATE AS state,
    ZIP AS zip_code, PHONE AS phone
FROM RAW.RAW_ORGANIZATIONS;

CREATE OR REPLACE TABLE FACT_ENCOUNTER AS
SELECT
    Id AS encounter_id, PATIENT AS patient_id, ORGANIZATION AS organization_id,
    PROVIDER AS provider_id, "START" AS start_datetime, "STOP" AS stop_datetime,
    DATE("START") AS start_date_key, ENCOUNTERCLASS AS encounter_class, CODE AS encounter_code,
    DESCRIPTION AS encounter_description, BASE_ENCOUNTER_COST AS base_cost,
    TOTAL_CLAIM_COST AS total_claim_cost, PAYER_COVERAGE AS payer_coverage
FROM RAW.RAW_ENCOUNTERS;

CREATE OR REPLACE TABLE FACT_CONDITION AS
SELECT
    PATIENT AS patient_id, ENCOUNTER AS encounter_id, "START" AS onset_date_key,
    SYSTEM AS coding_system, CODE AS condition_code, DESCRIPTION AS condition_description
FROM RAW.RAW_CONDITIONS;

CREATE OR REPLACE TABLE FACT_MEDICATION AS
SELECT
    PATIENT AS patient_id, ENCOUNTER AS encounter_id, "START" AS start_date_key,
    "STOP" AS stop_date_key, CODE AS medication_code, DESCRIPTION AS medication_description,
    BASE_COST AS base_cost, TOTALCOST AS total_cost, DISPENSES AS dispenses
FROM RAW.RAW_MEDICATIONS;

CREATE OR REPLACE TABLE FACT_ALLERGY AS
SELECT
    PATIENT AS patient_id, ENCOUNTER AS encounter_id, "START" AS onset_date_key,
    CODE AS allergy_code, DESCRIPTION AS allergy_description, CATEGORY AS category,
    REACTION1 AS reaction_1, SEVERITY1 AS severity_1
FROM RAW.RAW_ALLERGIES;

-- USCDI v3/v4 mapping documentation
COMMENT ON TABLE DIM_PATIENT IS 'Maps to USCDI v3 Data Class: Patient Demographics/Information';
COMMENT ON TABLE FACT_ENCOUNTER IS 'Maps to USCDI v3 Data Class: Encounter Information';
COMMENT ON TABLE FACT_CONDITION IS 'Maps to USCDI v3 Data Class: Problems';
COMMENT ON TABLE DIM_PROVIDER IS 'Maps to USCDI v3 Data Class: Care Team Member(s)';
COMMENT ON TABLE DIM_ORGANIZATION IS 'Maps to USCDI v4 Data Class: Facility Information';
COMMENT ON TABLE FACT_MEDICATION IS 'Maps to USCDI v3 Data Class: Medications';
COMMENT ON TABLE FACT_ALLERGY IS 'Maps to USCDI v3 Data Class: Allergies and Intolerances';