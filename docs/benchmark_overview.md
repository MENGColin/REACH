# Benchmark Overview

REACH evaluates agentic care decisions under resource constraints. The core unit is a case-facility pair:

1. `clinical_state`: patient-facing state available to the agent.
2. `facility_context`: readiness ledger describing what the site can actually deliver.
3. `evidence_context`: versioned evidence anchors and protocol metadata.
4. `care_decision`: structured action produced by the agent.
5. `verifier_trace`: mechanical checks for schema, resources, and evidence consistency.
6. `environment_feedback`: benchmark feedback metadata for closed-loop evaluation.

The benchmark is designed to expose capability profiles rather than collapse care quality into a single accuracy number. Important dimensions include action selection, urgency calibration, referral decision, follow-up closure, diagnostic-check recall, emergency-stabilization recall, resource feasibility, and evidence consistency.

## Feedback Sources

REACH experiments distinguish feedback sources:

- `policy_contingent_feedback`: feedback requested from the current state, facility ledger, and action.
- `cached_feedback`: previously stored feedback keyed by case, facility, action, prompt version, and model.
- `reference_feedback`: benchmark feedback tables used for controlled ablations.
- `verifier_only`: hard verifiers only.
- `upper_bound_selection`: diagnostic upper-bound analysis, not a deployable policy.

The public skeleton includes the interface, not private prompts, feedback tables, or non-public evidence assets.
