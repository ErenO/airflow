# Airflow Celery Worker image
FROM airflow-base:latest

USER airflow

# Copy DAGs
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root plugins/ /opt/airflow/plugins/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d celery@$(hostname) || exit 1

CMD ["airflow", "celery", "worker"]
