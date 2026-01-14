# Base Airflow image with common dependencies
FROM apache/airflow:2.10.4-python3.11

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies
RUN pip install --no-cache-dir \
    apache-airflow[celery]==2.10.4 \
    redis \
    gusty \
    flower
