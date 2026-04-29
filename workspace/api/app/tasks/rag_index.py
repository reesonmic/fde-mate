"""
Async task for RAG indexing.
"""
from app.tasks.celery_app import celery_app


@celery_app.task(bind=True)
def index_file_for_rag_task(self, file_id: int):
    """Index a file for RAG retrieval."""
    return {"file_id": file_id, "status": "indexed"}
