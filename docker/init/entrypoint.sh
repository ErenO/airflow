#!/bin/bash
set -e

echo "=== Airflow Init ==="

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
    sleep 1
done
echo "Redis is ready!"

# Run database migrations
echo "Running database migrations..."
airflow db migrate

# Create admin user if it doesn't exist
echo "Creating admin user..."
airflow users create \
    --username "${AIRFLOW_ADMIN_USER:-airflow}" \
    --password "${AIRFLOW_ADMIN_PASSWORD:-airflow}" \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    2>/dev/null || echo "Admin user already exists"

echo "=== Init Complete ==="
