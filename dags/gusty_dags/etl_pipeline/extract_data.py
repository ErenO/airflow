# ---
# operator: airflow.operators.python.PythonOperator
# ---

import json
from datetime import datetime


def extract(**context):
    """Extract data from source."""
    print("Extracting data...")
    data = {
        "records": [
            {"id": 1, "name": "Alice", "value": 100},
            {"id": 2, "name": "Bob", "value": 200},
            {"id": 3, "name": "Charlie", "value": 300},
        ],
        "extracted_at": datetime.now().isoformat()
    }
    print(f"Extracted {len(data['records'])} records")
    return json.dumps(data)


python_callable = extract
