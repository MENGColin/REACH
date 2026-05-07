"""Minimal executable care-circuit interface for REACH."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .verifiers import run_hard_verifiers


class FeedbackProvider(Protocol):
    def __call__(
        self,
        state: dict[str, Any],
        decision: dict[str, Any],
        verifier_trace: list[dict[str, Any]],
    ) -> dict[str, Any]:
        ...


@dataclass
class ReachCircuit:
    """A lightweight environment shell.

    Policy-contingent feedback, cached feedback, and reference benchmark
    feedback can all be implemented behind the same FeedbackProvider interface.
    """

    feedback_provider: FeedbackProvider | None = None

    def step(self, state: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        facility = state.get("facility_context", {})
        evidence = state.get("evidence_context", {})
        verifier_trace = run_hard_verifiers(decision, facility, evidence)
        feedback = {}
        if self.feedback_provider is not None:
            feedback = self.feedback_provider(state, decision, verifier_trace)
        return {
            "case_id": state.get("case_id"),
            "decision": decision,
            "verifier_trace": verifier_trace,
            "environment_feedback": feedback,
        }


def null_feedback_provider(
    state: dict[str, Any],
    decision: dict[str, Any],
    verifier_trace: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "feedback_type": "null",
        "note": "No environment feedback provider was configured.",
    }
