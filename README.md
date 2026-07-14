# Reliability Hub

Reliability Hub is a production-ready DevOps showcase project. It is an internal platform for monitoring service health, tracking incidents, and reporting SLO (Service Level Objective) status across environments.

## Features

- **Service Registry**: Register and manage services to monitor.
- **Health Checks**: Automated background health probes with latency tracking.
- **Incident Management**: Lifecycle management for service incidents (Open, Investigating, Mitigated, Resolved).
- **SLO Monitoring**: Define and track availability and latency SLOs.
- **Observability**: Prometheus metrics and Grafana dashboards.
- **Cloud Agnostic**: Deployable on any Kubernetes cluster (EKS, AKS, GKE, or local Kind/Minikube).
- **CI/CD**: Fully automated pipeline using GitHub Actions.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic migrations
- **Background Tasks**: APScheduler
- **Containerization**: Docker (Multi-stage builds)
- **Orchestration**: Kubernetes (Helm charts)
- **Monitoring**: Prometheus & Grafana
- **Infrastructure**: Terraform (Modular)
- **CI/CD**: GitHub Actions

## Project Structure

```text
reliability-hub/
├── app/                  # FastAPI Backend & Worker logic
├── tests/                # Unit and Integration tests
├── docker/               # Dockerfile & Docker Compose setups
├── k8s/                  # Helm Charts & Kubernetes Deployment Guide
├── terraform/            # Infrastructure as Code (Azure/Cloud)
├── monitoring/           # Prometheus & Grafana Dashboards
└── .github/workflows/    # GitHub Actions CI/CD Pipeline
```

---

## 🚀 Master Deployment Guide

This project supports three deployment modes depending on your needs.

### 1. Pure Local Development (Python)
Best for rapid code changes.
- Instructions: See [development.md](development.md)

### 2. Containerized Development (Docker Compose)
Best for testing the App + Database interaction without Kubernetes.
1. `docker compose -f docker/docker-compose.yml up --build`
2. Access at `http://localhost:8003/docs`
3. *Troubleshooting*: If you see `KeyError: 'ContainerConfig'`, run `docker compose down`.

### 3. Production-Ready Deployment (Kubernetes/Helm)
The core of this DevOps showcase.
- **Local (Kind)**: `make setup-kind` -> `make build-image` -> `make deploy-all`.
- **Cloud (AKS/EKS)**: See the detailed [Kubernetes Guide](k8s/README.md).

---

## 📊 Observability
Reliability Hub is pre-configured for Prometheus.
- Setup Monitoring: [Monitoring Guide](monitoring/README.md)
- Custom Dashboards: [Grafana JSONs](monitoring/grafana/dashboards/)

## 🏗️ Infrastructure
Automate your cloud setup using Terraform.
- Cloud Provisioning: [Terraform Guide](terraform/README.md)

## 🤖 CI/CD
Fully automated pipeline using GitHub Actions.
- Workflow definition: [.github/workflows/ci.yml](.github/workflows/ci.yml)

## License
MIT
