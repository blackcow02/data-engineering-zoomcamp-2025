#!/bin/bash

# Set environment variables for PostgreSQL
# export POSTGRES_HOST=localhost
# export POSTGRES_PORT=5432
# export POSTGRES_USER=postgres
# export POSTGRES_PASSWORD=postgres
# export POSTGRES_DB=your_db_name

# Wait for PostgreSQL to start up
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Create the database (if it doesn't exist)
psql -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;" || echo "Database already exists"

# Import data from CSV into your table (adjust the table name and CSV path)
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\COPY your_table_name FROM '/path/to/your/data.csv' WITH CSV HEADER;"

echo "Database setup complete."