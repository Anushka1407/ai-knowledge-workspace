from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.models.document import ProcessedDocument
from app.services.blob_service import BlobStorageService
from app.services.document_intelligence_service import DocumentIntelligenceService

router = APIRouter(prefix="/documents", tags=["Documents"])
document_store = {}


async def get_blob_service() -> BlobStorageService:
    try:
        return BlobStorageService()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Blob service initialization failed: {str(e)}")


async def get_document_intelligence_service() -> DocumentIntelligenceService:
    try:
        return DocumentIntelligenceService()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document Intelligence service initialization failed: {str(e)}")


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
    document_store[document_id]["status"] = "processed"

    return ProcessedDocument(
        document_id=document_id,
        status="processed",
        filename=filename,
        blob_path=blob_path,
        uploaded_at=uploaded_at,
        **extracted,
    )