"""
Crypto utilities - JWT token utilities.
"""
import hashlib
import secrets


def generate_token(length: int = 32) -> str:
    """Generate a random secure token."""
    return secrets.token_hex(length)


def hash_sha256(data: str) -> str:
    """Generate SHA-256 hash."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def verify_hash(data: str, hash_value: str) -> bool:
    """Verify data against hash."""
    return hash_sha256(data) == hash_value
