# Data Statement

This repository does not contain the full REACH benchmark data. It contains only schemas, examples, and public scaffolding code.

The manuscript describes a benchmark snapshot with 49,286 structured cases, 142,613 case-facility pairs, 8,198 OOD stress cases, 1,184 facility profiles, 228,955 accepted training transitions, and 812 expert-audited trajectories.

The full data release should be hosted separately with a dataset card and explicit versioning. Any restricted real-derived abstractions should be released only as metadata when permitted, and raw private records should not be redistributed.

## Intended Use

REACH is intended for research on healthcare-agent evaluation, resource-constrained decision-making, verifier-guided policies, and robustness analysis.

## Out-of-Scope Use

REACH must not be used for clinical deployment, patient triage, diagnosis, treatment recommendation, or substitution for professional medical judgment.

## Known Limitations

- Synthetic and abstracted cases may not reflect all real-world clinical variation.
- Facility ledgers are survey-style readiness abstractions, not live inventories.
- LLM-generated environment feedback can be plausible but wrong.
- Expert audit improves quality control but does not make the benchmark a clinical authority.

