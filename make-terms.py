#!/usr/bin/env python3
"""Write terms.json for the BTX Explainer bounty from live inputs.

    make-terms.py --tip 246553 --council keys.json [--target-btx 5] [--held-out held-out.json] [--out terms.json]

keys.json: [{"name": "Mende (easyBTX)", "public_key_hex": "..."}, ...]  (2 to 8
members; 0.34.15 wallets refuse a one-key council). The evaluation spec id is
the SHA-384 of bounty/evaluation-spec.md; the held-out questions' SHA-384 goes
into the description so the set is fixed before anyone submits. Heights follow
the plan: about 960 blocks a day.
"""
import argparse
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DAY = 960


def sha384(path):
    return hashlib.sha384(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tip", type=int, required=True, help="current mainnet height")
    ap.add_argument("--council", required=True, help="keys.json")
    ap.add_argument("--target-btx", type=float, default=5.0)
    ap.add_argument("--threshold", type=int, default=1, help="1: any member can award (0.34.15 wallets cannot combine signatures)")
    ap.add_argument("--held-out", default="", help="the held-out questions file, hashed into the description")
    ap.add_argument("--network-id", default="0" * 64, help="mainnet network id as the helper reports it")
    ap.add_argument("--requester", default="", help="the publishing helper's research identity (96 hex) or empty")
    ap.add_argument("--out", default=os.path.join(HERE, "terms.json"))
    a = ap.parse_args()
    council = json.load(open(a.council))
    if not 2 <= len(council) <= 8:
        raise SystemExit("council needs 2 to 8 members")
    spec_id = sha384(os.path.join(HERE, "evaluation-spec.md"))
    held = sha384(a.held_out) if a.held_out else "(to be set)"
    names = ", ".join(m["name"] for m in council)
    t = a.tip
    terms = {
        "terms_version": 1,
        "network_id": a.network_id,
        "requester_identity": a.requester,
        "title": "BTX Explainer: an open model that knows BTX and its model network",
        # The helper caps the description at 1,024 characters; the long form is evaluation-spec.md.
        "description": (
            "Creation bounty 1 on BTX's model plane, by easyBTX. Deliver one open-weight language model (one GGUF, "
            "at most 4,000,000,000 bytes, Apache-2.0 or MIT) that answers questions about BTX and its model network "
            "from the btx repository at v0.34.15 (README, HUMANS, modelnet docs, release notes 0.34.12-15) and the "
            "BTX Handbook, English second edition (easybtx.com/handbook). Test: 60 questions with required facts, "
            "20 published, 40 held out until submissions close, SHA-384 of the held-out file %s. Grader: "
            "lab/bounty/grade.py in github.com/MendeMatthias/ainode (llama.cpp, temperature 0, no system prompt). "
            "Pass 48 of 60; highest score wins, ties to the earlier commit. Council: %s, threshold %d. Prize %s BTX "
            "in one lot; unawarded, it refunds after the refund height. Spec: bounty/evaluation-spec.md."
        ) % (held, names, a.threshold, "%g" % a.target_btx),
        "tags": ["btx", "explainer", "small-model", "gguf", "first-bounty"],
        "deliverable_classes": ["BASE_MODEL"],
        "evaluation_spec_id": spec_id,
        "submission_mode": "PUBLIC",
        "payout_authority": "COUNCIL_MULTISIG",
        "council": [{"public_key_hex": m["public_key_hex"]} for m in council],
        "threshold": a.threshold,
        "nomination_min_bps": 0,
        "target_atoms": str(int(round(a.target_btx * 100_000_000))),
        "max_lots_per_round": 4,
        "funding_close_height": t + 7 * DAY,
        "submission_close_height": t + 28 * DAY,
        "evaluation_close_height": t + 35 * DAY,
        "earliest_award_height": t + 36 * DAY,
        "last_safe_award_height": t + 42 * DAY,
        "refund_height": t + 49 * DAY,
        "minimum_confirmations": 6,
        "claim_margin_blocks": 20,
        "challenge_policy": "BOUNDED_TYPED",
        "selection_rule": "EXACT_CANDIDATE",
        "license_statement": "Apache-2.0 or MIT",
        "max_model_bytes": 4_000_000_000,
        "fee_policy": "USER_CEILING",
        "sealed_confidentiality_disclosure": "",
    }
    if len(terms["description"]) > 1024:
        raise SystemExit("description is %d characters; the helper allows 1024" % len(terms["description"]))
    json.dump(terms, open(a.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("description %d characters" % len(terms["description"]))
    print("wrote", a.out)
    print("evaluation_spec_id", spec_id)
    print("heights: funding close %d, submissions close %d, award %d..%d, refund %d" % (
        terms["funding_close_height"], terms["submission_close_height"], terms["earliest_award_height"],
        terms["last_safe_award_height"], terms["refund_height"]))


if __name__ == "__main__":
    main()
