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



def run_query(query):
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Execute the query
        cur.execute(query)

        # If it's a SELECT query, fetch the results
        if query.strip().lower().startswith("select"):
            rows = cur.fetchall()
            for row in rows:
                print(row)
        else:
            # Commit any changes for INSERT, UPDATE, DELETE queries
            conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.close()

# Example SQL queries to run

# Query to check if pickup and dropoff times cross dates
print("Question 3. Trip Segmentation Count")

###
# Up to 1 mile
###
sql_query = """
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance <= 1;
"""
run_query(sql_query)

###
# In between 1 (exclusive) and 3 miles (inclusive)
###
sql_query = """
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 1
AND trip_distance <= 3;
"""
run_query(sql_query)

###
# In between 3 (exclusive) and 7 miles (inclusive)
###
sql_query = """
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 3
AND trip_distance <= 7;
"""
run_query(sql_query)

###
# In between 7 (exclusive) and 10 miles (inclusive)
###
sql_query = """
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 7
AND trip_distance <= 10;
"""
run_query(sql_query)

###
# Over 10 miles
###
sql_query = """
SELECT COUNT(*) FROM green_tripdata
WHERE 1=1
AND lpep_pickup_datetime >= '2019-10-01 00:00:00'
AND lpep_dropoff_datetime < '2019-11-01 00:00:00'
AND trip_distance > 10; 
"""
run_query(sql_query)

print("Question 4. Longest trip for each day")
###
# 
###
sql_query = """
SELECT

  DATE(lpep_pickup_datetime) AS pickup_date,
  MAX(trip_distance) AS max_trip_distance
FROM
  green_tripdata
GROUP BY
  pickup_date
ORDER BY
  max_trip_distance DESC, pickup_date LIMIT 1;


-- SELECT
-- 	DATE (LPEP_PICKUP_DATETIME) AS PICKUP_DATE,
-- 	MAX(TRIP_DISTANCE) AS MAX_TRIP_DISTANCE
-- FROM
-- 	GREEN_TRIPDATA
-- GROUP BY
-- 	PICKUP_DATE
-- ORDER BY
-- 	MAX_TRIP_DISTANCE DESC,
-- 	PICKUP_DATE;

"""
run_query(sql_query)
print("\n")

print("Question 5. Longest trip for each day")
###
#
###
sql_query = """
SELECT
  tzl.zone
  ,DATE(lpep_pickup_datetime) AS pickup_date,
  pulocationid,
  SUM(total_amount) AS amount_total
FROM 
  green_tripdata gd
INNER JOIN taxi_zone_lookup tzl ON tzl.locationid = gd.pulocationid
WHERE 
  lpep_pickup_datetime >= '2019-10-18 00:00:00'
  AND lpep_pickup_datetime < '2019-10-19 00:00:00'
GROUP BY
  pickup_date,
  pulocationid,
  tzl.zone
HAVING
  SUM(total_amount) > 13000
ORDER BY
  amount_total DESC;
"""
run_query(sql_query)
print("\n")

print("Question 6.  Largest tip For the passengers picked up in October 2019 in the zone named 'East Harlem North' which was the drop off zone that had the largest tip?")
###
#
###
sql_query = """
SELECT
  tzl_do.zone as dropoff_zone
  ,MAX(tip_amount) as do_max_tip
FROM 
  green_tripdata gd
INNER JOIN taxi_zone_lookup tzl_pu ON tzl_pu.locationid = gd.pulocationid
INNER JOIN taxi_zone_lookup tzl_do ON tzl_do.locationid = gd.dolocationid

WHERE 
  lpep_pickup_datetime >= '2019-10-01 00:00:00'
  AND lpep_pickup_datetime < '2019-11-01 00:00:00'
  AND tzl_pu.locationid=74
GROUP BY
  tzl_do.zone
ORDER BY do_max_tip DESC
LIMIT 1;
"""
run_query(sql_query)
print("\n")
