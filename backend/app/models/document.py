from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ProcessedDocument(BaseModel):
    document_id: UUID
    status: str
    filename: str
    blob_path: str
    uploaded_at: datetime
    pages: list[dict[str, Any]]
    paragraphs: list[dict[str, Any]]