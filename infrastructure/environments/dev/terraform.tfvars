location             = "uksouth"
app_service_location = "canadacentral"

resource_group_name = "rg-portfolio-dev-uks"

container_registry_name = "acrportfoliodev48291"
container_registry_sku  = "Basic"

app_service_plan_name = "asp-portfolio-dev-uks"
app_service_sku_name  = "B1"

web_app_name = "app-portfolio-api-dev-uks"

container_registry_login_server = "acrportfoliodev48291.azurecr.io"

docker_image_name = "acrportfoliodev48291.azurecr.io/ai-knowledge-backend:e6a147c3f086c49c3928bf17886a23b9ff2829fd"

common_tags = {
  environment = "dev"
  managed_by  = "terraform"
  project     = "portfolio"
}