# Airflow Init image - runs migrations and creates admin user
FROM airflow-base:latest

USER airflow

COPY --chown=airflow:root docker/init/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
