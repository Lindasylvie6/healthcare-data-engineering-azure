# Create Silver Views for SQL querying
spark.read.format("delta").load(f"{SILVER_PATH}patients").createOrReplaceTempView("patients")
spark.read.format("delta").load(f"{SILVER_PATH}encounters").createOrReplaceTempView("encounters")
spark.read.format("delta").load(f"{SILVER_PATH}diagnoses").createOrReplaceTempView("diagnoses")
spark.read.format("delta").load(f"{SILVER_PATH}claims_and_billing").createOrReplaceTempView("claims_and_billing")
spark.read.format("delta").load(f"{SILVER_PATH}denials").createOrReplaceTempView("denials")
spark.read.format("delta").load(f"{SILVER_PATH}procedures").createOrReplaceTempView("procedures")
spark.read.format("delta").load(f"{SILVER_PATH}medications").createOrReplaceTempView("medications")
spark.read.format("delta").load(f"{SILVER_PATH}providers").createOrReplaceTempView("providers")
spark.read.format("delta").load(f"{SILVER_PATH}lab_tests").createOrReplaceTempView("lab_tests")

print("All silver views created, ready for SQL!")
