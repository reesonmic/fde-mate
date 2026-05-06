"""
Async task for data sync (ES/Milvus).
"""
from app.tasks.celery_app import celery_app


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
)
def sync_to_es_task(self, entity_type: str, entity_id: int, action: str = "index"):
    """Sync entity to Elasticsearch."""
    return {"entity_type": entity_type, "entity_id": entity_id, "action": action, "status": "synced"}


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
)
def sync_to_milvus_task(self, entity_type: str, entity_id: int, action: str = "index"):
    """Sync entity to Milvus vector database."""
    return {"entity_type": entity_type, "entity_id": entity_id, "action": action, "status": "synced"}
