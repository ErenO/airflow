# Airflow with Celery Executor

Production-ready Apache Airflow deployment with Docker and Ansible.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                            │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│  PostgreSQL │    Redis    │  Webserver  │  Scheduler  │ Flower  │
│   (metadata)│   (broker)  │   (UI)      │  (orchestr) │ (monitor)│
│   :5432     │   :6379     │   :8080     │             │  :5555  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
               ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
               │ Worker 1│   │ Worker 2│   │ Worker N│
               │ (Celery)│   │ (Celery)│   │ (Celery)│
               └─────────┘   └─────────┘   └─────────┘
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Metadata database |
| Redis | 6379 | Celery message broker |
| Webserver | 8080 | Airflow Web UI |
| Scheduler | - | DAG orchestration |
| Worker | - | Task execution (scalable) |
| Flower | 5555 | Celery monitoring |

## Quick Start (Local)

### 1. Build and Start

```bash
# Build base image first
docker build -t airflow-base:latest -f docker/base/Dockerfile .

# Start all services
docker compose up -d --build

# Wait for init to complete
docker compose logs -f init
```

### 2. Access UIs

- **Airflow Web UI**: http://localhost:8080
- **Flower (Celery)**: http://localhost:5555
- **Login**: airflow / airflow

### 3. Common Operations

```bash
# View service status
docker compose ps

# View logs
docker compose logs -f webserver
docker compose logs -f scheduler
docker compose logs -f worker

# Scale workers
docker compose up -d --scale worker=3

# Restart services
docker compose restart

# Stop all services
docker compose down

# Stop and remove volumes (clean start)
docker compose down -v
```

## Directory Structure

```
airflow/
├── dags/                      # DAG definitions
│   ├── example_dag.py
│   ├── gusty_loader.py        # Gusty DAG loader
│   └── gusty_dags/            # YAML-based DAGs
│       └── etl_pipeline/
├── plugins/                   # Airflow plugins
├── docker/                    # Docker images
│   ├── base/                  # Base image with dependencies
│   ├── redis/                 # Redis broker
│   ├── webserver/             # Airflow webserver
│   ├── scheduler/             # Airflow scheduler
│   ├── worker/                # Celery worker
│   ├── flower/                # Celery monitoring
│   └── init/                  # DB migrations & user setup
├── ansible/                   # Ansible deployment
│   ├── tasks/                 # Main deployment tasks
│   ├── playbooks/             # Playbook wrappers
│   ├── roles/                 # Reusable roles
│   └── inventory/             # Server inventory
├── docker-compose.yml         # Container orchestration
└── README.md
```

## Ansible Deployment

### Prerequisites

```bash
# Install Ansible
pip install ansible

# Install required collections
ansible-galaxy collection install community.docker ansible.posix
```

### Configure Inventory

Edit `ansible/inventory/hosts.yml`:

```yaml
all:
  children:
    airflow_servers:
      hosts:
        production:
          ansible_host: your-server-ip
          ansible_user: ubuntu
          ansible_ssh_private_key_file: ~/.ssh/id_rsa
```

Or use environment variables:

```bash
export AIRFLOW_SERVER_IP="your-server-ip"
export AIRFLOW_SERVER_USER="ubuntu"
export AIRFLOW_SSH_KEY="~/.ssh/id_rsa"
```

### Deploy Airflow

```bash
cd ansible

# Full deployment (Docker + Airflow)
ansible-playbook tasks/main.yml

# Or use the playbook wrapper
ansible-playbook playbooks/deploy.yml

# With custom settings
ansible-playbook tasks/main.yml \
  -e "airflow_admin_password=secure-password" \
  -e "airflow_worker_replicas=3"
```

### Update DAGs

```bash
# Sync DAGs to remote server
ansible-playbook playbooks/update-dags.yml

# From custom source
ansible-playbook playbooks/update-dags.yml \
  -e "dags_source=/path/to/dags/"

# Delete removed DAGs
ansible-playbook playbooks/update-dags.yml \
  -e "dags_delete_removed=true"
```

### Manage Services

```bash
# Check status
ansible-playbook playbooks/manage.yml -e "action=status"

# Start/Stop/Restart
ansible-playbook playbooks/manage.yml -e "action=start"
ansible-playbook playbooks/manage.yml -e "action=stop"
ansible-playbook playbooks/manage.yml -e "action=restart"

# View logs
ansible-playbook playbooks/manage.yml -e "action=logs"
ansible-playbook playbooks/manage.yml -e "action=logs" -e "service=webserver"

# Scale workers
ansible-playbook playbooks/manage.yml -e "action=scale" -e "workers=5"

# Rebuild images
ansible-playbook playbooks/manage.yml -e "action=rebuild"

# List DAGs
ansible-playbook playbooks/manage.yml -e "action=dags"
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AIRFLOW_ADMIN_USER` | airflow | Web UI admin username |
| `AIRFLOW_ADMIN_PASSWORD` | airflow | Web UI admin password |
| `AIRFLOW_POSTGRES_PASSWORD` | airflow | PostgreSQL password |
| `AIRFLOW_SECRET_KEY` | (generated) | Flask secret key |

### Ansible Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `airflow_home` | /opt/airflow | Installation directory |
| `airflow_worker_replicas` | 1 | Number of workers |
| `airflow_worker_concurrency` | 4 | Tasks per worker |
| `airflow_navbar_color` | #b71c1c | Navbar color |

## Adding DAGs

### Python DAG

```python
# dags/my_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    'my_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    def my_task():
        print("Hello from Airflow!")

    PythonOperator(
        task_id='my_task',
        python_callable=my_task,
    )
```

### Gusty DAG (YAML)

```yaml
# dags/gusty_dags/my_pipeline/METADATA.yml
description: "My Pipeline"
schedule_interval: "@daily"
start_date: !days_ago 1
catchup: false
tags: [gusty]
```

```python
# dags/gusty_dags/my_pipeline/task_1.py
# operator: airflow.operators.python.PythonOperator
def task_1():
    print("Task 1 executed!")
```

## Troubleshooting

### Services not starting

```bash
# Check init logs
docker compose logs init

# Check specific service
docker compose logs webserver

# Verify database connection
docker compose exec webserver airflow db check
```

### Workers not picking up tasks

```bash
# Check worker logs
docker compose logs worker

# Check Celery broker connection
docker compose exec worker celery --app airflow.providers.celery.executors.celery_executor.app inspect ping

# View Flower dashboard
open http://localhost:5555
```

### DAGs not appearing

```bash
# Check for import errors
docker compose exec webserver airflow dags list-import-errors

# Trigger DAG parsing
docker compose restart scheduler
```

## Production Considerations

1. **Change default passwords** - Use environment variables or Ansible Vault
2. **Configure HTTPS** - Add nginx/traefik reverse proxy
3. **External database** - Use managed PostgreSQL (RDS, Cloud SQL)
4. **External Redis** - Use managed Redis (ElastiCache, Memorystore)
5. **Persistent storage** - Configure NFS/EFS for DAGs and logs
6. **Monitoring** - Add Prometheus/Grafana for metrics
7. **Backup** - Regular PostgreSQL backups

## License

MIT
