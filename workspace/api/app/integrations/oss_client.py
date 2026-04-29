"""
OSS Client (mock implementation).
"""
import logging

logger = logging.getLogger(__name__)


class OssClient:
    """Client for Aliyun OSS."""

    def __init__(self, endpoint: str = "", access_key: str = "", secret_key: str = "", bucket: str = ""):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket

    async def generate_sts_token(self, object_key: str) -> dict:
        """Generate STS token for direct upload."""
        logger.info(f"Generating STS token for {object_key} (mock)")
        return {
            "access_key_id": "mock-ak",
            "access_key_secret": "mock-sk",
            "security_token": "mock-token",
            "expiration": "2026-12-31T23:59:59Z",
        }

    async def delete_object(self, object_key: str) -> bool:
        logger.info(f"Deleting OSS object {object_key} (mock)")
        return True

    async def get_download_url(self, object_key: str, expires: int = 3600) -> str:
        return f"https://{self.bucket}.{self.endpoint}/{object_key}?expires={expires}"
