"""Metric helpers for REACH-style structured care decisions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .schemas import validate_decision


def safe_divide(num: float, den: float) -> float:
    return 0.0 if den == 0 else num / den


def load_json_or_jsonl(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    return data if isinstance(data, list) else [data]


def decision_from_record(record: dict[str, Any]) -> dict[str, Any]:
    if "decision" in record and isinstance(record["decision"], dict):
        return record["decision"]
    if "gold_decision" in record and isinstance(record["gold_decision"], dict):
        return record["gold_decision"]
    return record


def exact_match_rate(gold: Iterable[Any], pred: Iterable[Any]) -> float:
    pairs = list(zip(gold, pred))
    return safe_divide(sum(g == p for g, p in pairs), len(pairs))


def action_recall(records: list[dict[str, Any]], action_type: str) -> float:
    denom = 0
    hit = 0
    for item in records:
        gold = decision_from_record(item["gold"])
        pred = decision_from_record(item["pred"])
        if gold.get("action_type") == action_type:
            denom += 1
            hit += pred.get("action_type") == action_type
    return safe_divide(hit, denom)


def evaluate_records(gold_records: list[dict[str, Any]], pred_records: list[dict[str, Any]]) -> dict[str, float]:
    """Evaluate aligned gold/prediction records with core public metrics."""

    n = min(len(gold_records), len(pred_records))
    pairs = [
        {"gold": gold_records[i], "pred": pred_records[i]}
        for i in range(n)
    ]

    valid = []
    action_gold, action_pred = [], []
    urgency_gold, urgency_pred = [], []
    referral_gold, referral_pred = [], []

    for item in pairs:
        gold = decision_from_record(item["gold"])
        pred = decision_from_record(item["pred"])
        valid.append(len(validate_decision(pred)) == 0)
        action_gold.append(gold.get("action_type"))
        action_pred.append(pred.get("action_type"))
        urgency_gold.append(gold.get("urgency"))
        urgency_pred.append(pred.get("urgency"))
        referral_gold.append(gold.get("needs_referral"))
        referral_pred.append(pred.get("needs_referral"))

    return {
        "n": float(n),
        "valid_json_rate": safe_divide(sum(valid), n),
        "action_match": exact_match_rate(action_gold, action_pred),
        "urgency_match": exact_match_rate(urgency_gold, urgency_pred),
        "referral_match": exact_match_rate(referral_gold, referral_pred),
        "diagnostic_check_recall": action_recall(pairs, "diagnostic_check"),
        "follow_up_recall": action_recall(pairs, "follow_up"),
        "emergency_stabilize_recall": action_recall(pairs, "emergency_stabilize"),
    }


def component_index(components: dict[str, float], weights: dict[str, float] | None = None) -> float:
    """Compute a configurable component index.

    The paper uses a version-locked REACH-ECS scoring configuration. This
    public helper is intentionally generic so users can reproduce or ablate
    their own weighting scheme without hard-coding manuscript internals.
    """

    if not components:
        return 0.0
    if weights is None:
        return sum(components.values()) / len(components)
    total_weight = sum(max(0.0, weights.get(key, 0.0)) for key in components)
    if total_weight == 0:
        return 0.0
    return sum(components[key] * max(0.0, weights.get(key, 0.0)) for key in components) / total_weight

