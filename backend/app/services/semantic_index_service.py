import re
from collections.abc import Iterable
from typing import Any


class SemanticIndexService:
    """Simple semantic indexing layer for the AI Knowledge Workspace.

    This acts as the minimal scaffolding for the architecture's chunking and
    retrieval workflow before the Azure OpenAI embedding integration is added.
    """

    def __init__(self) -> None:
        self.indexed_chunks: list[dict[str, Any]] = []

    def chunk_text(self, content: str, chunk_size: int = 250, overlap: int = 50) -> list[str]:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if overlap < 0:
            raise ValueError("overlap must be non-negative")
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        normalized = re.sub(r"\s+", " ", content).strip()
        if not normalized:
            return []

        if len(normalized) <= chunk_size:
            return [normalized]

        chunks: list[str] = []
        step = chunk_size - overlap
        start = 0

        while start < len(normalized):
            end = min(start + chunk_size, len(normalized))
            chunk = normalized[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end == len(normalized):
                break
            start += step

        return chunks

    def index_document(self, document_id: str, paragraphs: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        indexed: list[dict[str, Any]] = []

        for paragraph in paragraphs:
            text = str(paragraph.get("content", "")).strip()
            if not text:
                continue

            page_number = paragraph.get("page_number", 1)
            chunks = self.chunk_text(text)
            for chunk in chunks:
                record = {
                    "document_id": document_id,
                    "page_number": page_number,
                    "content": chunk,
                    "score": 0.0,
                    "vector": self._fake_vector(chunk),
                }
                indexed.append(record)
                self.indexed_chunks.append(record)

        return indexed

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if not query or top_k <= 0:
            return []

        query_terms = {term.lower() for term in re.findall(r"\b\w+\b", query)}
        if not query_terms:
            return []

        scored = []
        for item in self.indexed_chunks:
            content = str(item["content"]).lower()
            content_terms = set(re.findall(r"\b\w+\b", content))
            overlap = len(query_terms & content_terms)
            if overlap == 0:
                continue
            item_copy = dict(item)
            item_copy["score"] = overlap
            scored.append(item_copy)

        scored.sort(key=lambda entry: entry["score"], reverse=True)
        return scored[:top_k]

    def _fake_vector(self, chunk: str) -> list[float]:
        text = re.sub(r"\W+", " ", chunk.lower()).strip()
        if not text:
            return [0.0]
        tokens = text.split()
        return [float(len(tokens)), float(len(chunk))] 
