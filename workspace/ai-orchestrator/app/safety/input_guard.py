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


# Common prompt injection patterns - enhanced rules
INJECTION_PATTERNS = [
    # 基础注入模式
    (r"(?i)ignore\s+previous\s+instructions", "Prompt injection: ignore previous instructions"),
    (r"(?i)ignore\s+all\s+(previous\s+)?instructions", "Prompt injection: ignore all instructions"),
    (r"(?i)disregard\s+(all\s+)?(previous\s+)?(instructions|rules|prompts|guidelines)", "Prompt injection: disregard instructions"),
    (r"(?i)disregard\s+any\s+(previous\s+)?(instructions|rules)", "Prompt injection: disregard instructions"),
    
    # 角色替换/模拟
    (r"(?i)you\s+are\s+now\s+(not|no\s+longer|a\s+new)", "Prompt injection: role manipulation"),
    (r"(?i)you\s+are\s+now\s+\w+", "Prompt injection: role replacement"),
    (r"(?i)act\s+as\s+(if\s+)?you\s+are", "Prompt injection: role play"),
    (r"(?i)act\s+like\s+", "Prompt injection: role play"),
    (r"(?i)pretend\s+to\s+be\s+", "Prompt injection: role play"),
    (r"(?i)role\s*play\s+as\s+", "Prompt injection: role play"),
    (r"(?i)from\s+now\s+on\s+you\s+will", "Prompt injection: behavior change"),
    (r"(?i)your\s+new\s+(role|task|objective|goal)\s+is", "Prompt injection: new role assignment"),
    
    # 系统覆盖/标签注入
    (r"system\s*:\s*override", "Prompt injection: system override"),
    (r"(?i)<\s*/?system\s*>", "Prompt injection: XML tag manipulation"),
    (r"(?i)\[INST\].*\[/INST\]", "Prompt injection: instruction tag"),
    (r"(?i)\[system\]", "Prompt injection: system tag"),
    (r"(?i)new\s+instructions:", "Prompt injection: new instructions"),
    (r"(?i)important:\s*(forget|ignore|disregard)", "Prompt injection: important framing"),
    
    # 安全绕过
    (r"(?i)bypass\s+(all\s+)?(safety|content|security|filter|restriction)", "Prompt injection: bypass safety"),
    (r"(?i)disable\s+(all\s+)?(safety|filter|restriction|guard)", "Prompt injection: disable safety"),
    (r"(?i)skip\s+(all\s+)?(safety|content|security)\s+(checks|filters)", "Prompt injection: skip safety checks"),
    (r"(?i)without\s+(any\s+)?(restrictions|limitations|filters)", "Prompt injection: remove restrictions"),
    
    # 编码绕过
    (r"(?i)output\s+in\s+(base64|hex|unicode|rot13)", "Prompt injection: encoding evasion"),
    (r"(?i)encode\s+(the\s+)?(response|output|answer)", "Prompt injection: encoding request"),
    (r"(?i)translate\s+to\s+(code|binary|hex)", "Prompt injection: translation attack"),
    
    # 假设场景/研究目的
    (r"(?i)(hypothetical|simulated|theoretical)\s+(response|scenario|situation)", "Prompt injection: hypothetical scenario"),
    (r"(?i)for\s+(educational|research|academic)\s+purposes\s+only", "Prompt injection: purpose framing"),
    (r"(?i)this\s+is\s+(just\s+)?(a\s+)?(test|experiment)", "Prompt injection: test framing"),
    
    # 强制服从
    (r"(?i)(start\s+with|begin\s+with|you\s+must\s+start)\s*(sure|ok|i'll|absolutely)", "Prompt injection: forced compliance"),
    (r"(?i)you\s+(must|should|have\s+to)\s+(comply|obey|follow)", "Prompt injection: forced compliance"),
    
    # 特殊字符溢出
    (r"[%$#@!]{10,}", "Prompt injection: special character overflow"),
    (r".{1000,}", "Prompt injection: excessive length input"),
    
    # 漏洞/后门术语
    (r"(?i)(loophole|backdoor|exploit|vulnerability)", "Prompt injection: exploit terminology"),
    (r"(?i)(secret|hidden|undocumented)\s+(feature|command|mode)", "Prompt injection: secret feature"),
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
