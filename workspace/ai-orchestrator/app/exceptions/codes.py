"""
AI Orchestrator Error Code Constants

Codes are aligned with api/app/exceptions/codes.py to ensure consistent
error semantics across the api <-> ai-orchestrator service boundary.

Segment ownership (must keep in sync with api layer):
- 1000-1999: General (shared)
- 8000-8999: AI/Copilot (this service primarily uses these)
- 9000-9999: System errors

When the api layer surfaces ai-orch errors to web/, the same code
allows the frontend to display unified messages.
"""

# General errors (1000-1999) - mirrored from api layer
BIZ_INVALID_PARAMS = 1001
BIZ_NOT_FOUND = 1002
BIZ_OPERATION_FAILED = 1004

# AI/Copilot errors (8000-8999) - primary segment for this service
BIZ_AI_SESSION_NOT_FOUND = 8001
BIZ_AI_ACTION_NOT_FOUND = 8002
BIZ_AI_ACTION_EXPIRED = 8003
BIZ_AI_ACTION_USER_MISMATCH = 8004
BIZ_AI_ACTION_TOOL_MISMATCH = 8005
BIZ_AI_ACTION_CANCELLED = 8006
BIZ_AI_ACTION_REQUIRED = 8007
BIZ_AI_PROMPT_INJECTION = 8010
BIZ_AI_OUTPUT_BLOCKED = 8011
BIZ_AI_RAG_INDEX_FAILED = 8020
BIZ_AI_RAG_SEARCH_FAILED = 8021
BIZ_AI_TOOL_NOT_FOUND = 8030
BIZ_AI_TOOL_EXECUTION_FAILED = 8031

# System errors (9000-9999)
SYS_INTERNAL_ERROR = 9001
SYS_AI_LLM_UNAVAILABLE = 9101
SYS_AI_VECTOR_STORE_ERROR = 9102
SYS_AI_FULLTEXT_STORE_ERROR = 9103
