# Airflow Webserver image
FROM airflow-base:latest

USER airflow

# Copy DAGs
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root plugins/ /opt/airflow/plugins/

# Expose webserver port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["airflow", "webserver", "--port", "8080"]
