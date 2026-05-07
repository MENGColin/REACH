from reach.metrics import evaluate_records


def test_evaluate_records_smoke():
    gold = [
        {
            "gold_decision": {
                "action_type": "follow_up",
                "urgency": "soon",
                "needs_referral": False,
                "follow_up_window": "24-72h",
                "resource_assumptions": ["phone_follow_up"],
                "evidence_trace": [{"evidence_id": "example_protocol"}],
                "protocol_family": "imci_child",
            }
        }
    ]
    pred = [
        {
            "decision": {
                "action_type": "follow_up",
                "urgency": "soon",
                "needs_referral": False,
                "follow_up_window": "24-72h",
                "resource_assumptions": ["phone_follow_up"],
                "evidence_trace": [{"evidence_id": "example_protocol"}],
                "protocol_family": "imci_child",
            }
        }
    ]
    metrics = evaluate_records(gold, pred)
    assert metrics["valid_json_rate"] == 1.0
    assert metrics["action_match"] == 1.0

