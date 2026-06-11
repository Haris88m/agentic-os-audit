"""SIMULATION 3 — Provider-shock resilience: engine-knob vs. coupled architecture.

THE QUESTION
    Providers change terms: prices move, metering models change, access
    tiers get cut. When a shock lands, how much fleet capacity does each
    architecture lose before it is back at full strength?

THE REAL-WORLD ANCHOR (the reason this simulation exists)
    On 2026-06-11 — four days ahead of an announced provider billing
    change — the production 9-agent fleet behind this assessment moved
    its entire reasoning engine from a frontier-provider CLI to
    DeepSeek V4 Pro behind one environment knob. The swap was designed,
    implemented, sealed, and verified live (9/9 agents answering) the
    SAME DAY. That measured event sets the CONSUME architecture's
    swap-time distribution below. The coupled architecture's migration
    range is an industry assumption, swept across a wide band.

THE MODEL (seeded Monte Carlo, n = 10,000 trials)
    Horizon: 360 days. One shock lands at T ~ Uniform(0, 360).
    Shock type (assumed mix, stated openly):
        50%  price x2          (no downtime, cost doubles until migrated)
        30%  metering change   (capacity limited to 60% until migrated)
        20%  access cut        (capacity 0% until migrated)
    Migration time, triangular(min, mode, max) days:
        coupled architecture:  (14, 30, 60)   [ASSUMPTION — swept]
        CONSUME engine-knob:   (0.2, 1, 3)    [anchored to the measured
                                               same-day swap, 2026-06-11]
    Fleet: 9 agents x 40 tasks/day. We report tasks lost to the shock
    and the 360-day excess cost at the per-task prices of Simulation 2.

HONESTY LABEL
    SIMULATED — Monte Carlo on stated distributions. One input (the
    CONSUME swap time) is anchored to a real, dated, verified event; the
    coupled-architecture migration band is an assumption and the result
    table shows its sensitivity.
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
HORIZON = 360.0
TASKS_DAY = 9 * 40
COST_PER_TASK = 0.2167  # routed-mix (70/20/10) USD/task, from Simulation 2 output

SHOCKS = [("price_x2", 0.50), ("metering_60pct", 0.30), ("access_cut", 0.20)]

ARCHS = {
    "coupled (14-60d migration)": (14.0, 30.0, 60.0),
    "CONSUME engine-knob (same-day, measured)": (0.2, 1.0, 3.0),
}

SENSITIVITY = {"coupled-fast (7-21d)": (7.0, 14.0, 21.0), "coupled-slow (30-90d)": (30.0, 60.0, 90.0)}


def one_trial(rng, tri):
    t_shock = rng.uniform(0, HORIZON)
    r = rng.random()
    acc, kind = 0.0, None
    for name, p in SHOCKS:
        acc += p
        if r <= acc:
            kind = name
            break
    mig = min(rng.triangular(*tri), HORIZON - t_shock)
    if kind == "price_x2":
        lost_tasks = 0.0
        excess_cost = mig * TASKS_DAY * COST_PER_TASK  # the doubled half
    elif kind == "metering_60pct":
        lost_tasks = mig * TASKS_DAY * 0.40
        excess_cost = 0.0
    else:  # access_cut
        lost_tasks = mig * TASKS_DAY * 1.00
        excess_cost = 0.0
    return lost_tasks, excess_cost, mig


def run(tri, seed_offset=0):
    rng = random.Random(SEED + seed_offset)
    lt, ec, mg = [], [], []
    for _ in range(N):
        a, b, c = one_trial(rng, tri)
        lt.append(a)
        ec.append(b)
        mg.append(c)
    lt.sort()
    return {
        "mean_lost_tasks": round(sum(lt) / N, 1),
        "p50_lost_tasks": round(lt[N // 2], 1),
        "p95_lost_tasks": round(lt[int(N * 0.95)], 1),
        "mean_excess_cost_usd": round(sum(ec) / N, 2),
        "mean_days_degraded": round(sum(mg) / N, 2),
        "_sorted_lost": lt,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    results = {}
    for i, (name, tri) in enumerate({**ARCHS, **SENSITIVITY}.items()):
        results[name] = run(tri, seed_offset=i)

    coupled = results["coupled (14-60d migration)"]
    knob = results["CONSUME engine-knob (same-day, measured)"]
    headline = {
        "mean_lost_tasks_ratio": round(coupled["mean_lost_tasks"] / max(1e-9, knob["mean_lost_tasks"]), 1),
        "mean_days_degraded_coupled": coupled["mean_days_degraded"],
        "mean_days_degraded_knob": knob["mean_days_degraded"],
    }

    with open(os.path.join(OUT, "provider_shock.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["architecture", "mean_lost_tasks", "p50_lost_tasks", "p95_lost_tasks", "mean_excess_cost_usd", "mean_days_degraded"])
        for name, r in results.items():
            w.writerow([name, r["mean_lost_tasks"], r["p50_lost_tasks"], r["p95_lost_tasks"], r["mean_excess_cost_usd"], r["mean_days_degraded"]])

    with open(os.path.join(OUT, "provider_shock.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "label": "SIMULATED (Monte Carlo, seeded)",
                "seed": SEED,
                "trials": N,
                "anchor": "CONSUME swap time anchored to the measured 2026-06-11 same-day 9-agent engine swap (verified live 9/9).",
                "results": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in results.items()},
                "headline": headline,
            },
            f,
            indent=2,
        )

    # Exceedance curve: P(lost tasks > x) for the two primary architectures
    series = []
    for name in ARCHS:
        lt = results[name]["_sorted_lost"]
        pts = []
        for q in range(0, 101, 2):
            idx = min(N - 1, int(q / 100 * (N - 1)))
            pts.append((lt[idx], 1.0 - q / 100))
        series.append((name, pts))
    _svg.line_chart(
        os.path.join(OUT, "provider_shock.svg"),
        "Provider shock: probability of losing more than X fleet tasks",
        f"{N:,} seeded trials, 360-day horizon, one shock (50% price x2 / 30% metering / 20% access cut), 9-agent fleet at 360 tasks/day.",
        "SIMULATED - CONSUME swap-time anchored to the measured 2026-06-11 same-day engine swap; coupled migration band is a stated assumption. Apex Prime assessment.",
        "Fleet tasks lost to the shock",
        "P(loss exceeds X)",
        series,
        xfmt=lambda v: f"{v:,.0f}",
        yfmt=lambda v: f"{v:.0%}",
    )

    out = {"headline": headline, "results": {k: {kk: vv for kk, vv in v.items() if not kk.startswith('_')} for k, v in results.items()}}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
