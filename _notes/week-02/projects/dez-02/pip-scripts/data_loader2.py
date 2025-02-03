import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2 import sql

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
db_params = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}

# Path to your CSV file
csv_file = "../data-share/green_tripdata_2019-10.csv"

# Read the CSV file using Pandas
df = pd.read_csv(csv_file, low_memory=False)  # Option 1: Avoid warning by setting low_memory=False

# Convert datetime columns to pandas datetime type
# This is important to ensure that they are properly handled as TIMESTAMP when inserting into PostgreSQL
# datetime_columns = df.select_dtypes(include=['object']).columns
# for col in datetime_columns:
#     try:
#         df[col] = pd.to_datetime(df[col], errors='coerce')  # Convert columns to datetime, coerce errors if any
#     except Exception as e:
#         print(f"Error converting column {col}: {e}")

# This is important to ensure that they are properly handled as TIMESTAMP when inserting into PostgreSQL
datetime_columns = df.select_dtypes(include=['object']).columns
for col in datetime_columns:
    try:
        # Specify the datetime format explicitly to avoid warnings
        df[col] = pd.to_datetime(df[col], format='%m/%d/%Y %H:%M', errors='coerce')  # Adjust the format accordingly
    except Exception as e:
        print(f"Error converting column {col}: {e}")
        
# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Dynamically create the table based on the DataFrame's columns and types
table_name = "green_tripdata"
columns = []
for col, dtype in zip(df.columns, df.dtypes):
    # Map pandas data types to PostgreSQL data types
    if dtype == 'int64':
        pg_dtype = 'BIGINT'
    elif dtype == 'float64':
        pg_dtype = 'FLOAT'
    elif dtype == 'object':
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
    columns=sql.SQL(', ').join(map(sql.Identifier, df.columns))
)

# Execute the COPY command
with open(csv_file, 'r') as f:
    cur.copy_expert(copy_query, f)  # Here we pass the file object directly

# Commit and close the connection
conn.commit()
cur.close()
conn.close()

print(f"Data loaded into {table_name} successfully.")


# #FK

# import os
# from dotenv import load_dotenv
# import pandas as pd
# import psycopg2
# from psycopg2 import sql

# # Database connection parameters
# # db_params = {
# #     "dbname": "your_db",
# #     "user": "your_user",
# #     "password": "your_password",
# #     "host": "localhost",
# #     "port": "5432"
# # }

# db_params = {
#     "dbname": os.getenv("POSTGRES_DB"),
#     "user": os.getenv("POSTGRES_USER"),
#     "password": os.getenv("POSTGRES_PASSWORD"),
#     "host": os.getenv("POSTGRES_HOST"),
#     "port": os.getenv("POSTGRES_PORT")
# }


# # Path to your CSV file
# csv_file = "../data-share/green_tripdata_2019-10.csv"

# # Read the CSV file using Pandas
# #df = pd.read_csv(csv_file)
# df = pd.read_csv(csv_file, low_memory=False)  # Option 1: Avoid warning by setting low_memory=False


# # Connect to PostgreSQL
# conn = psycopg2.connect(**db_params)
# cur = conn.cursor()

# # Dynamically create the table based on the DataFrame's columns and types
# table_name = "green_tripdata"
# columns = []
# for col, dtype in zip(df.columns, df.dtypes):
#     # Map pandas data types to PostgreSQL data types
#     if dtype == 'int64':
#         pg_dtype = 'BIGINT'
#     elif dtype == 'float64':
#         pg_dtype = 'FLOAT'
#     elif dtype == 'object':
#         pg_dtype = 'TEXT'
#     elif dtype == 'datetime64[ns]':
#         pg_dtype = 'TIMESTAMP'
#     else:
#         pg_dtype = 'TEXT'  # Fallback for unsupported types

#     columns.append(f"{col} {pg_dtype}")

# # Create the SQL statement to create the table
# create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
# cur.execute(create_table_query)

# # Commit the changes
# conn.commit()

# # # Now use the COPY command to load data into PostgreSQL
# # copy_query = sql.SQL("""
# #     COPY {table} ({columns})
# #     FROM %s
# #     WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"');
# # """).format(
# #     table=sql.Identifier(table_name),
# #     columns=sql.SQL(', ').join(map(sql.Identifier, df.columns))
# # )

# # # Execute the COPY command
# # with open(csv_file, 'r') as f:
# #     cur.copy_expert(copy_query, f)

# copy_query = sql.SQL("""
#     COPY {table} ({columns})
#     FROM csv_file
#     WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"');
# """).format(
#     table=sql.Identifier(table_name),
#     columns=sql.SQL(', ').join(map(sql.Identifier, df.columns))
# )

# # Execute the COPY command
# with open(csv_file, 'r') as f:
#     cur.copy_expert(copy_query, f)  # Here we pass the file object directly
    

# # with open(csv_file, 'r') as f:
# #     next(f) #Skip header
# #     cur.copy_from(f, table_name, sep=',', null='', columns=df.columns)


# # Commit and close the connection
# conn.commit()
# cur.close()
# conn.close()

# print(f"Data loaded into {table_name} successfully.")
