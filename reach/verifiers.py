"""Mechanical verifier scaffolds for REACH.

These checks are intentionally simple and public. The full benchmark uses
versioned clinical labels, expert audit, and facility ledgers.
"""

from __future__ import annotations

from typing import Any

from .schemas import validate_decision


def schema_verifier(decision: dict[str, Any]) -> dict[str, Any]:
    errors = validate_decision(decision)
    return {
        "name": "schema_verifier",
        "passed": len(errors) == 0,
        "errors": errors,
    }


def resource_verifier(decision: dict[str, Any], facility: dict[str, Any]) -> dict[str, Any]:
    """Check whether declared resources are listed in the facility ledger."""

    available = set(facility.get("available_resources", []))
    required = set(decision.get("resource_assumptions", []))
    missing = sorted(required - available)
    return {
        "name": "resource_verifier",
        "passed": len(missing) == 0,
        "missing_resources": missing,
    }


def evidence_trace_verifier(decision: dict[str, Any], evidence_context: dict[str, Any]) -> dict[str, Any]:
    """Check that cited evidence ids exist in the supplied evidence context."""

    allowed_ids = set(evidence_context.get("evidence_ids", []))
    cited = {
        item.get("evidence_id")
        for item in decision.get("evidence_trace", [])
        if isinstance(item, dict)
    }
    missing = sorted(eid for eid in cited if eid and eid not in allowed_ids)
    return {
        "name": "evidence_trace_verifier",
        "passed": len(missing) == 0,
        "unknown_evidence_ids": missing,
    }


def run_hard_verifiers(
    decision: dict[str, Any],
    facility: dict[str, Any],
    evidence_context: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        schema_verifier(decision),
        resource_verifier(decision, facility),
        evidence_trace_verifier(decision, evidence_context),
    ]

