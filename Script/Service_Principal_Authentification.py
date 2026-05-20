# Configuration (Service Principal Authentication)
storage_account_name = "hospitaldwh"
container_silver = "silver"
container_gold = "gold"
container_bronze = "bronze"
container_landing = "landing"

# Service Principal credentials
application_id = "ad3497a3-a8be-4251-8e01-4b7bc1c781b4"
tenant_id = "2be11f7b-4e63-4e64-b8a4-992816fe3359"
client_secret = "r.Z8Q~dtPdES3m64J_CgHnb1-AsUfe6L8tDBma4f"

# Service Principal with Blob Storage
spark.conf.set(f"fs.azure.account.auth.type.{storage_account_name}.blob.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account_name}.blob.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account_name}.blob.core.windows.net", application_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account_name}.blob.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account_name}.blob.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# Paths
LANDING_PATH = f"wasbs://{container_landing}@{storage_account_name}.blob.core.windows.net/"
BRONZE_PATH = f"wasbs://{container_bronze}@{storage_account_name}.blob.core.windows.net/"
SILVER_PATH = f"wasbs://{container_silver}@{storage_account_name}.blob.core.windows.net/"
GOLD_PATH = f"wasbs://{container_gold}@{storage_account_name}.blob.core.windows.net/"

print("Configuration complete")
print(f"Landing path: {LANDING_PATH}")
print(f"Bronze path: {BRONZE_PATH}")
print(f"Silver path: {SILVER_PATH}")
print(f"Gold path: {GOLD_PATH}")
