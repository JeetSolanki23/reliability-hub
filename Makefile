.PHONY: setup-kind build-image load-image deploy-all clean-kind help

CLUSTER_NAME=reliability-hub

help:
	@echo "Usage:"
	@echo "  make setup-kind    - Create Kind cluster and install NGINX Ingress"
	@echo "  make build-image   - Build the Reliability Hub Docker image"
	@echo "  make load-image    - Load the image into Kind"
	@echo "  make deploy-all    - Deploy everything using Helm"
	@echo "  make clean-kind    - Delete the Kind cluster"

setup-kind:
	kind create cluster --name $(CLUSTER_NAME) --config kind-config.yaml
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

build-image:
	docker build -f docker/Dockerfile -t reliability-hub:latest .

load-image:
	kind load docker-image reliability-hub:latest --name $(CLUSTER_NAME)

deploy-all:
	helm install reliability-hub ./k8s/charts/reliability-hub

clean-kind:
	kind delete cluster --name $(CLUSTER_NAME)
