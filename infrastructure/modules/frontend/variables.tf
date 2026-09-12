variable "resource_group_name" {
  description = "Name of the Azure resource group."
  type        = string
}

variable "location" {
  description = "Azure region for the frontend static web app."
  type        = string
}

variable "static_web_app_name" {
  description = "Name of the Azure Static Web App for the React frontend."
  type        = string
}

variable "common_tags" {
  description = "Common tags applied to all Azure resources."
  type        = map(string)
}
