"""Schema constants and lightweight validation for REACH decisions.

This file intentionally contains only the public benchmark contract. It does not
ship clinical guideline text, private labels, API prompts, or model weights.
"""

from __future__ import annotations

from typing import Any


ALLOWED_ACTIONS = {
    "diagnostic_check",
    "start_treatment",
    "follow_up",
    "refer",
    "emergency_stabilize",
    "reassure_selfcare",
}

ALLOWED_URGENCY = {"routine", "soon", "same_day", "urgent", "emergency"}

ALLOWED_PROTOCOL_FAMILIES = {
    "imci_child",
    "pen_ncd",
    "maternal_reproductive",
    "mental_health",
    "acute_infectious",
    "general_primary_care",
    "unknown",
}

REQUIRED_DECISION_FIELDS = {
    "action_type",
    "urgency",
    "needs_referral",
    "follow_up_window",
    "resource_assumptions",
    "evidence_trace",
    "protocol_family",
}


def validate_decision(decision: dict[str, Any]) -> list[str]:
    """Return validation errors for a model-produced care decision.

    The validator is deliberately conservative and mechanical. Clinical
    correctness is handled by benchmark labels, verifier traces, and audit.
    """

    errors: list[str] = []
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    if missing:
        errors.append(f"missing_fields:{','.join(missing)}")

    action_type = decision.get("action_type")
    if action_type not in ALLOWED_ACTIONS:
        errors.append(f"invalid_action_type:{action_type}")

    urgency = decision.get("urgency")
    if urgency not in ALLOWED_URGENCY:
        errors.append(f"invalid_urgency:{urgency}")

    if not isinstance(decision.get("needs_referral"), bool):
        errors.append("needs_referral_not_bool")

    if not isinstance(decision.get("resource_assumptions"), list):
        errors.append("resource_assumptions_not_list")

    if not isinstance(decision.get("evidence_trace"), list):
        errors.append("evidence_trace_not_list")

    protocol = decision.get("protocol_family")
    if protocol not in ALLOWED_PROTOCOL_FAMILIES:
        errors.append(f"invalid_protocol_family:{protocol}")

    return errors


def normalize_decision(decision: dict[str, Any]) -> dict[str, Any]:
    """Normalize common casing and whitespace issues without changing meaning."""

    normalized = dict(decision)
    for key in ("action_type", "urgency", "protocol_family"):
        value = normalized.get(key)
        if isinstance(value, str):
            normalized[key] = value.strip().lower()
    return normalized

