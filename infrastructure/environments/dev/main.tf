module "backend" {
  source = "../../modules/backend"

  resource_group_name        = var.resource_group_name
  location                   = var.location
  container_registry_name    = var.container_registry_name
  container_registry_sku     = var.container_registry_sku
  app_service_plan_name      = var.app_service_plan_name
  app_service_sku_name       = var.app_service_sku_name
  web_app_name               = var.web_app_name
  common_tags                = var.common_tags
  app_service_location       = var.app_service_location
  storage_account_name       = var.storage_account_name
  document_intelligence_name = var.document_intelligence_name
  storage_container_name     = var.storage_container_name
}

module "frontend" {
  source = "../../modules/frontend"

  resource_group_name = var.resource_group_name
  location            = var.static_web_app_location
  static_web_app_name = var.static_web_app_name
  common_tags         = var.common_tags
}