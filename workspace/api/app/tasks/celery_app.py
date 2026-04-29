"""
Celery async task configuration.
"""
from celery import Celery

from app.config.settings import settings

celery_app = Celery(
    "fde_tasks",
    broker=settings.celery_broker_url if hasattr(settings, "celery_broker_url") else "redis://localhost:6379/1",
    backend=settings.celery_result_backend if hasattr(settings, "celery_result_backend") else "redis://localhost:6379/2",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
)
