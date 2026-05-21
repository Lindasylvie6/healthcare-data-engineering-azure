# Patients
from pyspark.sql.functions import col, trim, upper, round, to_date

df_patients = spark.read.format("delta").load(f"{BRONZE_PATH}patients")

df_patients_silver = df_patients \
    .withColumn("dob", to_date(col("dob"), "yyyy-MM-dd")) \
    .withColumn("registration_date", to_date(col("registration_date"), "yyyy-MM-dd")) \
    .withColumn("gender", trim(upper(col("gender")))) \
    .withColumn("ethnicity", trim(upper(col("ethnicity")))) \
    .withColumn("insurance_type", trim(upper(col("insurance_type")))) \
    .withColumn("marital_status", trim(upper(col("marital_status")))) \
    .dropDuplicates(["patient_id"])

df_patients_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}patients")

print(f" Patients silver count: {df_patients_silver.count()}")


#####################################################################################################

# Encounters
from pyspark.sql.functions import col, trim, upper, to_date

df_encounters = spark.read.format("delta").load(f"{BRONZE_PATH}encounters")

df_encounters_silver = df_encounters \
    .withColumn("visit_date", to_date(col("visit_date"), "yyyy-MM-dd")) \
    .withColumn("discharge_date", to_date(col("discharge_date"), "yyyy-MM-dd")) \
    .withColumn("visit_type", trim(upper(col("visit_type")))) \
    .withColumn("department", trim(upper(col("department")))) \
    .withColumn("admission_type", trim(upper(col("admission_type")))) \
    .withColumn("status", trim(upper(col("status")))) \
    .withColumn("readmitted_flag", trim(upper(col("readmitted_flag")))) \
    .dropDuplicates(["encounter_id"])

df_encounters_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}encounters")

print(f" Encounters silver count: {df_encounters_silver.count()}")


#####################################################################################################

# Diagnoses (full row dedup - no unique ID)
from pyspark.sql.functions import col, trim, upper, to_date, round

df_diagnoses = spark.read.format("delta").load(f"{BRONZE_PATH}diagnoses")

df_diagnoses_silver = df_diagnoses \
    .withColumn("diagnosis_code", trim(upper(col("diagnosis_code")))) \
    .withColumn("diagnosis_description", trim(col("diagnosis_description"))) \
    .dropDuplicates()

df_diagnoses_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}diagnoses")
print(f" Diagnoses: {df_diagnoses_silver.count()}")

#####################################################################################################

# Claims and Billing
df_claims = spark.read.format("delta").load(f"{BRONZE_PATH}claims_and_billing")

df_claims_silver = df_claims \
    .withColumn("claim_billing_date", to_date(col("claim_billing_date"), "yyyy-MM-dd")) \
    .withColumn("billed_amount", round(col("billed_amount"), 2)) \
    .withColumn("paid_amount", round(col("paid_amount"), 2)) \
    .withColumn("insurance_provider", trim(upper(col("insurance_provider")))) \
    .withColumn("payment_method", trim(upper(col("payment_method")))) \
    .withColumn("claim_status", trim(upper(col("claim_status")))) \
    .withColumn("denial_reason", trim(col("denial_reason"))) \
    .dropDuplicates(["billing_id"])

df_claims_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}claims_and_billing")
print(f" Claims & Billing: {df_claims_silver.count()}")

#####################################################################################################

# Denials
df_denials = spark.read.format("delta").load(f"{BRONZE_PATH}denials")

df_denials_silver = df_denials \
    .withColumn("denial_date", to_date(col("denial_date"), "yyyy-MM-dd")) \
    .withColumn("appeal_resolution_date", to_date(col("appeal_resolution_date"), "yyyy-MM-dd")) \
    .withColumn("denied_amount", round(col("denied_amount"), 2)) \
    .withColumn("denial_reason_code", trim(upper(col("denial_reason_code")))) \
    .withColumn("appeal_filed", trim(upper(col("appeal_filed")))) \
    .withColumn("appeal_status", trim(upper(col("appeal_status")))) \
    .withColumn("final_outcome", trim(upper(col("final_outcome")))) \
    .dropDuplicates(["denial_id"])

df_denials_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}denials")
print(f" Denials: {df_denials_silver.count()}")

#####################################################################################################

# Procedures (full row dedup - no unique ID)
df_procedures = spark.read.format("delta").load(f"{BRONZE_PATH}procedures")

df_procedures_silver = df_procedures \
    .withColumn("procedure_date", to_date(col("procedure_date"), "yyyy-MM-dd")) \
    .withColumn("procedure_code", trim(upper(col("procedure_code")))) \
    .withColumn("procedure_description", trim(col("procedure_description"))) \
    .withColumn("procedure_cost", round(col("procedure_cost"), 2)) \
    .dropDuplicates()

df_procedures_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}procedures")
print(f" Procedures: {df_procedures_silver.count()}")


#####################################################################################################

# Silver Medications (full row dedup - no unique ID)
df_medications = spark.read.format("delta").load(f"{BRONZE_PATH}medications")

df_medications_silver = df_medications \
    .withColumn("prescribed_date", to_date(col("prescribed_date"), "yyyy-MM-dd")) \
    .withColumn("drug_name", trim(upper(col("drug_name")))) \
    .withColumn("route", trim(upper(col("route")))) \
    .withColumn("frequency", trim(upper(col("frequency")))) \
    .withColumn("cost", round(col("cost"), 2)) \
    .dropDuplicates()

df_medications_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}medications")
print(f" Medications fixed count: {df_medications_silver.count()}")

#####################################################################################################

# Silver Providers
df_providers = spark.read.format("delta").load(f"{BRONZE_PATH}providers")

df_providers_silver = df_providers \
    .withColumn("specialty", trim(upper(col("specialty")))) \
    .withColumn("department", trim(upper(col("department")))) \
    .withColumn("location", trim(upper(col("location")))) \
    .withColumn("inhouse", trim(upper(col("inhouse")))) \
    .dropDuplicates(["provider_id"])

df_providers_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}providers")
print(f" Providers: {df_providers_silver.count()}")

#####################################################################################################

# Lab Tests (full row dedup - no unique ID)
df_lab_tests = spark.read.format("delta").load(f"{BRONZE_PATH}lab_tests")

df_lab_tests_silver = df_lab_tests \
    .withColumn("test_date", to_date(col("test_date"), "yyyy-MM-dd")) \
    .withColumn("test_name", trim(upper(col("test_name")))) \
    .withColumn("test_code", trim(upper(col("test_code")))) \
    .withColumn("specimen_type", trim(upper(col("specimen_type")))) \
    .withColumn("status", trim(upper(col("status")))) \
    .dropDuplicates()

df_lab_tests_silver.write.format("delta").mode("overwrite").save(f"{SILVER_PATH}lab_tests")
print(f" Lab Tests: {df_lab_tests_silver.count()}")
