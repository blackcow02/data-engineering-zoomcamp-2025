#!/bin/bash

#RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz -O /app/data-share/green_tripdata_2019-10.csv.gz && gunzip /app/data-share/green_tripdata_2019-10.csv.gz


# Check if at least one year, color type, and a valid data set color are provided as arguments
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <color_type> <year(s)>"
  echo "Example: $0 yellow 2019 2020"
  exit 1
fi

# Set the color type (yellow_ or green_)
COLOR_TYPE=$1

# Validate color type
# if [[ "$COLOR_TYPE" != "yellow_" && "$COLOR_TYPE" != "green_" ]]; then
#   echo "Error: Invalid color type. Please specify 'yellow_' or 'green_'."
#   exit 1
# fi

# Remove the first argument (color type), leaving only the year(s)
shift

# Define the base URL for the GitHub releases
BASE_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/${COLOR_TYPE}"

# Loop through all provided years
for YEAR in "$@"; do
  # Loop through all 12 months
  for MONTH in {01..12}; do
    # Construct the filename based on the color type and year/month
    FILE="${COLOR_TYPE}_tripdata_${YEAR}-${MONTH}.csv.gz"
    
    # Construct the full download URL
    URL="${BASE_URL}/${FILE}"

    # Use wget to check if the file exists
    echo "Checking if ${FILE} exists..."
    if wget --spider "$URL" 2>/dev/null; then
      # If the file exists, download it
      echo "Downloading ${FILE}..."
      wget "$URL" -O ../data-share/"$FILE"

      # Check if the download was successful
      if [ $? -eq 0 ]; then
        # Use gunzip to extract the file
        echo "Extracting ${FILE}..."
        gunzip ../data-share/"$FILE"
      else
        echo "Failed to download ${FILE}."
      fi
    else
      echo "File ${FILE} does not exist, skipping..."
    fi
  done
done

echo "All downloads and extractions are complete."
