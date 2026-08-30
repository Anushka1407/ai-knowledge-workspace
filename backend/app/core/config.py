import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    storage_account_url: str = os.getenv("AZURE_STORAGE_ACCOUNT_URL", "")
    storage_connection_string: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    storage_container_name: str = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "documents")
    document_intelligence_endpoint: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
    document_intelligence_key: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


settings = Settings()