from google.cloud import bigquery

# Instantiate a BigQuery client
#client = bigquery.Client()

CREDENTIALS_FILE = "gcs.json"
client = bigquery.Client.from_service_account_json(CREDENTIALS_FILE)

# Define the dataset and table name
#dataset_id = 'serene-art-448820-d8.dwol_de_zoomcamp'
dataset_id = 'dwol_de_zoomcamp'

table_id = 'dwol_yellow_tripdata_2024_external_02'

BUCKET_NAME = "dwol-de-zoomcamp-bucket"

# Define the dataset and table names
materialized_view_id = 'dwol_yellow_tripdata_2024_materialized_view'

# Step 1: Load data from GCS into a regular table (same as the previous script)
#uri = f'gs://{BUCKET_NAME}/*.parquet'
uri = f'gs://{BUCKET_NAME}/dwol_*.parquet'  # Wildcard to load multiple Parquet files


# # Define the external table configuration
# external_config = bigquery.ExternalConfig(bigquery.SourceFormat.PARQUET)
# external_config.autodetect = True
# external_config.source_uris = [uri]  # List of URIs

# # Define the table reference
# table_ref = client.dataset(dataset_id).table(table_id)

# # Define the table object and attach the external configuration
# table = bigquery.Table(table_ref)
# table.external_data_configuration = external_config  # Correct way to assign ExternalConfig

# # Create the external table in BigQuery
# table = client.create_table(table)  # This will create the external table

# print(f'Created external table {table_id} in dataset {dataset_id}')


# Define table reference
table_ref = client.dataset(dataset_id).table(table_id)

# Configure the load job
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,  # Specify Parquet format
    autodetect=True,  # Automatically infer schema
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Overwrite table if exists
)

# Load data from GCS into BigQuery
load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)

# Wait for the job to complete
load_job.result()

print(f'Successfully created native table {table_id} in dataset {dataset_id}')



# Step 2: Create a Materialized View based on the regular table
materialized_view_query = f"""
    CREATE MATERIALIZED VIEW `{dataset_id}.{materialized_view_id}`
    AS
    SELECT * FROM `{dataset_id}.{table_id}`;
"""

# Run the query to create the materialized view
query_job = client.query(materialized_view_query)

# Wait for the query to complete
query_job.result()

print(f'Created materialized view {dataset_id}.{materialized_view_id}')
