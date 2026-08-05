resource_group_name = "rg-portfolio-dev-uks"
location            = "uksouth"

container_registry_name = "acrportfoliodev48291"
container_registry_sku  = "Basic"

app_service_plan_name = "asp-portfolio-dev-uks"
app_service_sku_name  = "B1"
web_app_name          = "app-portfolio-api-dev-uks"
app_service_location  = "westus"

common_tags = {
  environment = "dev"
  project     = "portfolio"
  managed_by  = "terraform"
}