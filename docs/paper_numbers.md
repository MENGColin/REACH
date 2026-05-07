# Manuscript-Aligned Numbers

This file records the public-facing numerical snapshot used by the current NeurIPS 2026 manuscript draft. Update this file when the paper version changes.

## Benchmark Scale

| Quantity | Value |
|---|---:|
| Structured cases | 49,286 |
| Case-facility pairs | 142,613 |
| OOD stress cases | 8,198 |
| Facility profiles | 1,184 |
| Accepted training transitions | 228,955 |
| Expert-audited trajectories | 812 |
| Atomic rubric criteria | 4,872 |

## Key Results

| Setting | Method | Result |
|---|---|---:|
| ID test | Local SFT policy | 0.672 [0.651, 0.692] |
| ID test | REACH-VRC | 0.803 [0.787, 0.819] |
| Closed-loop rollout | Prompted baseline | 0.482 [0.458, 0.505] |
| Closed-loop rollout | SFT policy | 0.604 [0.579, 0.627] |
| Closed-loop rollout | REACH-VRC | 0.758 [0.728, 0.785] |
| OOD stress | SFT policy | 0.601 [0.578, 0.624] |
| OOD stress | GRPO | 0.661 [0.638, 0.683] |
| OOD stress | RAPO-memory | 0.712 [0.686, 0.738] |
| OOD stress | REACH-VRC | 0.765 [0.741, 0.789] |
| Pair-level robustness | Local SFT | 0.654 [0.628, 0.679] |
| Pair-level robustness | RAPO-memory | 0.735 [0.706, 0.763] |
| Pair-level robustness | REACH-VRC | 0.776 [0.748, 0.804] |

## Rare-Action Support

The canonical test set includes 809 diagnostic-check cases, 306 emergency-stabilization cases, and 681 follow-up-primary cases.

