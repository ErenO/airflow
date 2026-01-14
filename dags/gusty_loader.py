"""Gusty DAG loader - automatically creates DAGs from YAML definitions."""
from pathlib import Path
from gusty import create_dag

# Path to gusty DAGs directory
GUSTY_DAGS_DIR = Path(__file__).parent / "gusty_dags"


def _load_gusty_dags():
    """Load all gusty DAGs and return them as a dict."""
    dags = {}
    for dag_folder in GUSTY_DAGS_DIR.iterdir():
        if dag_folder.is_dir() and not dag_folder.name.startswith(("_", ".")):
            dag = create_dag(str(dag_folder))
            dags[dag.dag_id] = dag
    return dags


# Load DAGs and expose them at module level
_gusty_dags = _load_gusty_dags()
for _dag_id, _dag in _gusty_dags.items():
    globals()[_dag_id] = _dag

# Explicit reference for Airflow to find
etl_pipeline = _gusty_dags.get("etl_pipeline")
