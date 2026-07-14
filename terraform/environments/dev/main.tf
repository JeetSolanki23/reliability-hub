provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "rg-reliability-hub-dev"
  location = "Central India"
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-reliability-hub-dev"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "reliabilityhubdev"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Development"
  }
}

resource "azurerm_container_registry" "main" {
  name                = "acrreliabilityhubdev"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Standard"
  admin_enabled       = true
}

resource "azurerm_role_assignment" "aks_acr" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}
