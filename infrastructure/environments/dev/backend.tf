terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state-uks"
    storage_account_name = "statfstate48291"
    container_name       = "tfstate"
    key                  = "ai-knowledge-workspace-dev.tfstate"
  }
}