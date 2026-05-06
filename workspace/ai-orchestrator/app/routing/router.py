"""
Multi-model router with fallback and circuit breaker.

Routes LLM requests across multiple providers with automatic
failover when a provider becomes unhealthy.
"""
from typing import AsyncIterator

from app.config import settings
from app.llm.provider import LlmProvider, DashScopeLlm, OpenAiLlm, MockLlm
from app.routing.circuit_breaker import CircuitBreaker, CircuitBreakerConfig


class MultiModelRouter:
    """
    Routes LLM requests across configured providers.

    Priority order: dashscope -> openai -> mock
    If primary fails, falls back to next provider.
    Uses circuit breakers to avoid hammering failing providers.
    """

    def __init__(self):
        self._providers: dict[str, tuple[LlmProvider, CircuitBreaker]] = {}
        self._primary_order: list[str] = []
        self._init_providers()

    def _init_providers(self):
        """Initialize provider pool."""
        if settings.dashscope_api_key:
            self._providers["dashscope"] = (
                DashScopeLlm(),
                CircuitBreaker(
                    name="dashscope",
                    config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30.0),
                ),
            )
            self._primary_order.append("dashscope")

        if settings.openai_api_key:
            self._providers["openai"] = (
                OpenAiLlm(),
                CircuitBreaker(
                    name="openai",
                    config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=30.0),
                ),
            )
            self._primary_order.append("openai")

        # Mock is always available as fallback (no circuit breaker)
        self._providers["mock"] = (MockLlm(), None)
        self._primary_order.append("mock")

    async def stream(self, messages: list[dict], preferred: str | None = None) -> AsyncIterator[str]:
        """
        Stream response from the best available provider.

        Args:
            messages: Conversation messages
            preferred: Preferred provider name (optional)
        """
        order = list(self._primary_order)
        if preferred and preferred in order:
            # Move preferred to front
            order.remove(preferred)
            order.insert(0, preferred)

        last_error = None
        for provider_name in order:
            provider, cb = self._providers.get(provider_name, (None, None))
            if provider is None:
                continue

            # Mock doesn't need circuit breaker
            if provider_name == "mock":
                async for chunk in provider.stream(messages):
                    yield chunk
                return

            # Try provider through circuit breaker
            if cb and cb.can_execute():
                try:
                    async for chunk in provider.stream(messages):
                        yield chunk
                    return
                except Exception as e:
                    last_error = e
                    # Record failure in circuit breaker
                    cb._on_failure()
                    continue

        # All providers failed - fallback to mock (should always work)
        mock_provider, _ = self._providers.get("mock", (MockLlm(), None))
        async for chunk in mock_provider.stream(messages):
            yield chunk

    def get_provider_status(self) -> list[dict]:
        """Get status of all providers."""
        status = []
        for name, (provider, cb) in self._providers.items():
            info = {
                "name": name,
                "type": type(provider).__name__,
            }
            if cb:
                info.update(cb.stats)
            else:
                info["state"] = "always_available"
                info["is_healthy"] = True
            status.append(info)
        return status


# Module-level singleton
_router: MultiModelRouter | None = None


def get_router() -> MultiModelRouter:
    """Get or create router singleton."""
    global _router
    if _router is None:
        _router = MultiModelRouter()
    return _router
