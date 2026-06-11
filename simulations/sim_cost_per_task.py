"""SIMULATION 2 — BYOM cost-per-task across provider tiers.

THE QUESTION
    The architecture treats the model as a replaceable engine behind one
    knob (BYOM: bring-your-own-model). What does that engine choice cost
    per agent task, and what does a routed mix save versus pinning the
    whole fleet to one frontier model?

THE MODEL (pure arithmetic on stated assumptions — no randomness)
    Representative agent task = 6 turns.
      Turn input  = 12,000 tokens, of which 8,000 is a stable prefix
                    (system brief + memory) cacheable from turn 2 onward
                    at hit rate h = 0.85 where the provider discounts
                    cache reads.
      Turn output = 1,200 tokens.
    Cost(task) = sum over turns of in/out/cache-read token prices.

PRICE ANCHORS (USD per million tokens; all are published list prices)
    frontier      15.00 / 75.00 / 1.50   (in / out / cache-read)
    standard       3.00 / 15.00 / 0.30
    light          1.00 /  5.00 / 0.10
        The three Anthropic-class tiers above are the rates configured in
        the platform's own token meter (VERIFIED as configured rates).
    deepseek-v4-pro  0.435 / 0.87        (OpenRouter list price, 2026-06;
        modeled WITHOUT a cache-read discount — conservative for this
        tier. This is the engine the production 9-agent fleet actually
        moved to on 2026-06-11.)                              [VERIFIED]

ROUTED MIX
    70% of tasks -> light tier, 20% -> standard, 10% -> frontier:
    the routing share a cost-tiered fleet sends each class of work.
    Compared against "all-frontier" (every task on the frontier tier).

FLEET PROJECTION
    9 agents x 40 tasks/day x 30 days = 10,800 tasks/month
    (the production fleet is 9 agents; 40 tasks/agent/day is an
    ASSUMPTION held constant across engines so only price varies).

HONESTY LABEL
    VERIFIED arithmetic on stated assumptions. Prices are list prices on
    the stated date; cost figures are API-equivalent cost-to-serve, not
    necessarily cash (subscription seats change the cash picture).
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # portable/embeddable Python lacks script-dir on sys.path


import csv
import json
import os

import _svg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# (in, out, cache_read) USD per 1M tokens; cache_read=None -> no discount modeled
TIERS = {
    "frontier": (15.00, 75.00, 1.50),
    "standard": (3.00, 15.00, 0.30),
    "light": (1.00, 5.00, 0.10),
    "deepseek-v4-pro": (0.435, 0.87, None),
}

TURNS = 6
IN_TOK = 12_000
PREFIX = 8_000
OUT_TOK = 1_200
HIT = 0.85
TASKS_MONTH = 9 * 40 * 30


def task_cost(p_in, p_out, p_cache):
    cost = 0.0
    for turn in range(TURNS):
        fresh, cached = IN_TOK, 0
        if turn > 0 and p_cache is not None:
            cached = PREFIX * HIT
            fresh = IN_TOK - cached
        cost += fresh / 1e6 * p_in + cached / 1e6 * (p_cache or 0.0) + OUT_TOK / 1e6 * p_out
    return cost


def main():
    os.makedirs(OUT, exist_ok=True)
    per_task = {name: task_cost(*p) for name, p in TIERS.items()}

    routed = 0.70 * per_task["light"] + 0.20 * per_task["standard"] + 0.10 * per_task["frontier"]
    routed_byom = 0.70 * per_task["deepseek-v4-pro"] + 0.20 * per_task["standard"] + 0.10 * per_task["frontier"]

    table = {name: round(c, 4) for name, c in per_task.items()}
    table["routed-mix (70/20/10)"] = round(routed, 4)
    table["routed-mix BYOM floor"] = round(routed_byom, 4)

    monthly = {name: round(c * TASKS_MONTH, 2) for name, c in {**per_task, "routed-mix (70/20/10)": routed, "routed-mix BYOM floor": routed_byom}.items()}

    ratios = {
        "frontier_vs_deepseek_per_task": round(per_task["frontier"] / per_task["deepseek-v4-pro"], 1),
        "frontier_vs_routed": round(per_task["frontier"] / routed, 1),
        "frontier_vs_routed_byom": round(per_task["frontier"] / routed_byom, 1),
        "list_price_ratio_in": round(TIERS["frontier"][0] / TIERS["deepseek-v4-pro"][0], 1),
        "list_price_ratio_out": round(TIERS["frontier"][1] / TIERS["deepseek-v4-pro"][1], 1),
    }

    with open(os.path.join(OUT, "cost_per_task.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["engine", "usd_per_task", "usd_per_month_10800_tasks"])
        for name in table:
            w.writerow([name, table[name], monthly[name]])

    with open(os.path.join(OUT, "cost_per_task.json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "label": "VERIFIED arithmetic on stated assumptions",
                "task_shape": {"turns": TURNS, "input_tokens": IN_TOK, "stable_prefix": PREFIX, "output_tokens": OUT_TOK, "cache_hit": HIT},
                "prices_usd_per_M": {k: list(v) for k, v in TIERS.items()},
                "usd_per_task": table,
                "usd_per_month": monthly,
                "ratios": ratios,
            },
            f,
            indent=2,
        )

    names = list(table.keys())
    _svg.bar_chart(
        os.path.join(OUT, "cost_per_task.svg"),
        "Cost per agent task by engine (BYOM knob)",
        f"Representative task: {TURNS} turns x {IN_TOK:,} in / {OUT_TOK:,} out tokens, {PREFIX:,}-token stable prefix, cache hit {HIT:.0%} where discounted.",
        "VERIFIED arithmetic on published list prices (2026-06). API-equivalent cost-to-serve, not cash. Apex Prime assessment.",
        "Engine / routing policy",
        "USD per task",
        names,
        [("USD per task", [table[n] for n in names])],
        yfmt=lambda v: f"${v:.2f}",
    )

    out = {"usd_per_task": table, "usd_per_month": monthly, "ratios": ratios}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
