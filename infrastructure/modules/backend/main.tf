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
  resource_group_name = var.resource_group_name
  location            = var.app_service_location
  service_plan_id     = azurerm_service_plan.this.id

  https_only = true

  ftp_publish_basic_authentication_enabled       = false
  webdeploy_publish_basic_authentication_enabled = false

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    WEBSITES_PORT                       = "8000"
  }

  site_config {
    always_on                               = false
    container_registry_use_managed_identity = true
    ftps_state                              = "FtpsOnly"

    application_stack {
      docker_image_name   = var.docker_image_name
      docker_registry_url = "https://${var.container_registry_login_server}"
    }
  }

  logs {
    detailed_error_messages = false
    failed_request_tracing  = false

    http_logs {
      file_system {
        retention_in_days = 3
        retention_in_mb   = 100
      }
    }
  }

  tags = var.common_tags
}