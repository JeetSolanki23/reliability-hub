# Infrastructure as Code (Terraform)

This directory contains Terraform configurations to automate the provisioning of cloud resources.

## Strategy

The project is designed to be **cloud-agnostic**. While the application runs on Kubernetes (which is portable), the underlying infrastructure (K8s Cluster, Container Registry, Database) is provisioned using cloud-specific providers.

## Structure

```text
terraform/
├── modules/              # Reusable infrastructure blocks (Future)
└── environments/
    └── dev/             # Environment-specific configuration
        └── main.tf      # Primary entry point
```

## Getting Started (Azure Example)

Currently, the focus is on Azure (AKS).

### Prerequisites
- [Terraform CLI](https://developer.hashicorp.com/terraform/downloads)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

### Deployment
1. **Login**: `az login`
2. **Initialize**:
   ```bash
   cd terraform/environments/dev
   terraform init
   ```
3. **Plan**:
   ```bash
   terraform plan
   ```
4. **Apply**:
   ```bash
   terraform apply
   ```

## Managed Resources

The Terraform scripts manage:
- **Resource Group**: Logical container for all resources.
- **AKS Cluster**: Managed Kubernetes service.
- **ACR**: Azure Container Registry for storing Docker images.
- **VNET/Subnet**: Network isolation.

## Customization

To change regions or resource names, modify the variables in `main.tf` or provide a `terraform.tfvars` file.
