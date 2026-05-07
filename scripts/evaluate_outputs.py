"""Evaluate REACH-style prediction files against gold files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reach.metrics import evaluate_records, load_json_or_jsonl  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", required=True, help="Gold JSON or JSONL file")
    parser.add_argument("--pred", required=True, help="Prediction JSON or JSONL file")
    args = parser.parse_args()

    gold = load_json_or_jsonl(args.gold)
    pred = load_json_or_jsonl(args.pred)
    metrics = evaluate_records(gold, pred)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

