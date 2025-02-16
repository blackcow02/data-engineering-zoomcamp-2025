import subprocess
import sys

# Install dlt with DuckDB support
subprocess.check_call([sys.executable, "-m", "pip", "install", "dlt[duckdb]"])



import dlt
print("dlt version:", dlt.__version__)


import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides")   # <--- The name of the resource (will be used as the table name)


def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):    # <--- API endpoint for retrieving taxi ride data
        yield page   # <--- yield data to manage memory


pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data"
)

load_info = pipeline.run(ny_taxi(), write_disposition="replace")  # Call ny_taxi()
print("Pipeline completed successfully!")
print(load_info)


try:
    df = pipeline.dataset(dataset_type="default").rides.df()
    print(df.head())  # Show the first few rows of the DataFrame

# Count the total number of rows
    total_rows = len(df)  # or df.shape[0]
    print(f"Total rows in the 'rides' dataset: {total_rows}")

    
except Exception as e:
    print("Error retrieving dataset:", e)




import duckdb
import pandas as pd

conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")

df = conn.sql("DESCRIBE").df()

# Display the DataFrame
print(df)
total_rows = len(df)  # or df.shape[0]
print(f"Total tables in DuckDB: {total_rows}")


df = pipeline.dataset(dataset_type="default").rides.df()
print(df.info())




with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM rides;
            """
        )
    print(res)


