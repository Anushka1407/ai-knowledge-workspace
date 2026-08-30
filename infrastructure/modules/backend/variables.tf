variable "resource_group_name" {
  description = "Name of the Azure resource group."
  type        = string
}

variable "location" {
  description = "Azure region for the resources."
  type        = string
}

variable "container_registry_name" {
  description = "Globally unique name of the Azure Container Registry."
  type        = string
}

variable "container_registry_sku" {
  description = "SKU for the Azure Container Registry."
  type        = string
  default     = "Basic"
}

variable "app_service_plan_name" {
  description = "Name of the Linux App Service Plan."
  type        = string
}

variable "app_service_sku_name" {
  description = "SKU of the App Service Plan."
  type        = string
  default     = "B1"
}

variable "web_app_name" {
  description = "Name of the Linux Web App."
  type        = string
}

variable "common_tags" {
  description = "Common tags applied to all Azure resources."

  type = map(string)
}

variable "app_service_location" {
  description = "Azure region for the App Service Plan and Web App."
  type        = string
}

variable "storage_account_name" {
  description = "Globally unique Azure Storage account name."
  type        = string
}

variable "document_intelligence_name" {
  description = "Name of the Azure AI Document Intelligence resource."
  type        = string
}

variable "storage_container_name" {
  description = "Blob container used for uploaded documents."
  type        = string
  default     = "documents"
}