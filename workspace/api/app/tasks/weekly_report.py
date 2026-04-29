"""
Async task for generating weekly reports.
"""
from app.tasks.celery_app import celery_app


@celery_app.task(bind=True)
def generate_weekly_report_task(self, project_id: int, user_id: int):
    """Generate weekly report for a project."""
    return {"project_id": project_id, "status": "generated"}
