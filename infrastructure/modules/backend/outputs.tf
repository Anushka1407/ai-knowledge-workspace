output "web_app_url" {
  description = "URL of the backend web app."
  value       = "https://${azurerm_linux_web_app.this.default_hostname}"
}

output "storage_account_name" {
  description = "Name of the document storage account."
  value       = azurerm_storage_account.documents.name
}

output "document_intelligence_endpoint" {
  description = "Endpoint for Azure AI Document Intelligence."
  value       = azurerm_cognitive_account.document_intelligence.endpoint
}