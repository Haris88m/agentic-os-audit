"""SIMULATION 5 — The autonomy dial: unsafe pass-through vs. operator load.

THE QUESTION
    The architecture's central safety device is a mechanical human-gate
    layer: an autonomy dial (L0-L5) crossed with a per-action risk score,
    with one hard floor — EVEN AT MAXIMUM AUTONOMY, a high-risk action
    still queues for a human. What does that floor buy, in numbers?

EVIDENCE ANCHOR (the category's measured weakness)
    Academic measurement of the category's most popular incumbent found
    baseline sandbox-escape defense averaging ~17%; adding a staged
    human-in-the-loop defense layer raised measured defense to 19-92%
    depending on the reviewing model (~91.5% at the strongest).
    [VERIFIED events/figures from the published study; the exact
    percentages are that study's, not re-measured here.]
    The incumbent's documented failures (a CVSS 8.8 one-click RCE, a
    1.5M-token credential breach, a "shadow superuser" demonstration)
    are why the gate question is THE category question.

THE MODEL (closed-form expectation, plus a seeded action stream)
    Action stream: 1,000 actions/week, of which 2% are HIGH-RISK
    (irreversible, outward-facing, or credential-touching) and 8% are
    MEDIUM-RISK. 52 weeks.
    Autonomy dial L0-L5 -> fraction of actions auto-executed without a
    human gate, rising with the dial level:
        gate_coverage(L) for (low, med, high) risk classes:
          L0: gate everything            (1.00, 1.00, 1.00)
          L1: (0.50, 1.00, 1.00)
          L2: (0.20, 0.80, 1.00)
          L3: (0.05, 0.50, 1.00)
          L4: (0.01, 0.20, 1.00)
          L5: (0.00, 0.05, 1.00)   <- the hard floor: high risk ALWAYS gated
        and a contrast architecture "L5-no-floor" = (0.00, 0.05, 0.00):
        the same dial WITHOUT the high-risk floor.
    Unsafe pass-through: a gated action is caught by the human reviewer
    with probability 0.915 (the anchored strongest-reviewer figure); an
    ungated unsafe action passes through unchallenged. P(an unscreened
    high-risk action is actually harmful) = 0.25; medium = 0.05.
    Operator load = expected gated actions routed to the human per week.

HONESTY LABEL
    SIMULATED — the dial mapping and harm priors are stated model
    assumptions; the reviewer-effectiveness and baseline figures are
    anchored to the published category study. The result quantifies a
    trade-off curve; it is not a penetration test.
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # portable/embeddable Python lacks script-dir on sys.path


import csv
import json
import os

import _svg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

ACTIONS_WEEK = 1000.0
SHARES = {"low": 0.90, "med": 0.08, "high": 0.02}
P_HARM = {"low": 0.001, "med": 0.05, "high": 0.25}
REVIEW_CATCH = 0.915

DIAL = {
    "L0": (1.00, 1.00, 1.00),
    "L1": (0.50, 1.00, 1.00),
    "L2": (0.20, 0.80, 1.00),
    "L3": (0.05, 0.50, 1.00),
    "L4": (0.01, 0.20, 1.00),
    "L5": (0.00, 0.05, 1.00),
    "L5-no-floor": (0.00, 0.05, 0.00),
}


def level_stats(cov):
    cov_map = dict(zip(("low", "med", "high"), cov))
    gated = sum(ACTIONS_WEEK * SHARES[c] * cov_map[c] for c in SHARES)
    unsafe_week = 0.0
    for c in SHARES:
        n = ACTIONS_WEEK * SHARES[c]
        harmful = n * P_HARM[c]
        g = cov_map[c]
        unsafe_week += harmful * (g * (1 - REVIEW_CATCH) + (1 - g))
    return gated, unsafe_week * 52.0


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = {}
    for name, cov in DIAL.items():
        gated, unsafe_year = level_stats(cov)
        rows[name] = {"gated_actions_per_week": round(gated, 1), "expected_unsafe_passthrough_per_year": round(unsafe_year, 1)}

    floor_value = rows["L5-no-floor"]["expected_unsafe_passthrough_per_year"] - rows["L5"]["expected_unsafe_passthrough_per_year"]
    headline = {
        "unsafe_per_year_L0": rows["L0"]["expected_unsafe_passthrough_per_year"],
        "unsafe_per_year_L5_with_floor": rows["L5"]["expected_unsafe_passthrough_per_year"],
        "unsafe_per_year_L5_no_floor": rows["L5-no-floor"]["expected_unsafe_passthrough_per_year"],
        "high_risk_floor_prevents_per_year": round(floor_value, 1),
        "operator_load_L5_per_week": rows["L5"]["gated_actions_per_week"],
        "operator_load_L0_per_week": rows["L0"]["gated_actions_per_week"],
    }

    with open(os.path.join(OUT, "gate_safety.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dial_level", "gated_actions_per_week", "expected_unsafe_passthrough_per_year"])
        for name, r in rows.items():
            w.writerow([name, r["gated_actions_per_week"], r["expected_unsafe_passthrough_per_year"]])

    with open(os.path.join(OUT, "gate_safety.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "label": "SIMULATED (closed-form expectation on stated priors)",
                "anchors": {
                    "reviewer_catch_rate": REVIEW_CATCH,
                    "source": "published category study: ~17% baseline defense; 19-92% with staged human-in-the-loop review (strongest reviewer ~91.5%)",
                },
                "model": {"actions_per_week": ACTIONS_WEEK, "risk_shares": SHARES, "harm_priors": P_HARM, "dial": {k: list(v) for k, v in DIAL.items()}},
                "results": rows,
                "headline": headline,
            },
            f,
            indent=2,
        )

    cats = list(DIAL.keys())
    _svg.bar_chart(
        os.path.join(OUT, "gate_safety.svg"),
        "The autonomy dial: operator load vs. expected unsafe pass-through",
        "1,000 actions/week (2% high-risk), reviewer catch rate 91.5% (anchored). 'L5-no-floor' removes the design's always-gate-high-risk floor.",
        "SIMULATED - dial mapping and harm priors are stated assumptions; reviewer effectiveness anchored to the published category study. Apex Prime assessment.",
        "Autonomy dial level",
        "Per week (load) / per year (unsafe)",
        cats,
        [
            ("Gated actions per week (operator load)", [rows[c]["gated_actions_per_week"] for c in cats]),
            ("Expected unsafe pass-through per year", [rows[c]["expected_unsafe_passthrough_per_year"] for c in cats]),
        ],
        yfmt=lambda v: f"{v:,.0f}",
    )

    out = {"headline": headline, "results": rows}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
