from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings

from app.core.config import settings


class BlobStorageService:
    def __init__(self) -> None:
        if settings.storage_connection_string:
            self.client = BlobServiceClient.from_connection_string(
                settings.storage_connection_string
            )
        elif settings.storage_account_url:
            self.client = BlobServiceClient(
                account_url=settings.storage_account_url,
                credential=DefaultAzureCredential(),
            )
        else:
            raise RuntimeError("Azure Blob Storage configuration is missing")

    def upload(self, blob_path: str, content: bytes) -> None:
        container = self.client.get_container_client(settings.storage_container_name)
        container.upload_blob(
            name=blob_path,
            data=content,
            overwrite=False,
            content_settings=ContentSettings(content_type="application/pdf"),
        )