# Airflow Flower image (Celery monitoring)
FROM airflow-base:latest

USER airflow

# Expose Flower port
EXPOSE 5555

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD curl -f http://localhost:5555/ || exit 1

CMD ["airflow", "celery", "flower", "--port", "5555"]
