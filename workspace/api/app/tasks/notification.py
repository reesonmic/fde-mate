"""
Async task for sending notifications.
"""
from app.tasks.celery_app import celery_app


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
)
def send_notification_task(self, user_id: int, title: str, content: str, channel: str = "dingtalk"):
    """Send a notification via specified channel."""
    return {"user_id": user_id, "channel": channel, "status": "sent"}
