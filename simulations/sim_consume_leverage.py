"""SIMULATION 4 — Consumption leverage: consume-and-own vs. build-from-scratch.

THE QUESTION
    The CONSUME intake gate only admits a pattern when its value-to-
    integration-overhead ratio is at least 3x. Does the documented
    consumption record actually deliver that leverage, and what does a
    year of it compound to?

EVIDENCE ANCHOR (the public consumption ledger)
    ~8 consumption families -> ~12 owned capability modules in the
    recorded window, each re-implemented in the platform's own stack
    and passed through a real test before admission. Documented families
    include: a context-discipline/sandboxed-execute family (one open
    engine -> four owned capabilities), a read-before-edit safety
    invariant, symbol-aware editing, a 7-class post-edit failure
    classifier, trajectory evaluation, permission-gating/phase-locking,
    exploratory-QA and email-handling patterns, and multi-provider
    routing + a model-hub adapter.                          [VERIFIED]

THE MODEL (seeded Monte Carlo, n = 10,000 trials)
    Effort to OWN one capability, triangular(min, mode, max) eng-hours:
        build-from-scratch:  (24, 40, 80)    [ASSUMPTION — swept]
        consume-and-own:     (6, 12, 24) + 2h fixed intake-gate cost
            (pattern extraction + owned re-implementation + real test;
             the gate cost covers license check, value/overhead check,
             framework-conflict check, drift check)
    Leverage = scratch_hours / consume_hours per capability.
    12-month projection: at a fixed verification budget of 30 eng-hours
    per month, how many owned capabilities does each strategy validate?

HONESTY LABEL
    SIMULATED — effort bands are stated assumptions; the consumption
    record and the >=3x admission gate are real and public. The model's
    mean leverage landing near the gate's own admission threshold is a
    consistency check, not a coincidence: the gate REJECTS candidates
    below 3x, so admitted work should cluster at or above it.
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # portable/embeddable Python lacks script-dir on sys.path


import csv
import json
import os
import random

import _svg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
SEED = 20260611
N = 10_000

SCRATCH = (24.0, 40.0, 80.0)
CONSUME = (6.0, 12.0, 24.0)
GATE_COST = 2.0
BUDGET_HOURS_MONTH = 30.0
MONTHS = 12


def main():
    os.makedirs(OUT, exist_ok=True)
    rng = random.Random(SEED)
    lev, sc_h, co_h = [], [], []
    for _ in range(N):
        s = rng.triangular(*SCRATCH)
        c = rng.triangular(*CONSUME) + GATE_COST
        sc_h.append(s)
        co_h.append(c)
        lev.append(s / c)
    lev.sort()
    stats = {
        "mean_leverage": round(sum(lev) / N, 2),
        "p25_leverage": round(lev[N // 4], 2),
        "p50_leverage": round(lev[N // 2], 2),
        "p75_leverage": round(lev[3 * N // 4], 2),
        "share_above_3x_gate": round(sum(1 for x in lev if x >= 3.0) / N, 3),
        "mean_scratch_hours": round(sum(sc_h) / N, 1),
        "mean_consume_hours": round(sum(co_h) / N, 1),
    }

    # 12-month projection at fixed verification budget
    proj = []
    cum_s = cum_c = 0.0
    for m in range(1, MONTHS + 1):
        cum_s += BUDGET_HOURS_MONTH / stats["mean_scratch_hours"]
        cum_c += BUDGET_HOURS_MONTH / stats["mean_consume_hours"]
        proj.append((m, cum_s, cum_c))
    projection = {
        "budget_hours_per_month": BUDGET_HOURS_MONTH,
        "capabilities_12mo_scratch": round(proj[-1][1], 1),
        "capabilities_12mo_consume": round(proj[-1][2], 1),
    }

    with open(os.path.join(OUT, "consume_leverage.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month", "cum_capabilities_scratch", "cum_capabilities_consume"])
        for m, s, c in proj:
            w.writerow([m, round(s, 2), round(c, 2)])

    with open(os.path.join(OUT, "consume_leverage.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "label": "SIMULATED (Monte Carlo, seeded)",
                "seed": SEED,
                "trials": N,
                "effort_bands_hours": {"scratch": SCRATCH, "consume": CONSUME, "gate_fixed": GATE_COST},
                "stats": stats,
                "projection": projection,
                "evidence_anchor": "~8 consumption families -> ~12 owned modules in the public consumption ledger; >=3x value/overhead admission gate.",
            },
            f,
            indent=2,
        )

    _svg.line_chart(
        os.path.join(OUT, "consume_leverage.svg"),
        "Owned capabilities per year at a fixed 30 eng-hour/month verification budget",
        f"Monte Carlo mean effort: build-from-scratch {stats['mean_scratch_hours']}h vs. consume-and-own {stats['mean_consume_hours']}h per capability "
        f"(mean leverage {stats['mean_leverage']}x).",
        "SIMULATED - effort bands are stated assumptions; the consumption ledger and the >=3x intake gate are public. Apex Prime assessment, 2026-06.",
        "Month",
        "Cumulative owned, validated capabilities",
        [
            ("Build-from-scratch", [(m, s) for m, s, _ in proj]),
            ("CONSUME (gated consumption)", [(m, c) for m, _, c in proj]),
        ],
    )

    out = {"stats": stats, "projection": projection}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
