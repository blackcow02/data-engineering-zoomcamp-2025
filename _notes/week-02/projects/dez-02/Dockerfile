FROM python:3.12.8-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    unzip \
    nano \
    && rm -rf /var/lib/apt/lists/*
#    libpq-dev \

   
# Upgrade pip
#RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade pip \
    && pip install pandas \
    && pip install psycopg2-binary \
    && pip install python-dotenv

RUN pip install dbt
# Optionally, install additional dbt adapters (e.g., for PostgreSQL, Snowflake, etc.)
RUN pip install dbt-postgres  # For PostgreSQL
# RUN pip install dbt-snowflake  # For Snowflake

    
# Google Cloud SDK
RUN apt-get update && apt-get install -y curl gnupg && \
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
apt-get update && apt-get install -y google-cloud-cli


# Install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip \
    && unzip terraform_1.5.0_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_1.5.0_linux_amd64.zip
    
# Copy requirements file (if you have one)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /pip-scripts
COPY ./pip-scripts /app/pip-scripts
#RUN chmod +x /app/pip-scripts/*.sh

RUN mkdir /app/data-share
RUN chmod 777 /app/data-share



#RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz -O /app/data-share/green_tripdata_2019-10.csv.gz
#RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz -O /app/data-share/green_tripdata_2019-10.csv.gz && gunzip /app/data-share/green_tripdata_2019-10.csv.gz

#&& tar -xvzf green_tripdata_2019-10.csv.gz
##RUN tar -xvzf file.tar.gz -C /app/data-share/green_tripdata_2019-10.csv.gz /app/data-share/green_tripdata_2019-10.csv
#RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O /app/data-share/taxi_zone_lookup.csv

RUN mkdir /sql
COPY ./sql /app/sql
RUN chmod +x /app/sql/*.sql

RUN mkdir /terraform
COPY ./terraform /app/terraform
RUN chmod 777 /app/terraform

RUN mkdir /flows
COPY ./flows /app/flows
RUN chmod -R a+w /app/flows
#RUN chmod 777 /app/flows
#RUN chmod +x /app/flows/*.yaml


RUN mkdir /scripts
COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/*.sh


#Create a non-root user and switch to it
RUN useradd -m -s /bin/bash vscode
USER vscode
#USER vscode

# Set the default command
CMD ["bash"]
#CMD ["python", "/app/scripts/data_loader.py"]

