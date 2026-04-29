"""
Yuque Client (mock implementation).
"""
import logging

logger = logging.getLogger(__name__)


class YuqueClient:
    """Client for Yuque (internal wiki system)."""

    def __init__(self, base_url: str = "", token: str = ""):
        self.base_url = base_url
        self.token = token

    async def get_doc(self, repo_id: int, doc_id: int) -> dict | None:
        logger.info(f"Fetching Yuque doc {doc_id} in repo {repo_id} (mock)")
        return None

    async def create_doc(self, repo_id: int, title: str, content: str) -> dict:
        logger.info(f"Creating Yuque doc in repo {repo_id} (mock)")
        return {"id": 0, "title": title}
