# Monitoring Setup Guide

This project uses the standard Prometheus Community Helm charts for production-grade monitoring.

## 1. Add Helm Repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

## 2. Install Prometheus Stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

## 3. Access Grafana

1. Get the admin password:
   ```bash
   kubectl get secret --namespace monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
   ```
2. Port-forward to Grafana:
   ```bash
   kubectl port-forward --namespace monitoring service/monitoring-grafana 3000:80
   ```
3. Login at `http://localhost:3000` with username `admin`.

## 4. Import Dashboards

Import the JSON files located in `monitoring/grafana/dashboards/` into Grafana to see Reliability Hub metrics.
