# Configuration (Service Principal + ADLS Gen2)
storage_account_name = "adlshospitaldwh"
container_landing = "landing"
container_bronze = "bronze"
container_silver = "silver"
container_gold = "gold"

# Service Principal credentials
application_id = "ad3497a3-a8be-4251-8e01-4b7bc1c781b4"
tenant_id = "2be11f7b-4e63-4e64-b8a4-992816fe3359"
client_secret = "*************************"

# Configure Service Principal authentication
spark.conf.set(f"fs.azure.account.auth.type.{storage_account_name}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account_name}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account_name}.dfs.core.windows.net", application_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account_name}.dfs.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account_name}.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# Paths
LANDING_PATH = f"abfss://{container_landing}@{storage_account_name}.dfs.core.windows.net/"
BRONZE_PATH = f"abfss://{container_bronze}@{storage_account_name}.dfs.core.windows.net/"
SILVER_PATH = f"abfss://{container_silver}@{storage_account_name}.dfs.core.windows.net/"
GOLD_PATH = f"abfss://{container_gold}@{storage_account_name}.dfs.core.windows.net/"

print("Configuration complete")
print(f"Landing path: {LANDING_PATH}")
print(f"Bronze path: {GOLD_PATH}")
