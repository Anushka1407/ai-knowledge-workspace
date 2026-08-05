resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.common_tags
}

resource "azurerm_container_registry" "this" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = var.container_registry_sku
  admin_enabled       = false
  tags                = var.common_tags
}

resource "azurerm_service_plan" "this" {
  name                = var.app_service_plan_name
  resource_group_name = azurerm_resource_group.this.name
  location            = var.app_service_location
  os_type             = "Linux"
  sku_name            = var.app_service_sku_name
  tags                = var.common_tags
}

resource "azurerm_linux_web_app" "this" {
  name                = var.web_app_name
  resource_group_name = azurerm_resource_group.this.name
  location            = var.app_service_location
  service_plan_id     = azurerm_service_plan.this.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on = true

    application_stack {
      docker_image_name        = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      docker_registry_url      = "https://mcr.microsoft.com"
    }
  }

  tags = var.common_tags
}