# ---
# operator: airflow.operators.python.PythonOperator
# dependencies:
#   - extract_data
# ---

import json
from datetime import datetime


def transform(**context):
    """Transform the extracted data."""
    print("Transforming data...")
    ti = context['ti']
    raw_data = ti.xcom_pull(task_ids='extract_data')
    data = json.loads(raw_data)

    transformed_records = []
    for record in data['records']:
        transformed_records.append({
            "id": record['id'],
            "name": record['name'].upper(),
            "value": record['value'] * 2,
            "processed": True
        })

    result = {
        "records": transformed_records,
        "transformed_at": datetime.now().isoformat()
    }
    print(f"Transformed {len(transformed_records)} records")
    return json.dumps(result)


python_callable = transform
