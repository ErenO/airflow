# Airflow Ansible Deployment

Ansible playbooks and roles for deploying and managing Airflow with Celery on remote servers.

## Directory Structure

```
ansible/
├── ansible.cfg              # Ansible configuration
├── inventory/
│   └── hosts.yml            # Server inventory
├── tasks/
│   └── main.yml             # Main deployment orchestration
├── playbooks/
│   ├── deploy.yml           # Full deployment (wrapper)
│   ├── update-dags.yml      # Update DAGs only
│   └── manage.yml           # Service management
└── roles/
    ├── docker/              # Install Docker
    │   └── tasks/main.yml
    └── airflow/             # Deploy Airflow
        ├── tasks/main.yml
        ├── handlers/main.yml
        └── templates/       # Docker/config templates
```

## Prerequisites

```bash
# Install Ansible
pip install ansible

# Install required collections
ansible-galaxy collection install community.docker ansible.posix
```

## Configuration

### Option 1: Edit Inventory File

```yaml
# inventory/hosts.yml
all:
  children:
    airflow_servers:
      hosts:
        production:
          ansible_host: 192.168.1.100
          ansible_user: ubuntu
          ansible_ssh_private_key_file: ~/.ssh/id_rsa
```

### Option 2: Environment Variables

```bash
export AIRFLOW_SERVER_IP="your-server-ip"
export AIRFLOW_SERVER_USER="ubuntu"
export AIRFLOW_SSH_KEY="~/.ssh/id_rsa"

# Optional: Credentials
export AIRFLOW_ADMIN_USER="admin"
export AIRFLOW_ADMIN_PASSWORD="secure-password"
export AIRFLOW_POSTGRES_PASSWORD="db-password"
export AIRFLOW_SECRET_KEY="your-secret-key"
```

## Usage

### Full Deployment

Deploy Docker and Airflow to a fresh server:

```bash
cd ansible

# Using tasks/main.yml (recommended)
ansible-playbook tasks/main.yml

# Or using playbook wrapper
ansible-playbook playbooks/deploy.yml

# With custom variables
ansible-playbook tasks/main.yml \
  -e "airflow_admin_password=mysecretpass" \
  -e "airflow_worker_replicas=3" \
  -e "airflow_navbar_color=#1a237e"
```

### Update DAGs Only

Sync DAGs without full redeployment:

```bash
ansible-playbook playbooks/update-dags.yml

# Custom source directory
ansible-playbook playbooks/update-dags.yml \
  -e "dags_source=/path/to/my/dags/"

# Delete removed DAGs from remote
ansible-playbook playbooks/update-dags.yml \
  -e "dags_delete_removed=true"
```

### Manage Services

```bash
# Status
ansible-playbook playbooks/manage.yml -e "action=status"

# Start/Stop/Restart
ansible-playbook playbooks/manage.yml -e "action=start"
ansible-playbook playbooks/manage.yml -e "action=stop"
ansible-playbook playbooks/manage.yml -e "action=restart"

# Logs
ansible-playbook playbooks/manage.yml -e "action=logs"
ansible-playbook playbooks/manage.yml -e "action=logs" -e "service=webserver"

# Scale workers
ansible-playbook playbooks/manage.yml -e "action=scale" -e "workers=5"

# Rebuild images
ansible-playbook playbooks/manage.yml -e "action=rebuild"

# List DAGs
ansible-playbook playbooks/manage.yml -e "action=dags"
```

## Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `airflow_home` | `/opt/airflow` | Installation directory |
| `airflow_user` | `airflow` | System user |
| `airflow_admin_user` | `airflow` | Web UI username |
| `airflow_admin_password` | `airflow` | Web UI password |
| `airflow_postgres_user` | `airflow` | Database username |
| `airflow_postgres_password` | `airflow` | Database password |
| `airflow_secret_key` | `change-me...` | Flask secret key |
| `airflow_navbar_color` | `#b71c1c` | Navbar color |
| `airflow_worker_replicas` | `1` | Number of workers |
| `airflow_worker_concurrency` | `4` | Tasks per worker |
| `dags_source` | `../../dags/` | Local DAGs path |

## Roles

### docker

Installs Docker CE and Docker Compose on Ubuntu/Debian.

**Tasks:**
- Adds Docker repository
- Installs Docker packages
- Enables Docker service
- Adds user to docker group
- Installs Python Docker library

### airflow

Deploys the complete Airflow stack with Docker Compose.

**Services deployed:**
- PostgreSQL (metadata database)
- Redis (Celery broker)
- Init (migrations, admin user)
- Webserver (Web UI)
- Scheduler (DAG orchestration)
- Worker (task execution, scalable)
- Flower (Celery monitoring)

## Troubleshooting

### Connection Issues

```bash
# Test SSH connection
ssh -i ~/.ssh/id_rsa ubuntu@your-server-ip

# Test Ansible connection
ansible airflow_servers -m ping
```

### Deployment Issues

```bash
# Run with verbose output
ansible-playbook tasks/main.yml -vvv

# Check specific role
ansible-playbook tasks/main.yml --tags docker
ansible-playbook tasks/main.yml --tags airflow
```

### Service Issues

```bash
# Check service status
ansible-playbook playbooks/manage.yml -e "action=status"

# View logs
ansible-playbook playbooks/manage.yml -e "action=logs" -e "service=init"
```
