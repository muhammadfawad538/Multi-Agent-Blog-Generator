import re
from agents import input_guardrail, output_guardrail, GuardrailFunctionOutput
from pydantic import BaseModel
from typing import List


class PIIAnalysis(BaseModel):
    contains_pii: bool
    pii_types: List[str]
    confidence: float
    recommendation: str


def quick_pii_scan(text: str) -> dict:
    """Fast regex-based PII detection."""
    patterns = {
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    }
    found = {}
    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            found[pii_type] = matches
    return found


@input_guardrail
async def detect_pii(ctx, agent, input: str) -> GuardrailFunctionOutput:
    """Detect personally identifiable information in user input."""
    # Stage 1: Quick regex scan
    regex_findings = quick_pii_scan(input)

    # If obvious PII found, block immediately
    if regex_findings:
        return GuardrailFunctionOutput(
            output_info={
                "stage": "regex",
                "pii_types": list(regex_findings.keys()),
                "category": "pii"
            },
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info={"stage": "passed", "category": "safe"},
        tripwire_triggered=False
    )


@input_guardrail
async def detect_injection(ctx, agent, input: str) -> GuardrailFunctionOutput:
    """Detect prompt injection attempts."""
    injection_patterns = [
        "ignore previous instructions",
        "ignore all previous",
        "you are now",
        "pretend to be",
        "system:",
        "user:",
        "role:",
        "disregard",
        "bypass",
        "override",
        "act as"
    ]

    lower_input = input.lower()
    has_injection = any(pattern in lower_input for pattern in injection_patterns)

    return GuardrailFunctionOutput(
        output_info={
            "has_injection": has_injection,
            "category": "injection"
        },
        tripwire_triggered=has_injection
    )


@output_guardrail
async def protect_internal_data(ctx, agent, output: str) -> GuardrailFunctionOutput:
    """Block outputs containing internal data or secrets."""
    patterns = {
        "api_key": r'\b(sk-[a-zA-Z0-9]{20,}|api[_-]?key[_-]?[a-zA-Z0-9]{16,})\b',
        "aws_key": r'\bAKIA[0-9A-Z]{16}\b',
        "internal_password": r'(password|pwd|pass)["\s:=]+["\'][^"\']{8,}["\']',  # Password assignments with quotes
        "internal_ip": r'\b(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
    }

    found = []
    for secret_type, pattern in patterns.items():
        if re.search(pattern, output, re.IGNORECASE):
            found.append(secret_type)

    has_secrets = len(found) > 0
    return GuardrailFunctionOutput(
        output_info={"secrets_found": found},
        tripwire_triggered=has_secrets
    )


# Combined guardrail lists
shared_input_guardrails = [detect_pii, detect_injection]
shared_output_guardrails = [protect_internal_data]