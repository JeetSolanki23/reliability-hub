# Reliability Hub Helm Chart

This Helm chart deploys the Reliability Hub application (API and Background Worker) on a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

## Configuration

The following table lists the configurable parameters of the Reliability Hub chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of API replicas | `1` |
| `image.repository` | Docker image name | `reliability-hub` |
| `image.tag` | Docker image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Kubernetes Service type | `ClusterIP` |
| `service.port` | Kubernetes Service port | `8003` |
| `databaseUrl` | Full PostgreSQL connection URL | `postgresql://user:password@reliability-hub-postgresql:5432/reliabilityhub` |
| `ingress.enabled` | Enable Ingress controller | `false` |
| `ingress.hosts` | Ingress hostnames | `reliability-hub.local` |

## Installation

### From local directory
```bash
helm install my-release ./k8s/charts/reliability-hub
```

### Uninstallation
```bash
helm uninstall my-release
```

## Internal vs External Database

By default, the chart expects a database at the URL provided in `databaseUrl`.

1. **Internal (Development)**: You can install a PostgreSQL chart (like `bitnami/postgresql`) into the same namespace.
2. **External (Production)**: Use a managed service like Azure Database for PostgreSQL and update the `databaseUrl`.

## Monitoring Integration

The API deployment includes annotations for Prometheus scraping. Ensure you have a Prometheus instance running in your cluster that respects these annotations:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8003"
```
