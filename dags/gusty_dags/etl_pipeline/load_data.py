# ---
# operator: airflow.operators.python.PythonOperator
# dependencies:
#   - transform_data
# ---

import json


def load(**context):
    """Load the transformed data."""
    print("Loading data...")
    ti = context['ti']
    raw_data = ti.xcom_pull(task_ids='transform_data')
    data = json.loads(raw_data)

    for record in data['records']:
        print(f"Loading record: {record}")

    print(f"Successfully loaded {len(data['records'])} records")
    return "Load complete"


python_callable = load
