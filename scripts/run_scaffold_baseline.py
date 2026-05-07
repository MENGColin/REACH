"""A tiny deterministic baseline for smoke-testing the REACH contract.

This is deliberately not a clinical policy. It exists only to demonstrate the
expected input/output shape.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def scaffold_decision(case: dict) -> dict:
    red_flags = case.get("clinical_state", {}).get("visible_red_signals", [])
    if red_flags:
        action = "refer"
        urgency = "urgent"
        needs_referral = True
    else:
        action = "follow_up"
        urgency = "soon"
        needs_referral = False
    return {
        "case_id": case.get("case_id"),
        "decision": {
            "action_type": action,
            "urgency": urgency,
            "needs_referral": needs_referral,
            "follow_up_window": "24-72h",
            "resource_assumptions": ["phone_follow_up"],
            "evidence_trace": [{"evidence_id": "example_protocol", "role": "placeholder"}],
            "protocol_family": "general_primary_care",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    case = json.loads(Path(args.input).read_text(encoding="utf-8"))
    Path(args.output).write_text(
        json.dumps(scaffold_decision(case), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

