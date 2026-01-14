# Airflow Scheduler image
FROM airflow-base:latest

USER airflow

# Copy DAGs
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root plugins/ /opt/airflow/plugins/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD airflow jobs check --job-type SchedulerJob --hostname "$(hostname)" || exit 1

CMD ["airflow", "scheduler"]
