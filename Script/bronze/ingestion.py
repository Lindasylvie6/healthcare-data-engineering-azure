# Bronze Ingestion - All 9 tables
from pyspark.sql.functions import current_timestamp, input_file_name, lit

tables = [
    "patients",
    "encounters",
    "diagnoses",
    "claims_and_billing",
    "denials",
    "procedures",
    "medications",
    "providers",
    "lab_tests"
]

for table in tables:
    print(f"Ingesting {table}...")
    
    df = spark.read.format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(f"{LANDING_PATH}{table}.csv")
    
    df_bronze = df \
        .withColumn("_ingested_at", current_timestamp()) \
        .withColumn("_source_file", input_file_name()) \
        .withColumn("_layer", lit("bronze"))
    
    df_bronze.write.format("delta") \
        .mode("overwrite") \
        .save(f"{BRONZE_PATH}{table}")
    
    print(f" {table}: {df_bronze.count()} rows written to bronze")

print("\n Bronze ingestion complete!")
