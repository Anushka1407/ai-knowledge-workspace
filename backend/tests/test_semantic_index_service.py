from app.services.semantic_index_service import SemanticIndexService


def test_chunk_text_splits_large_content_into_multiple_chunks():
    service = SemanticIndexService()
    content = "word " * 200

    chunks = service.chunk_text(content, chunk_size=80, overlap=20)

    assert len(chunks) > 1
    assert all(len(chunk) <= 90 for chunk in chunks)
    assert all(chunk.strip() for chunk in chunks)


def test_index_document_and_search_returns_relevant_chunks():
    service = SemanticIndexService()
    paragraphs = [
        {"content": "The project uses Python for AI pipelines and vector search.", "page_number": 1},
        {"content": "Users upload documents and ask questions about the source material.", "page_number": 1},
    ]

    service.index_document("doc-1", paragraphs)
    results = service.search("vector search in AI pipeline", top_k=1)

    assert results
    assert results[0]["document_id"] == "doc-1"
    assert "vector" in results[0]["content"].lower()
