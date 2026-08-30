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

resource "azurerm_storage_account" "documents" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = var.common_tags
}

resource "azurerm_storage_container" "documents" {
  name                  = var.storage_container_name
  storage_account_id    = azurerm_storage_account.documents.id
  container_access_type = "private"
}

resource "azurerm_cognitive_account" "document_intelligence" {
  name                = var.document_intelligence_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  kind                = "FormRecognizer"
  sku_name            = "S0"
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

  app_settings = {
    AZURE_STORAGE_ACCOUNT_URL            = azurerm_storage_account.documents.primary_blob_endpoint
    AZURE_STORAGE_CONTAINER_NAME         = azurerm_storage_container.documents.name
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = azurerm_cognitive_account.document_intelligence.endpoint
  }

  site_config {
    always_on = true

    application_stack {
      docker_image_name   = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      docker_registry_url = "https://mcr.microsoft.com"
    }
  }

  tags = var.common_tags
}

resource "azurerm_role_assignment" "web_app_blob_contributor" {
  scope                = azurerm_storage_account.documents.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_web_app.this.identity[0].principal_id
}

resource "azurerm_role_assignment" "web_app_acr_pull" {
  scope                = azurerm_container_registry.this.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.this.identity[0].principal_id
}

resource "azurerm_role_assignment" "web_app_document_intelligence_user" {
  scope                = azurerm_cognitive_account.document_intelligence.id
  role_definition_name = "Cognitive Services User"
  principal_id         = azurerm_linux_web_app.this.identity[0].principal_id
}