from fastapi.testclient import TestClient

from app.api.documents import get_blob_service, get_document_intelligence_service
from app.main import app


class FakeBlobService:
    def __init__(self):
        self.uploads = []

    def upload(self, blob_path, content):
        self.uploads.append((blob_path, content))


class FakeDocumentIntelligenceService:
    def analyze(self, content):
        return {"pages": [{"page_number": 1}], "paragraphs": [{"content": "Hello"}]}


def test_upload_document_returns_processed_structure():
    blob_service = FakeBlobService()
    app.dependency_overrides[get_blob_service] = lambda: blob_service
    app.dependency_overrides[get_document_intelligence_service] = (
        lambda: FakeDocumentIntelligenceService()
    )

    try:
        response = TestClient(app).post(
            "/documents/upload",
            files={"file": ("sample.pdf", b"%PDF-1.7", "application/pdf")},
        )
    finally:
        app.dependency_overrides.clear()

    body = response.json()
    assert response.status_code == 201
    assert body["status"] == "processed"
    assert body["filename"] == "sample.pdf"
    assert body["pages"] == [{"page_number": 1}]
    assert body["paragraphs"] == [{"content": "Hello"}]
    assert len(blob_service.uploads) == 1
    assert blob_service.uploads[0][1] == b"%PDF-1.7"