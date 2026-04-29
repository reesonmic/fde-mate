"""
CRM Client (mock implementation).
"""
import logging

logger = logging.getLogger(__name__)


class CrmClient:
    """Client for CRM system."""

    def __init__(self, base_url: str = "", token: str = ""):
        self.base_url = base_url
        self.token = token

    async def get_customer(self, customer_id: int) -> dict | None:
        logger.info(f"Fetching CRM customer {customer_id} (mock)")
        return None

    async def sync_customer(self, data: dict) -> dict:
        logger.info(f"Syncing CRM customer (mock)")
        return {"id": 0, **data}
