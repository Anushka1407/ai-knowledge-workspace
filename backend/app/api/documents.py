from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status

from app.models.document import ProcessedDocument
from app.services.blob_service import BlobStorageService
from app.services.document_intelligence_service import DocumentIntelligenceService
from app.services.semantic_index_service import SemanticIndexService

router = APIRouter(prefix="/documents", tags=["Documents"])
document_store = {}
semantic_index_service = SemanticIndexService()


async def get_blob_service() -> BlobStorageService:
    try:
        return BlobStorageService()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Blob service initialization failed: {e!s}") from e


async def get_document_intelligence_service() -> DocumentIntelligenceService:
    try:
        return DocumentIntelligenceService()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Document Intelligence service initialization failed: {e!s}") from e


@router.post("/upload", response_model=ProcessedDocument, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),  # noqa: B008
    blob_service: BlobStorageService = Depends(get_blob_service),  # noqa: B008
    document_intelligence: DocumentIntelligenceService = Depends(  # noqa: B008
        get_document_intelligence_service
    ),
) -> ProcessedDocument:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    content = await file.read()
    document_id = uuid4()
    filename = file.filename or "document.pdf"
    blob_path = f"{document_id}/{filename}"
    uploaded_at = datetime.now(timezone.utc)
    document_store[document_id] = {
        "document_id": document_id,
        "filename": filename,
        "blob_path": blob_path,
        "uploaded_at": uploaded_at,
        "status": "uploaded",
    }
    blob_service.upload(blob_path, content)
    extracted = document_intelligence.analyze(content)
    semantic_index_service.index_document(str(document_id), extracted.get("paragraphs", []))
    document_store[document_id]["status"] = "processed"

    return ProcessedDocument(
        document_id=document_id,
        status="processed",
        filename=filename,
        blob_path=blob_path,
        uploaded_at=uploaded_at,
        **extracted,
    )


@router.post("/search")
async def search_documents(
    query: str = Body(..., embed=False),
    top_k: int = Body(5, embed=False),
) -> list[dict[str, object]]:
    """Return the highest-scoring indexed chunks for the supplied query."""
    if not query or not str(query).strip():
        return []

    search_results = semantic_index_service.search(str(query), top_k=top_k)
    enriched_results: list[dict[str, object]] = []

    for item in search_results:
        document_id = str(item["document_id"])
        document = document_store.get(document_id)
        if document is None:
            document = document_store.get(item.get("document_id"))

        enriched_results.append(
            {
                "document_id": document_id,
                "filename": (document or {}).get("filename"),
                "blob_path": (document or {}).get("blob_path"),
                "page_number": item.get("page_number"),
                "content": item["content"],
                "score": item["score"],
            }
        )

    return enriched_results