"""
Unified retriever - combines vector search and full-text search
with reranking for optimal document retrieval.
"""
from dataclasses import dataclass, field

from app.config import settings

from app.rag.milvus_store import MilvusStore, DocResult
from app.rag.es_search import ElasticSearch
from app.rag.reranker import get_reranker, HybridReranker
from app.rag.embedder import get_embedder, Embedder


@dataclass
class RetrievalResult:
    """Final retrieval result with context for LLM prompt injection."""
    documents: list[DocResult]
    context_text: str
    source: str  # "vector" | "text" | "hybrid" | "none"

    def build_context(self) -> str:
        """Build a formatted context string from documents."""
        if not self.documents:
            return ""
        parts = []
        for i, doc in enumerate(self.documents, 1):
            parts.append(f"[{i}] {doc.content}")
        return "\n\n".join(parts)


class Retriever:
    """
    Unified document retriever that orchestrates vector search,
    full-text search, and reranking.
    """

    def __init__(
        self,
        milvus_store: MilvusStore | None = None,
        es: ElasticSearch | None = None,
        reranker: HybridReranker | None = None,
        embedder: Embedder | None = None,
    ):
        self._milvus = milvus_store or MilvusStore(embedder=embedder or get_embedder())
        self._es = es or ElasticSearch()
        self._reranker = reranker or get_reranker()

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        source_filter: str = "",
        user_id: int | None = None,
        project_id: int | None = None,
    ) -> RetrievalResult:
        """
        Retrieve relevant documents using hybrid search.

        1. Search Milvus for semantic similarity
        2. Search Elasticsearch for full-text match
        3. Rerank combined results
        4. Build context string
        """
        # Run both searches in parallel with timeout
        import asyncio
        vec_task = asyncio.create_task(
            self._milvus.search(query, top_k=top_k * 2, user_id=user_id, project_id=project_id)
        )
        txt_task = asyncio.create_task(
            self._es.search(query, top_k=top_k * 2, source_filter=source_filter, user_id=user_id)
        )

        vec_task = asyncio.wait_for(vec_task, timeout=10)
        txt_task = asyncio.wait_for(txt_task, timeout=10)

        vector_results, text_results = await asyncio.gather(vec_task, txt_task, return_exceptions=True)

        # Handle failures gracefully
        if isinstance(vector_results, Exception):
            vector_results = []
        if isinstance(text_results, Exception):
            text_results = []

        # Determine source
        has_vector = len(vector_results) > 0
        has_text = len(text_results) > 0

        if has_vector and has_text:
            # Hybrid: rerank both
            docs = self._reranker.rerank(vector_results, text_results, top_k=top_k)
            result = RetrievalResult(documents=docs, context_text="", source="hybrid")
        elif has_vector:
            result = RetrievalResult(documents=vector_results[:top_k], context_text="", source="vector")
        elif has_text:
            result = RetrievalResult(documents=text_results[:top_k], context_text="", source="text")
        else:
            result = RetrievalResult(documents=[], context_text="", source="none")

        # Build context
        result.context_text = result.build_context()
        return result

    async def index_document(self, doc_id: str, content: str, title: str = "", metadata: dict | None = None, source: str = "") -> bool:
        """Index a document in both vector and text stores."""
        ok1 = await self._milvus.upsert(doc_id, content, metadata, source)
        ok2 = await self._es.index(doc_id, content, title, metadata, source)
        return ok1 or ok2

    async def delete_document(self, doc_id: str) -> bool:
        """Delete a document from both stores."""
        ok1 = await self._milvus.delete(doc_id)
        ok2 = await self._es.delete(doc_id)
        return ok1 or ok2


# Module-level singleton
_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    """Get or create retriever singleton."""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever
