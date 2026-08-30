from typing import Any

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential

from app.core.config import settings


class DocumentIntelligenceService:
    def __init__(self) -> None:
        if not settings.document_intelligence_endpoint:
            raise RuntimeError("Azure Document Intelligence configuration is missing")
        credential = (
            AzureKeyCredential(settings.document_intelligence_key)
            if settings.document_intelligence_key
            else DefaultAzureCredential()
        )
        self.client = DocumentIntelligenceClient(
            endpoint=settings.document_intelligence_endpoint,
            credential=credential,
        )

    def analyze(self, content: bytes) -> dict[str, list[dict[str, Any]]]:
        poller = self.client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=AnalyzeDocumentRequest(bytes_source=content),
        )
        result = poller.result()
        pages = [
            {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "line_count": len(page.lines or []),
            }
            for page in result.pages or []
        ]
        paragraphs = [
            {"content": paragraph.content, "role": paragraph.role}
            for paragraph in result.paragraphs or []
        ]
        return {"pages": pages, "paragraphs": paragraphs}