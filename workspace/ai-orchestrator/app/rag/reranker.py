"""
Document reranking module.

Combines results from multiple retrieval sources (Milvus vector search
and Elasticsearch BM25) and reranks them using a hybrid scoring approach.
"""
from app.rag.milvus_store import DocResult


class HybridReranker:
    """
    Hybrid reranker that merges results from vector and text search
    using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self, k: int = 60, vector_weight: float = 0.6, text_weight: float = 0.4):
        """
        Args:
            k: RRF constant - controls how much rank position matters
            vector_weight: Weight for Milvus vector results
            text_weight: Weight for Elasticsearch results
        """
        self.k = k
        self.vector_weight = vector_weight
        self.text_weight = text_weight

    def rerank(self, vector_results: list[DocResult], text_results: list[DocResult], top_k: int = 5) -> list[DocResult]:
        """
        Merge and rerank results using RRF.

        RRF score = sum(1 / (k + rank_i)) for each source i
        Final score = vector_weight * vector_rrf + text_weight * text_rrf
        """
        # Build rank maps: doc_id -> rank (1-based)
        vector_ranks: dict[str, int] = {doc.id: i + 1 for i, doc in enumerate(vector_results)}
        text_ranks: dict[str, int] = {doc.id: i + 1 for i, doc in enumerate(text_results)}

        # All unique doc IDs
        all_ids = set(vector_ranks.keys()) | set(text_ranks.keys())

        # Calculate RRF scores
        scores: dict[str, float] = {}
        doc_map: dict[str, DocResult] = {}
        for doc_id in all_ids:
            vec_rank = vector_ranks.get(doc_id, len(vector_results) + 1)
            txt_rank = text_ranks.get(doc_id, len(text_results) + 1)

            vec_rrf = 1.0 / (self.k + vec_rank)
            txt_rrf = 1.0 / (self.k + txt_rank)

            scores[doc_id] = self.vector_weight * vec_rrf + self.text_weight * txt_rrf

            # Keep the doc with the highest individual score
            vec_doc = vector_ranks.get(doc_id)
            txt_doc = text_ranks.get(doc_id)
            if vec_doc is not None:
                doc_map[doc_id] = vector_results[vec_doc - 1]
            else:
                doc_map[doc_id] = text_results[txt_doc - 1]

        # Sort by RRF score descending
        sorted_ids = sorted(all_ids, key=lambda x: scores[x], reverse=True)

        results = []
        for doc_id in sorted_ids[:top_k]:
            doc = doc_map[doc_id]
            # Update score with reranked value
            doc.score = round(scores[doc_id], 4)
            results.append(doc)

        return results


class ScoreFusionReranker:
    """
    Simple score fusion reranker - normalizes scores from different
    sources and combines them linearly.
    """

    def __init__(self, vector_weight: float = 0.6, text_weight: float = 0.4):
        self.vector_weight = vector_weight
        self.text_weight = text_weight

    def rerank(self, vector_results: list[DocResult], text_results: list[DocResult], top_k: int = 5) -> list[DocResult]:
        """Normalize and fuse scores from both sources."""
        doc_map: dict[str, DocResult] = {}

        # Normalize vector scores to [0, 1]
        vec_scores = [d.score for d in vector_results]
        vec_min = min(vec_scores) if vec_scores else 0
        vec_max = max(vec_scores) if vec_scores else 1
        vec_range = vec_max - vec_min if vec_max != vec_min else 1

        for doc in vector_results:
            norm = (doc.score - vec_min) / vec_range
            doc_map[doc.id] = DocResult(
                id=doc.id,
                content=doc.content,
                score=norm * self.vector_weight,
                metadata=doc.metadata,
            )

        # Normalize text scores and merge
        txt_scores = [d.score for d in text_results]
        txt_min = min(txt_scores) if txt_scores else 0
        txt_max = max(txt_scores) if txt_scores else 1
        txt_range = txt_max - txt_min if txt_max != txt_min else 1

        for doc in text_results:
            norm = (doc.score - txt_min) / txt_range
            if doc.id in doc_map:
                doc_map[doc.id].score += norm * self.text_weight
            else:
                doc_map[doc.id] = DocResult(
                    id=doc.id,
                    content=doc.content,
                    score=norm * self.text_weight,
                    metadata=doc.metadata,
                )

        # Sort and return top_k
        sorted_docs = sorted(doc_map.values(), key=lambda d: d.score, reverse=True)
        return sorted_docs[:top_k]


def get_reranker() -> HybridReranker:
    """Get default reranker instance."""
    return HybridReranker()
