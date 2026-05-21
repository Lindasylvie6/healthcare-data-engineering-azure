# dim_patient
df_dim_patient = spark.sql(""" 
    SELECT
        patient_id,
        first_name,
        last_name,
        dob,
        age,
        CASE 
            WHEN age < 18 THEN 'Under 18'
            WHEN age BETWEEN 18 AND 34 THEN '18-34'
            WHEN age BETWEEN 35 AND 49 THEN '35-49'
            WHEN age BETWEEN 50 AND 64 THEN '50-64'
            ELSE '65+'
        END AS age_group,
        gender,
        ethnicity,
        insurance_type,
        marital_status,
        city,
        state,
        zip,
        registration_date
    FROM patients
""")

df_dim_patient.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}dim_patient")
print(f"dim_patient: {df_dim_patient.count()} rows")

##############################################################################################

# dim_provider
df_dim_provider = spark.sql("""
    SELECT
        provider_id,
        name,
        department,
        specialty,
        npi,
        inhouse,
        location,
        years_experience
    FROM providers
""")

df_dim_provider.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}dim_provider")
print(f" dim_provider: {df_dim_provider.count()} rows")

##############################################################################################

# dim_date
df_dim_date = spark.sql("""
    SELECT DISTINCT
        visit_date AS full_date,
        DAY(visit_date) AS day,
        MONTH(visit_date) AS month,
        DATE_FORMAT(visit_date, 'MMMM') AS month_name,
        QUARTER(visit_date) AS quarter,
        YEAR(visit_date) AS year,
        DATE_FORMAT(visit_date, 'EEEE') AS day_of_week,
        CASE 
            WHEN DAYOFWEEK(visit_date) IN (1,7) THEN 'Yes' 
            ELSE 'No' 
        END AS is_weekend
    FROM encounters
    WHERE visit_date IS NOT NULL
""")

df_dim_date.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}dim_date")
print(f" dim_date: {df_dim_date.count()} rows")

##############################################################################################

# fact_encounters
df_fact_encounters = spark.sql("""
    SELECT
        e.encounter_id,
        e.patient_id,
        e.provider_id,
        e.visit_date,
        e.visit_type,
        e.department,
        e.admission_type,
        e.discharge_date,
        e.length_of_stay,
        e.status,
        e.readmitted_flag,
        e.diagnosis_code,
        CASE 
            WHEN p.age < 18 THEN 'Under 18'
            WHEN p.age BETWEEN 18 AND 34 THEN '18-34'
            WHEN p.age BETWEEN 35 AND 49 THEN '35-49'
            WHEN p.age BETWEEN 50 AND 64 THEN '50-64'
            ELSE '65+'
        END AS age_group,
        p.gender,
        p.ethnicity,
        p.insurance_type,
        p.city,
        p.state,
        p.zip,
        YEAR(e.visit_date) AS visit_year,
        MONTH(e.visit_date) AS visit_month,
        DATE_FORMAT(e.visit_date, 'MMMM') AS visit_month_name,
        QUARTER(e.visit_date) AS visit_quarter
    FROM encounters e
    LEFT JOIN patients p ON e.patient_id = p.patient_id
""")

df_fact_encounters.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}fact_encounters")
print(f" fact_encounters: {df_fact_encounters.count()} rows")

##############################################################################################

# fact_claims
df_fact_claims = spark.sql("""
    SELECT
        c.billing_id,
        c.patient_id,
        c.encounter_id,
        c.claim_id,
        c.insurance_provider,
        c.payment_method,
        c.claim_billing_date,
        c.billed_amount,
        c.paid_amount,
        c.billed_amount - c.paid_amount AS unpaid_amount,
        c.claim_status,
        c.denial_reason,
        CASE 
            WHEN p.age < 18 THEN 'Under 18'
            WHEN p.age BETWEEN 18 AND 34 THEN '18-34'
            WHEN p.age BETWEEN 35 AND 49 THEN '35-49'
            WHEN p.age BETWEEN 50 AND 64 THEN '50-64'
            ELSE '65+'
        END AS age_group,
        p.gender,
        p.ethnicity,
        p.city,
        p.state,
        p.zip,
        YEAR(c.claim_billing_date) AS claim_year,
        MONTH(c.claim_billing_date) AS claim_month,
        DATE_FORMAT(c.claim_billing_date, 'MMMM') AS claim_month_name,
        QUARTER(c.claim_billing_date) AS claim_quarter
    FROM claims_and_billing c
    LEFT JOIN patients p ON c.patient_id = p.patient_id
""")

df_fact_claims.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}fact_claims")
print(f" fact_claims: {df_fact_claims.count()} rows")

##############################################################################################

# fact_denials
df_fact_denials = spark.sql("""
    SELECT
        d.denial_id,
        d.claim_id,
        d.denial_reason_code,
        d.denial_reason_description,
        d.denied_amount,
        d.denial_date,
        d.appeal_filed,
        d.appeal_status,
        d.appeal_resolution_date,
        d.final_outcome,
        c.patient_id,
        c.insurance_provider,
        c.billed_amount,
        c.paid_amount,
        CASE 
            WHEN p.age < 18 THEN 'Under 18'
            WHEN p.age BETWEEN 18 AND 34 THEN '18-34'
            WHEN p.age BETWEEN 35 AND 49 THEN '35-49'
            WHEN p.age BETWEEN 50 AND 64 THEN '50-64'
            ELSE '65+'
        END AS age_group,
        p.gender,
        p.ethnicity,
        p.city,
        p.state,
        p.zip,
        YEAR(d.denial_date) AS denial_year,
        MONTH(d.denial_date) AS denial_month,
        DATE_FORMAT(d.denial_date, 'MMMM') AS denial_month_name,
        QUARTER(d.denial_date) AS denial_quarter
    FROM denials d
    LEFT JOIN claims_and_billing c ON d.claim_id = c.claim_id
    LEFT JOIN patients p ON c.patient_id = p.patient_id
""")

df_fact_denials.write.format("delta").mode("overwrite").save(f"{GOLD_PATH}fact_denials")
print(f" fact_denials: {df_fact_denials.count()} rows")

