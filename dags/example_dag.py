from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def print_hello():
    print("Hello from Airflow with Celery!")
    return "Hello task completed"


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'example_celery_dag',
    default_args=default_args,
    description='A simple example DAG for Celery executor',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    task_hello = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello,
    )

    task_bash = BashOperator(
        task_id='bash_task',
        bash_command='echo "Running on Celery worker: $(hostname)"',
    )

    task_hello >> task_bash
