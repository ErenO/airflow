# Stage 1: Get Conda from miniconda image
FROM continuumio/miniconda3:latest AS conda-stage

# Stage 2: Base Airflow image with Conda
FROM apache/airflow:2.10.4-python3.11

USER root

# Copy Conda from miniconda image
COPY --from=conda-stage /opt/conda /opt/conda

# Add Conda to PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Initialize conda for all users
RUN conda init bash && \
    echo "conda activate base" >> /etc/bash.bashrc

USER airflow

# Initialize conda for airflow user
RUN conda init bash

# Install Python dependencies
RUN pip install --no-cache-dir \
    apache-airflow[celery]==2.10.4 \
    redis \
    gusty \
    flower
