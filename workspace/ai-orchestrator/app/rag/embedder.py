"""
Text embedding service - supports DashScope and local mock embeddings.
"""
from abc import ABC, abstractmethod

from app.config import settings


class Embedder(ABC):
    """Abstract embedding provider."""

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        pass


class DashScopeEmbedder(Embedder):
    """DashScope text embedding via OpenAI-compatible API."""

    _dimension = 1536

    def __init__(self) -> None:
        from langchain_openai import OpenAIEmbeddings
        self._embeddings = OpenAIEmbeddings(
            model=settings.dashscope_embedding_model,
            openai_api_key=settings.dashscope_api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    async def embed(self, text: str) -> list[float]:
        result = await self._embeddings.aembed_query(text)
        return result

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        results = await self._embeddings.aembed_documents(texts)
        return results

    @property
    def dimension(self) -> int:
        return self._dimension


class MockEmbedder(Embedder):
    """Mock embedder for development/testing - returns deterministic hash-based vectors."""

    _dimension = 128

    async def embed(self, text: str) -> list[float]:
        return self._hash_vector(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._hash_vector(t) for t in texts]

    @property
    def dimension(self) -> int:
        return self._dimension

    def _hash_vector(self, text: str) -> list[float]:
        """Generate a deterministic pseudo-random vector from text."""
        import hashlib
        h = hashlib.md5(text.encode()).hexdigest()
        # Seed a simple PRNG from the hash
        seed = int(h[:8], 16)
        vec = []
        for i in range(self._dimension):
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            vec.append((seed % 1000 - 500) / 500.0)
        return vec


def get_embedder() -> Embedder:
    """Get embedding provider based on configuration."""
    if settings.llm_provider == "dashscope" and settings.dashscope_api_key:
        return DashScopeEmbedder()
    return MockEmbedder()
