"""
Elasticsearch full-text search integration.

Provides document indexing and BM25-based text search
as a complement to Milvus vector similarity search.
"""
from dataclasses import dataclass, field

from app.config import settings

from app.rag.milvus_store import DocResult


class ElasticSearch:
    """Elasticsearch full-text search for document retrieval."""

    INDEX_NAME = "fde_documents"

    def __init__(self) -> None:
        self._client = None
        self._connected = False

    def _ensure_client(self):
        """Lazy-connect to Elasticsearch."""
        if self._connected:
            return
        try:
            from elasticsearch import AsyncElasticsearch
            self._client = AsyncElasticsearch(
                settings.es_host,
                request_timeout=10,
            )
            # Create index if not exists
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're in async context, create index lazily
                pass
            else:
                if not self._client.indices.exists(index=self.INDEX_NAME):
                    self._client.indices.create(
                        index=self.INDEX_NAME,
                        mappings={
                            "properties": {
                                "content": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_smart"},
                                "title": {"type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_smart"},
                                "source": {"type": "keyword"},
                                "doc_type": {"type": "keyword"},
                                "metadata": {"type": "object"},
                                "created_at": {"type": "date"},
                            }
                        },
                    )
            self._connected = True
        except Exception:
            self._connected = False

    async def index(self, doc_id: str, content: str, title: str = "", metadata: dict | None = None, source: str = "", doc_type: str = "") -> bool:
        """Index a document for full-text search."""
        self._ensure_client()
        if not self._connected:
            return False
        try:
            from datetime import datetime, timezone
            await self._client.index(
                index=self.INDEX_NAME,
                id=doc_id,
                document={
                    "content": content,
                    "title": title,
                    "source": source,
                    "doc_type": doc_type,
                    "metadata": metadata or {},
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            return True
        except Exception:
            return False

    async def search(self, query: str, top_k: int = 5, source_filter: str = "", user_id: int | None = None) -> list[DocResult]:
        """Full-text search using BM25."""
        self._ensure_client()
        if not self._connected:
            return []
        try:
            must_clauses = [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["content^2", "title^3"],
                        "type": "best_fields",
                    }
                }
            ]
            if source_filter:
                must_clauses.append({"term": {"source": source_filter}})
            if user_id is not None:
                must_clauses.append({"term": {"metadata.user_id": str(user_id)}})

            response = await self._client.search(
                index=self.INDEX_NAME,
                query={"bool": {"must": must_clauses}},
                size=top_k,
            )
            docs = []
            for hit in response["hits"]["hits"]:
                docs.append(DocResult(
                    id=hit["_id"],
                    content=hit["_source"].get("content", ""),
                    score=hit.get("_score", 0.0),
                    metadata=hit["_source"].get("metadata", {}),
                ))
            return docs
        except Exception:
            return []

    async def delete(self, doc_id: str) -> bool:
        """Delete a document from the index."""
        self._ensure_client()
        if not self._connected:
            return False
        try:
            await self._client.delete(index=self.INDEX_NAME, id=doc_id)
            return True
        except Exception:
            return False
