from google.cloud import bigquery

# Instantiate a BigQuery client

#If you authenticated through the GCP SDK you can comment out these two lines
CREDENTIALS_FILE = "gcs.json"
client = bigquery.Client.from_service_account_json(CREDENTIALS_FILE)
#client = bigquery.Client()

# Define the dataset and table name
#dataset_id = 'serene-art-448820-d8.dwol_de_zoomcamp'
dataset_id = 'dwol_de_zoomcamp'

#dwol_de_zoomcamp


table_id = 'dwol_yellow_tripdata_2024_external_01'


BUCKET_NAME = "dwol-de-zoomcamp-bucket"
#{BUCKET_NAME}
#
#gs://dwol-de-zoomcamp-bucket/dwol_yellow_tripdata_2024-01.parquet

# Define the source URI (GCS path), using wildcard to match multiple Parquet files
uri = f'gs://{BUCKET_NAME}/dwol_*.parquet'  # Wildcard to load multiple Parquet files

# # Define the external table configuration
# external_config = bigquery.ExternalConfig(
#     source_format=bigquery.SourceFormat.PARQUET,  # Use Parquet format
#     autodetect=True,  # Automatically detect schema from the files
#     uris=[uri],  # GCS URI for the files
# )

# # Define the table configuration (external table)
# table = bigquery.Table(f'{dataset_id}.{table_id}', external_config=external_config)

# # Create the external table in BigQuery
# table = client.create_table(table)  # This will create the external table

# print(f'Created external table {table_id} in dataset {dataset_id}')


# Define the external table configuration
external_config = bigquery.ExternalConfig(bigquery.SourceFormat.PARQUET)
external_config.autodetect = True
external_config.source_uris = [uri]  # List of URIs

# Define the table reference
table_ref = client.dataset(dataset_id).table(table_id)

# Define the table object and attach the external configuration
table = bigquery.Table(table_ref)
table.external_data_configuration = external_config  # Correct way to assign ExternalConfig

# Create the external table in BigQuery
table = client.create_table(table)  # This will create the external table

print(f'Created external table {table_id} in dataset {dataset_id}')