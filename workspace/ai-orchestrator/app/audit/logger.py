"""
Audit logging for AI Orchestrator.

Records all AI interactions for compliance, debugging, and analytics:
- Chat requests and responses
- Tool calls and results
- RAG retrievals
- Safety guard triggers
- Provider usage and costs
"""
import json
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger("fde.audit")


@dataclass
class AuditEntry:
    """A single audit log entry."""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = ""  # chat_request, chat_response, tool_call, rag_retrieve, safety_block
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    assistant_id: Optional[str] = None
    input_preview: str = ""
    output_preview: str = ""
    provider: str = ""
    duration_ms: float = 0.0
    token_count: int = 0
    tool_calls: list[dict] = field(default_factory=list)
    rag_docs_count: int = 0
    safety_triggered: bool = False
    safety_reason: str = ""
    error: str = ""
    trace_id: str = ""
    metadata: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, default=str)


class AuditLogger:
    """Audit logger with file and in-memory logging."""

    def __init__(self, log_dir: str = "./logs", enabled: bool = True):
        self.enabled = enabled
        self._log_dir = Path(log_dir)
        self._handler_added = False
        if enabled:
            try:
                self._log_dir.mkdir(parents=True, exist_ok=True)
                log_file = self._log_dir / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
                self._file_handler = logging.FileHandler(str(log_file))
                self._file_handler.setFormatter(logging.Formatter("%(message)s"))
                # Prevent duplicate handlers
                if not logger.handlers:
                    logger.addHandler(self._file_handler)
                    self._handler_added = True
            except Exception as e:
                logging.getLogger("fde.audit").warning(
                    f"audit_log_dir_fallback: using stderr, path={log_dir}, error={e}"
                )
                self.enabled = False

    def log_chat(self, entry: AuditEntry):
        """Log a chat request/response."""
        if not self.enabled:
            return
        entry.event_type = "chat"
        self._log(entry)

    def log_tool_call(self, entry: AuditEntry):
        """Log a tool call."""
        if not self.enabled:
            return
        entry.event_type = "tool_call"
        self._log(entry)

    def log_rag(self, entry: AuditEntry):
        """Log a RAG retrieval."""
        if not self.enabled:
            return
        entry.event_type = "rag_retrieve"
        self._log(entry)

    def log_safety_block(self, entry: AuditEntry):
        """Log a safety guard trigger."""
        if not self.enabled:
            return
        entry.event_type = "safety_block"
        self._log(entry)

    def _log(self, entry: AuditEntry):
        """Write audit entry to log."""
        try:
            logger.info(entry.to_json())
        except Exception:
            pass  # Never let audit logging fail the main operation

    def close(self):
        """Close file handlers."""
        if hasattr(self, "_file_handler"):
            self._file_handler.close()
            logger.removeHandler(self._file_handler)


# Module-level singleton
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """Get or create audit logger singleton."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def create_entry(
    user_id: int | None = None,
    session_id: str | None = None,
    assistant_id: str | None = None,
    trace_id: str = "",
) -> AuditEntry:
    """Create a new audit entry with common fields."""
    return AuditEntry(
        user_id=user_id,
        session_id=session_id,
        assistant_id=assistant_id,
        trace_id=trace_id,
    )
