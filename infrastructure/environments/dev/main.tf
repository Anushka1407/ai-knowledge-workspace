module "backend" {
  source = "../../modules/backend"

  resource_group_name     = var.resource_group_name
  location                = var.location
  container_registry_name = var.container_registry_name
  container_registry_sku  = var.container_registry_sku
  app_service_plan_name   = var.app_service_plan_name
  app_service_sku_name    = var.app_service_sku_name
  web_app_name            = var.web_app_name
  common_tags             = var.common_tags
  app_service_location    = var.app_service_location
}