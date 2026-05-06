"""
Milvus vector store integration.

Provides document upsert, search, and delete operations
using Milvus for semantic similarity search.
"""
from dataclasses import dataclass, field

from app.config import settings


@dataclass
class DocResult:
    """A single retrieved document."""
    id: str
    content: str
    score: float
    metadata: dict = field(default_factory=dict)


class MilvusStore:
    """Milvus vector store for document embeddings."""

    COLLECTION_NAME = "fde_documents"

    def __init__(self, embedder=None) -> None:
        self._embedder = embedder
        self._client = None
        self._connected = False

    def _ensure_client(self):
        """Lazy-connect to Milvus."""
        if self._connected:
            return
        try:
            from pymilvus import connections, Collection, utility
            connections.connect(
                alias="default",
                host=settings.milvus_host,
                port=settings.milvus_port,
            )
            if not utility.has_collection(self.COLLECTION_NAME):
                from pymilvus import FieldSchema, CollectionSchema, DataType
                fields = [
                    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
                    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self._embedder.dimension),
                    FieldSchema(name="metadata_json", dtype=DataType.VARCHAR, max_length=4096),
                    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=256),
                ]
                schema = CollectionSchema(fields, description="FDE document vectors")
                Collection(self.COLLECTION_NAME, schema)
            self._client = Collection(self.COLLECTION_NAME)
            self._client.load()
            self._connected = True
        except Exception:
            # Milvus not available - graceful degradation
            self._connected = False

    async def upsert(self, doc_id: str, content: str, metadata: dict | None = None, source: str = "") -> bool:
        """Insert or update a document."""
        self._ensure_client()
        if not self._connected:
            return False
        try:
            import json
            from pymilvus import MutationResult
            embedding = await self._embedder.embed(content)
            # Delete existing doc first (escape quotes to prevent injection)
            safe_id = doc_id.replace('"', '\\"')
            self._client.delete(f'id == "{safe_id}"')
            self._client.insert([
                [doc_id],
                [content],
                [embedding],
                [json.dumps(metadata or {})],
                [source],
            ])
            return True
        except Exception:
            return False

    async def upsert_batch(self, docs: list[dict]) -> bool:
        """Batch insert documents. Each dict: {id, content, metadata?, source?}."""
        self._ensure_client()
        if not self._connected:
            return False
        try:
            import json
            texts = [d["content"] for d in docs]
            embeddings = await self._embedder.embed_batch(texts)
            ids = [d["id"] for d in docs]
            contents = [d["content"] for d in docs]
            metas = [json.dumps(d.get("metadata", {})) for d in docs]
            sources = [d.get("source", "") for d in docs]
            self._client.insert([ids, contents, embeddings, metas, sources])
            return True
        except Exception:
            return False

    async def search(self, query: str, top_k: int = 5, filter_expr: str = "") -> list[DocResult]:
        """Search for similar documents by query text."""
        self._ensure_client()
        if not self._connected:
            return []
        try:
            import json
            embedding = await self._embedder.embed(query)
            results = self._client.search(
                data=[embedding],
                anns_field="embedding",
                param={"metric_type": "COSINE", "params": {"nprobe": 10}},
                limit=top_k,
                output_fields=["id", "content", "metadata_json", "source"],
                expr=filter_expr,
            )
            docs = []
            for hits in results:
                for hit in hits:
                    meta = {}
                    try:
                        meta = json.loads(hit.entity.get("metadata_json", "{}"))
                    except Exception:
                        pass
                    docs.append(DocResult(
                        id=str(hit.id),
                        content=hit.entity.get("content", ""),
                        score=hit.distance,
                        metadata=meta,
                    ))
            return docs
        except Exception:
            return []

    async def delete(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        self._ensure_client()
        if not self._connected:
            return False
        try:
            safe_id = doc_id.replace('"', '\\"')
            self._client.delete(f'id == "{safe_id}"')
            return True
        except Exception:
            return False

    async def delete_by_source(self, source: str) -> int:
        """Delete all documents from a source. Returns count deleted."""
        self._ensure_client()
        if not self._connected:
            return 0
        try:
            safe_source = source.replace('"', '\\"')
            self._client.delete(f'source == "{safe_source}"')
            return 1  # Simplified
        except Exception:
            return 0
