"""
Circuit breaker pattern for LLM providers.

Protects against cascading failures when an LLM provider
becomes unhealthy by temporarily stopping requests to it.

States:
- CLOSED: Normal operation, requests flow through
- OPEN: Provider is failing, requests are rejected immediately
- HALF_OPEN: Testing if provider recovered, limited requests allowed
"""
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5       # Consecutive failures before opening
    recovery_timeout: float = 60.0    # Seconds before trying half-open
    half_open_max_calls: int = 3      # Max test calls in half-open


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""
    pass


@dataclass
class CircuitBreaker:
    """Circuit breaker for a single provider."""
    name: str
    config: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)

    _state: CircuitState = CircuitState.CLOSED
    _failure_count: int = 0
    _last_failure_time: float = 0.0
    _half_open_calls: int = 0
    _last_success_time: float = 0.0
    _total_calls: int = 0
    _total_failures: int = 0

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            # Check if recovery timeout has elapsed
            if time.time() - self._last_failure_time >= self.config.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
        return self._state

    def can_execute(self) -> bool:
        """Check if a request can be sent to this provider."""
        state = self.state  # May trigger state transition
        if state == CircuitState.CLOSED:
            return True
        if state == CircuitState.HALF_OPEN:
            return self._half_open_calls < self.config.half_open_max_calls
        return False  # OPEN

    async def execute(self, func, *args, **kwargs):
        """Execute a function through the circuit breaker."""
        if not self.can_execute():
            raise CircuitBreakerError(
                f"Circuit breaker '{self.name}' is OPEN. "
                f"Provider unavailable (failed {self._failure_count} times). "
                f"Retry after {self.config.recovery_timeout}s."
            )

        self._total_calls += 1
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Record a successful call."""
        self._failure_count = 0
        self._last_success_time = time.time()
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            self._half_open_calls = 0

    def _on_failure(self):
        """Record a failed call."""
        self._failure_count += 1
        self._total_failures += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN:
            # Failed during recovery test - go back to open
            self._state = CircuitState.OPEN
        elif self._failure_count >= self.config.failure_threshold:
            self._state = CircuitState.OPEN

    def reset(self):
        """Manually reset the circuit breaker."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0

    @property
    def is_healthy(self) -> bool:
        return self.state != CircuitState.OPEN

    @property
    def stats(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self._failure_count,
            "total_calls": self._total_calls,
            "total_failures": self._total_failures,
            "is_healthy": self.is_healthy,
        }
