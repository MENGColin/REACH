"""Verifier-routed candidate selection skeleton."""

from __future__ import annotations

from typing import Any

from .metrics import component_index
from .verifiers import run_hard_verifiers


def candidate_score(candidate: dict[str, Any], state: dict[str, Any]) -> float:
    """Score a candidate with public mechanical checks.

    This is not the full manuscript scorer. It illustrates the routing contract
    without exposing private rubrics or clinical evidence assets.
    """

    traces = run_hard_verifiers(
        candidate,
        state.get("facility_context", {}),
        state.get("evidence_context", {}),
    )
    components = {
        trace["name"]: 1.0 if trace["passed"] else 0.0
        for trace in traces
    }
    return component_index(components)


def select_candidate(candidates: list[dict[str, Any]], state: dict[str, Any]) -> dict[str, Any]:
    if not candidates:
        raise ValueError("select_candidate requires at least one candidate")
    return max(candidates, key=lambda candidate: candidate_score(candidate, state))

