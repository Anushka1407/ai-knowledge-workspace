from fastapi.testclient import TestClient

from app.api.documents import (
    document_store,
    get_blob_service,
    get_document_intelligence_service,
    semantic_index_service,
)
from app.main import app


class FakeBlobService:
    def __init__(self):
        self.uploads = []

    def upload(self, blob_path, content):
        self.uploads.append((blob_path, content))


class FakeDocumentIntelligenceService:
    def analyze(self, content):
        return {"pages": [{"page_number": 1}], "paragraphs": [{"content": "Hello world"}]}


def test_upload_document_returns_processed_structure():
    document_store.clear()
    semantic_index_service.indexed_chunks.clear()

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
    assert body["paragraphs"] == [{"content": "Hello world"}]
    assert len(blob_service.uploads) == 1
    assert blob_service.uploads[0][1] == b"%PDF-1.7"


def test_search_documents_returns_ranked_results():
    document_store.clear()
    semantic_index_service.indexed_chunks.clear()

    blob_service = FakeBlobService()
    app.dependency_overrides[get_blob_service] = lambda: blob_service
    app.dependency_overrides[get_document_intelligence_service] = (
        lambda: FakeDocumentIntelligenceService()
    )

    try:
        upload_response = TestClient(app).post(
            "/documents/upload",
            files={"file": ("sample.pdf", b"%PDF-1.7", "application/pdf")},
        )
        search_response = TestClient(app).post(
            "/documents/search",
            json={"query": "hello world", "top_k": 5},
        )
    finally:
        app.dependency_overrides.clear()

    assert upload_response.status_code == 201
    assert search_response.status_code == 200
    payload = search_response.json()
    assert payload
    assert payload[0]["document_id"] == upload_response.json()["document_id"]
    assert "hello" in payload[0]["content"].lower()


def test_chat_documents_uses_retrieved_context():
    document_store.clear()
    semantic_index_service.indexed_chunks.clear()

    blob_service = FakeBlobService()
    app.dependency_overrides[get_blob_service] = lambda: blob_service
    app.dependency_overrides[get_document_intelligence_service] = (
        lambda: FakeDocumentIntelligenceService()
    )

    try:
        TestClient(app).post(
            "/documents/upload",
            files={"file": ("sample.pdf", b"%PDF-1.7", "application/pdf")},
        )
        response = TestClient(app).post(
            "/documents/chat",
            json={"question": "what does hello world say?", "top_k": 3},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert "hello" in payload["answer"].lower()
    assert payload["sources"]