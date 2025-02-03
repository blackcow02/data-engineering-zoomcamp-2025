import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file (if using)
load_dotenv()

# Database connection parameters
db_params = {
    "dbname": os.getenv("POSTGRES_DB", "your_dbname"),  # Update or set a default if needed
    "user": os.getenv("POSTGRES_USER", "your_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "your_password"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

# Path to your CSV file
csv_file = "../data-share/taxi_zone_lookup.csv"

# Read the CSV file using Pandas
df = pd.read_csv(csv_file, low_memory=False)

# Clean column names: Remove leading/trailing spaces and convert to lowercase (optional)
df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
# Optionally, convert to lowercase (you can adjust if needed)
df.columns = df.columns.str.lower()  

# Convert datetime columns to pandas datetime type for correct PostgreSQL mapping
# datetime_columns = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']  # Adjust column names as needed
# for col in datetime_columns:
#     df[col] = pd.to_datetime(df[col], format='%m/%d/%Y %H:%M', errors='coerce')  # Adjust format if needed

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Dynamically create the table based on the DataFrame's columns and types
table_name = "taxi_zone_lookup"
columns = []
for col, dtype in zip(df.columns, df.dtypes):
    # Map pandas data types to PostgreSQL data types
    if dtype == 'int64':
        pg_dtype = 'BIGINT'
    elif dtype == 'float64':
        pg_dtype = 'FLOAT'
    elif dtype == 'object':  # Text columns in pandas are treated as object dtype
        pg_dtype = 'TEXT'
    elif dtype == 'datetime64[ns]':
        pg_dtype = 'TIMESTAMP'
    else:
        pg_dtype = 'TEXT'  # Fallback for unsupported types

    columns.append(f"{col} {pg_dtype}")

# Create the SQL statement to create the table
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
cur.execute(create_table_query)

# Commit the changes
conn.commit()

# Prepare the COPY command
copy_query = sql.SQL("""
    COPY {table} ({columns})
    FROM stdin WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"');
""").format(
    table=sql.Identifier(table_name),
    columns=sql.SQL(', ').join(map(sql.Identifier, df.columns))  # Ensure proper quoting of column names
)

# Execute the COPY command
with open(csv_file, 'r') as f:
    cur.copy_expert(copy_query, f)  # Pass the file object directly to copy_expert

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

print(f"Data loaded into {table_name} successfully.")
