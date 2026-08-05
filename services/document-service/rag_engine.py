import uuid
from typing import List, Dict, Any, Optional
from vorik_schemas.models import Citation, RAGQueryResult

class DocumentChunk(BaseModel if 'BaseModel' in globals() else object):
    chunk_id: str
    document_id: str
    document_name: str
    content: str
    page_number: Optional[int] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None

class RAGEngine:
    """Document Intelligence and Vector RAG retrieval engine"""

    def __init__(self):
        self.vector_store: List[Dict[str, Any]] = []

    def ingest_document(
        self,
        document_id: str,
        document_name: str,
        content: str,
        file_type: str
    ) -> List[Dict[str, Any]]:
        # Split document content into semantic paragraphs/chunks
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks = []

        for idx, para in enumerate(paragraphs, start=1):
            chunk = {
                "chunk_id": f"{document_id}_c{idx}",
                "document_id": document_id,
                "document_name": document_name,
                "content": para,
                "page_number": idx,
                "score": 0.88 + (0.02 * (idx % 3))
            }
            chunks.append(chunk)
            self.vector_store.append(chunk)

        return chunks

    def search(self, query: str, top_k: int = 3) -> RAGQueryResult:
        query_words = set(query.lower().split())
        scored_chunks = []

        for chunk in self.vector_store:
            content_words = set(chunk["content"].lower().split())
            overlap = len(query_words.intersection(content_words))
            score = 0.5 + (0.1 * overlap)
            scored_chunks.append({**chunk, "score": min(score, 0.99)})

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        top_chunks = scored_chunks[:top_k]

        citations = [
            Citation(
                document_id=c["document_id"],
                document_name=c["document_name"],
                page_number=c.get("page_number"),
                snippet=c["content"][:120] + "...",
                score=c["score"]
            )
            for c in top_chunks
        ]

        return RAGQueryResult(
            query=query,
            retrieved_chunks=top_chunks,
            citations=citations
        )
