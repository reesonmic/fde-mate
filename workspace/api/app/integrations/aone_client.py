"""
Aone Client (mock implementation).
"""
import logging

logger = logging.getLogger(__name__)


class AoneClient:
    """Client for Aone (internal project management system)."""

    def __init__(self, base_url: str = "", token: str = ""):
        self.base_url = base_url
        self.token = token

    async def get_tasks(self, project_id: int) -> list[dict]:
        logger.info(f"Fetching Aone tasks for project {project_id} (mock)")
        return []

    async def create_task(self, project_id: int, title: str, description: str) -> dict:
        logger.info(f"Creating Aone task in project {project_id} (mock)")
        return {"id": 0, "title": title}
