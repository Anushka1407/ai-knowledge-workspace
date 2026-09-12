output "static_web_app_url" {
  description = "Default URL for the frontend static web app."
  value       = "https://${azurerm_static_web_app.this.default_host_name}"
}

output "static_web_app_name" {
  description = "Name of the Azure Static Web App resource."
  value       = azurerm_static_web_app.this.name
}
