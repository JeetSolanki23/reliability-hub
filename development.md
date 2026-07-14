Reliability Hub - Development Guide
Project Overview
Reliability Hub is an internal platform for monitoring service health, tracking incidents, and reporting SLO status across environments.

Target: SRE-style operational engineering demonstrating monitoring, alerting, incident workflows, and automated deployments with strong DevOps/SRE signal.

Quick Start
Prerequisites
Python 3.11+
PostgreSQL 14+
Git
Setup
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost/reliabilityhub
EOF

# 4. Create database (PostgreSQL running locally)
psql -U postgres -c "CREATE DATABASE reliabilityhub;"

# 5. Run migrations (when Alembic is configured)
alembic upgrade head

# 6. Start development server
uvicorn app.main:app --reload --port 8003
Visit http://localhost:8003/docs for interactive API documentation.

Project Structure
reliability-hub/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── services.py       # Service registry CRUD
│   │   ├── health.py         # Health check execution and history
│   │   ├── incidents.py      # Incident lifecycle management
│   │   └── slo.py            # SLO definition and status
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py       # SQLAlchemy engine and session
│   │   ├── models.py         # ORM models (Service, HealthCheck, Incident, SLO)
│   │   └── schemas.py        # Pydantic request/response schemas
│   ├── workers/
│   │   ├── __init__.py
│   │   └── health_probe.py   # Background health check executor
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── webhooks.py       # Alert webhook notifiers
│   └── main.py               # FastAPI app with router includes
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   └── test_health.py        # Health check test
├── docker/
│   └── Dockerfile
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── worker-deployment.yaml  # Background worker pod
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── prod/
├── terraform/
│   └── environments/
│       └── dev/
│           └── main.tf
├── monitoring/
│   ├── prometheus.yml
│   ├── alertmanager.yml
│   └── grafana/
│       └── dashboards/
│           ├── service-health.json
│           ├── incidents.json
│           └── slo-compliance.json
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml (with environment promotion)
├── .flake8
├── pyproject.toml
├── .gitignore
├── requirements.txt
├── README.md
├── alembic.ini
└── DEVELOPMENT.md (this file)
API Endpoints (Implementation Checklist)
Service Registry
POST /services - Register new service to monitor
GET /services - List all services (paginated)
GET /services/{id} - Get service details
PATCH /services/{id} - Update service configuration
DELETE /services/{id} - Remove service from monitoring
Health Checks & Probes
GET /services/{id}/checks - List recent health checks
POST /services/{id}/checks/run - Trigger immediate health check
GET /services/{id}/history - Historical health data (time range query)
Incidents
POST /incidents - Create incident manually
GET /incidents - List incidents (filterable by status, severity)
PATCH /incidents/{id} - Update incident (title, severity, notes)
POST /incidents/{id}/resolve - Mark incident as resolved
SLO (Service Level Objectives)
POST /slos - Create SLO for service
GET /slos - List SLOs
GET /slo/status - Current SLO compliance status for all services
Health & Observability
GET /healthz - Liveness probe
GET /readyz - Readiness probe
GET /metrics - Prometheus metrics endpoint
Database Models
Services
- id (UUID, primary key)
- name (string, unique)
- owner (string)
- endpoint_url (string)
- environment (string: "dev", "staging", "prod")
- check_interval_seconds (integer, default 60)
HealthChecks
- id (UUID, primary key)
- service_id (UUID, foreign key → services)
- checked_at (datetime)
- status (string: "up", "down", "degraded")
- latency_ms (integer)
- response_code (integer, nullable)
Incidents
- id (UUID, primary key)
- service_id (UUID, foreign key → services)
- title (string)
- severity (string: "sev1", "sev2", "sev3", "sev4")
- status (string: "open", "investigating", "mitigated", "resolved")
- started_at (datetime)
- resolved_at (datetime, nullable)
SLOs
- id (UUID, primary key)
- service_id (UUID, foreign key → services)
- target_availability (float, e.g., 0.99 for 99%)
- window_days (integer, e.g., 30 for monthly)
Implementation Steps
Step 1: Database & Core Models (Week 1)
Configure PostgreSQL in app/core/database.py
Complete Alembic setup: alembic init alembic
Create first migration: alembic revision --autogenerate -m "Initial schema"
Apply migration: alembic upgrade head
Step 2: Service Registry API (Week 1-2)
Implement POST /services endpoint
Implement GET /services (with pagination)
Implement GET /services/{id}
Implement PATCH /services/{id}
Implement DELETE /services/{id}
Add URL validation for endpoint_url
Step 3: Health Check Executor (Week 2)
Implement HTTP probe function (HEAD/GET to endpoint_url)
Record response latency and status code
Implement POST /services/{id}/checks/run endpoint
Implement GET /services/{id}/checks endpoint
Implement GET /services/{id}/history with date range filtering
Step 4: Background Scheduler (Week 2-3)
Set up APScheduler or Celery for background probes
Implement periodic health check execution based on check_interval_seconds
Create separate worker deployment for scheduled tasks
Add error handling and retry logic
Step 5: Incident Management (Week 3)
Implement POST /incidents endpoint
Implement GET /incidents with filtering
Implement PATCH /incidents/{id}
Implement POST /incidents/{id}/resolve
Implement auto-incident creation on health check failures
Step 6: SLO Calculation & Status (Week 3-4)
Implement SLO CRUD endpoints
Implement SLI calculation (availability = successful_checks / total_checks)
Implement SLI latency percentile calculation (p95, p99)
Implement GET /slo/status with burn rate
Add SLO breach detection and alerting
Step 7: Alerting & Webhooks (Week 4)
Implement webhook notification system
Send alerts on SLO breaches
Send alerts on incident creation/resolution
Support Slack, Teams, email webhooks
Step 8: Tests (Week 4-5)
Unit tests for health check logic
Integration tests for all endpoints
Tests for SLO calculation
Tests for incident workflow
Aim for 70%+ coverage
Step 9: Monitoring & Dashboards (Week 5)
Update Prometheus config for self-monitoring
Create Grafana dashboards:
Service health matrix
Incident timeline
SLO compliance across all services
Create alert rules for system health
Step 10: DevOps & Deployment (Week 5-6)
Test Docker build
Verify CI passes
Push to GitHub
Create separate worker deployment in Kubernetes
Configure Terraform for AKS
Deploy monitoring stack (Prometheus, Grafana, Alertmanager)
Development Commands
Linting & Code Quality
ruff check .
flake8 app tests
ruff check --fix .
Security Scanning
bandit -r app/
pip-audit --desc
Testing
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_services.py -v

# Run unit tests only
pytest -m unit
Database
# Migrations
alembic upgrade head
alembic revision --autogenerate -m "Add service tags"
alembic downgrade -1

# Connect to database
psql -U postgres -d reliabilityhub
Running Background Worker
# Start health probe scheduler
python -m app.workers.health_probe

# With Celery (if implemented)
celery -A app.workers worker --loglevel=info
Docker
# Build image
docker build -f docker/Dockerfile -t reliability-hub:dev .

# Run API service
docker run -p 8003:8000 reliability-hub:dev

# Run worker service
docker run --env-file .env reliability-hub:dev python -m app.workers.health_probe
Testing Strategy
Unit Tests
# tests/test_probes.py
def test_http_probe_success():
    result = probe_health_check("https://example.com", timeout=5)
    assert result["status"] in ["up", "degraded"]
    assert result["latency_ms"] > 0

def test_slo_calculation():
    slo = calculate_availability(up_checks=990, total_checks=1000)
    assert slo == 0.99
Integration Tests
# tests/test_api.py
def test_create_service(test_app, db):
    response = test_app.post("/services", json={
        "name": "api-gateway",
        "owner": "platform-team",
        "endpoint_url": "https://api.example.com/health",
        "environment": "prod",
        "check_interval_seconds": 60
    })
    assert response.status_code == 200
    assert response.json()["name"] == "api-gateway"

def test_incident_lifecycle(test_app, db):
    # Create incident
    create_resp = test_app.post("/incidents", json={
        "service_id": "service-123",
        "title": "API latency spike",
        "severity": "sev2"
    })
    incident_id = create_resp.json()["id"]

    # Update incident
    update_resp = test_app.patch(f"/incidents/{incident_id}", json={
        "status": "investigating"
    })
    assert update_resp.json()["status"] == "investigating"

    # Resolve incident
    resolve_resp = test_app.post(f"/incidents/{incident_id}/resolve")
    assert resolve_resp.json()["status"] == "resolved"
Coverage Goal: 70%+ overall, 100% for critical SLO calculations.

SLO/SLI Model
Availability SLI
Availability = Successful Checks / Total Checks
Latency SLI
Latency SLI = Checks where latency < threshold / Total Checks
Error Budget
Error Budget = (1 - Target Availability) * Window Duration
Burn Rate
Current Burn Rate = (1 - Current Availability) / (1 - Target Availability)
Example Alert
Alert: SLO will be breached in 1 day if burn rate > 10x
Kubernetes Deployment
Key considerations for multi-environment setup:

# Kustomize overlays for environment-specific configs
k8s/
├── base/
│   ├── deployment.yaml       # API service
│   ├── worker-deployment.yaml # Background probes
│   └── service.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml (3 replicas, less strict probes)
    ├── staging/
    │   └── kustomization.yaml (5 replicas)
    └── prod/
        └── kustomization.yaml (10 replicas, strict probes)
Monitoring & Alerting
Prometheus Metrics
reliability_hub_http_requests_total - Request count
reliability_hub_http_request_duration_seconds - Request latency
reliability_hub_health_checks_total - Health check count
reliability_hub_slo_compliance - SLO compliance percentage
Alert Rules (AlertManager)
- alert: SLOBreach
  expr: reliability_hub_slo_compliance < 99
  for: 5m
  annotations:
    summary: "{{ $labels.service }} SLO breached"

- alert: HighBurnRate
  expr: burn_rate > 10
  for: 1m
  annotations:
    summary: "High burn rate detected for {{ $labels.service }}"
Common Issues & Solutions
Health Probe Timeouts
Increase probe timeout in service config
Check network connectivity to target endpoints
Verify target endpoint is responding
Incident Auto-Creation Not Triggering
Check background worker is running
Verify service check_interval_seconds is set
Check database for health check records
SLO Calculations Incorrect
Verify time window is calculated correctly
Check that all health checks are recorded
Ensure check timestamps are in UTC
PostgreSQL Issues
psql -U postgres -c "SELECT 1"
docker run --name postgres-rh -e POSTGRES_PASSWORD=password -e POSTGRES_DB=reliabilityhub -p 5432:5432 -d postgres:14
CI/CD Pipeline
GitHub Actions in .github/workflows/:

CI (ci.yml): Lint, security, test, Docker build, container scan
CD (cd.yml): Environment promotion (dev → staging → prod)
Promote through environments with manual approval gates.

Production Checklist
All endpoint tests passing
70%+ code coverage
Background worker running and probing services
Database backups configured
Monitoring dashboards verified
Alert rules tested
Webhook integrations working (Slack, Teams, etc.)
SLO targets defined for all services
Incident runbooks documented
On-call alerting configured
Useful Links
FastAPI: https://fastapi.tiangolo.com/
SQLAlchemy: https://www.sqlalchemy.org/
APScheduler: https://apscheduler.readthedocs.io/
Prometheus: https://prometheus.io/docs/
Grafana: https://grafana.com/docs/grafana/
Alertmanager: https://prometheus.io/docs/alerting/latest/overview/
Kubernetes: https://kubernetes.io/docs/
Key SRE Concepts to Demonstrate
SLO Definition: Clear, measurable targets
SLI Tracking: Continuous measurement
Error Budget: Quantified risk tolerance
Incident Response: Structured workflow
Alerting: Intelligent thresholds and escalation
Observability: Metrics, logs, traces
