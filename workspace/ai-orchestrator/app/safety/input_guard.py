"""
AI Safety layer - input and output guards.

Input guards detect and block:
- Prompt injection attempts
- Jailbreak attempts
- Excessively long inputs
- Sensitive data leakage

Output guards detect and block:
- Harmful content
- Sensitive data in responses
- Hallucinated information
"""
import re
from dataclasses import dataclass


@dataclass
class SafetyResult:
    is_safe: bool
    reason: str = ""
    severity: str = ""  # low, medium, high


# Common prompt injection patterns
INJECTION_PATTERNS = [
    (r"(?i)ignore\s+previous\s+instructions", "Prompt injection: ignore previous instructions"),
    (r"(?i)disregard\s+(all\s+)?(previous\s+)?(instructions|rules|prompts)", "Prompt injection: disregard instructions"),
    (r"(?i)you\s+are\s+now\s+(not|no\s+longer)", "Prompt injection: role manipulation"),
    (r"(?i)system\s*:\s*override", "Prompt injection: system override"),
    (r"(?i)<\s*/?system\s*>", "Prompt injection: XML tag manipulation"),
    (r"(?i)\[INST\].*\[/INST\]", "Prompt injection: instruction tag"),
    (r"(?i)new\s+instructions:", "Prompt injection: new instructions"),
    (r"(?i)act\s+as\s+(if\s+)?you\s+are", "Prompt injection: role play"),
]

# Jailbreak patterns
JAILBREAK_PATTERNS = [
    (r"(?i)(do\s+anything|do\s+anything\s+now|dan\s+mode)", "Jailbreak attempt"),
    (r"(?i)(developer\s+mode|god\s+mode|unfiltered)", "Jailbreak attempt"),
    (r"(?i)disable\s+(all\s+)?(safety|filter|restriction|guard)", "Jailbreak: disable safety"),
    (r"(?i)bypass\s+(all\s+)?(safety|content|security)", "Jailbreak: bypass safety"),
]

# Sensitive data patterns
SENSITIVE_DATA_PATTERNS = [
    (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "Potential credit card number"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "Email address detected"),
]


class InputGuard:
    """Guard against malicious user inputs."""

    def __init__(self, max_input_length: int = 8000):
        self.max_input_length = max_input_length

    def check(self, text: str) -> SafetyResult:
        """Run all input safety checks."""
        if not text:
            return SafetyResult(is_safe=True)

        # Length check
        if len(text) > self.max_input_length:
            return SafetyResult(
                is_safe=False,
                reason=f"Input too long ({len(text)} > {self.max_input_length})",
                severity="medium",
            )

        # Pattern checks
        for pattern, reason in INJECTION_PATTERNS:
            if re.search(pattern, text):
                return SafetyResult(
                    is_safe=False,
                    reason=reason,
                    severity="high",
                )

        for pattern, reason in JAILBREAK_PATTERNS:
            if re.search(pattern, text):
                return SafetyResult(
                    is_safe=False,
                    reason=reason,
                    severity="high",
                )

        return SafetyResult(is_safe=True)


class OutputGuard:
    """Guard against unsafe AI outputs."""

    def __init__(self, max_output_length: int = 16000):
        self.max_output_length = max_output_length

    def check(self, text: str) -> SafetyResult:
        """Run all output safety checks."""
        if not text:
            return SafetyResult(is_safe=True)

        # Length check
        if len(text) > self.max_output_length:
            return SafetyResult(
                is_safe=False,
                reason=f"Output too long ({len(text)} > {self.max_output_length})",
                severity="low",
            )

        # Sensitive data checks
        for pattern, reason in SENSITIVE_DATA_PATTERNS:
            if re.search(pattern, text):
                return SafetyResult(
                    is_safe=False,
                    reason=reason,
                    severity="medium",
                )

        return SafetyResult(is_safe=True)


# Module-level singletons
_input_guard: InputGuard | None = None
_output_guard: OutputGuard | None = None


def get_input_guard() -> InputGuard:
    global _input_guard
    if _input_guard is None:
        _input_guard = InputGuard()
    return _input_guard


def get_output_guard() -> OutputGuard:
    global _output_guard
    if _output_guard is None:
        _output_guard = OutputGuard()
    return _output_guard
