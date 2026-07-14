# Kubernetes Deployment Guide

This directory contains the Kubernetes manifests and Helm charts to deploy Reliability Hub.

## 1. Local Deployment (Kind)

The easiest way to test the deployment locally is using the provided `Makefile` in the root directory.

### Prerequisites
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Helm](https://helm.sh/docs/intro/install/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

### Steps
1. **Create Cluster**:
   ```bash
   make setup-kind
   ```
   This creates a cluster named `reliability-hub` and installs the NGINX Ingress Controller.

2. **Build and Load Image**:
   ```bash
   make build-image
   make load-image
   ```
   This builds the Docker image locally and sideloads it into the Kind nodes so Kubernetes can pull it without a registry.

3. **Deploy with Helm**:
   ```bash
   make deploy-all
   ```
   This installs the `reliability-hub` chart.

4. **Verify**:
   ```bash
   kubectl get pods
   ```

## 2. Helm Chart Usage

We use a modular Helm chart located in `./charts/reliability-hub`.

### Installation
```bash
helm install [RELEASE_NAME] ./charts/reliability-hub
```

### Configuration
You can override default values using a `custom-values.yaml` file:
```bash
helm install reliability-hub ./charts/reliability-hub -f custom-values.yaml
```

Key parameters to configure:
- `databaseUrl`: The connection string for your PostgreSQL database.
- `image.repository`: The Docker image to use.
- `ingress.enabled`: Set to `true` to enable external access.

## 3. Production Deployment (AKS/EKS/GKE)

For production, follow these steps:

1. **Provision Infrastructure**: Use the Terraform configurations in `/terraform`.
2. **Configure Context**: Ensure your `kubectl` is pointed to your cloud cluster.
3. **Database**: We recommend using a managed database service (like Azure Database for PostgreSQL). Update the `databaseUrl` in `values.yaml` accordingly.
4. **Deploy Monitoring**: Follow the instructions in `/monitoring/README.md` to install Prometheus and Grafana first.
5. **Install App**:
   ```bash
   helm upgrade --install reliability-hub ./charts/reliability-hub \
     --set databaseUrl="your-production-db-url" \
     --set ingress.enabled=true \
     --set ingress.hosts[0].host="reliability-hub.yourdomain.com"
   ```

## 4. Troubleshooting

- **Image Pull Errors**: Ensure the image tag matches what was built or pushed. In Kind, use `make load-image`.
- **Database Connection**: Ensure the PostgreSQL service is reachable from the Kubernetes pods. Check the `DATABASE_URL` secret.
- **Ingress Not Working**: On Kind, ensure you waited for the NGINX Ingress Controller pods to be `Ready`.
