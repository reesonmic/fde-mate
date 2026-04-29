"""
DingTalk Client (mock implementation).
"""
import logging

logger = logging.getLogger(__name__)


class DingTalkClient:
    """Client for DingTalk messaging."""

    def __init__(self, app_key: str = "", app_secret: str = ""):
        self.app_key = app_key
        self.app_secret = app_secret

    async def send_message(self, user_id: int, title: str, content: str) -> bool:
        logger.info(f"Sending DingTalk message to user {user_id}: {title} (mock)")
        return True

    async def send_group_message(self, group_id: str, content: str) -> bool:
        logger.info(f"Sending DingTalk group message to {group_id} (mock)")
        return True
