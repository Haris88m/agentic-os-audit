"""Measure the real system: walk the operator's live substrate and emit counts.

This is the measurement script behind assessment/06-the-real-system.md.
It runs on the operator's machine (the substrate is private infrastructure;
the published artifact is the dated snapshot JSON it emits, checked in at
data/real_system_metrics.json). Counts only - no file contents, no paths,
no credentials are written to the snapshot.

Usage: python extract_real_metrics.py --root <substrate-root> [--ledger <token-ledger.json>]
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
from datetime import datetime, timezone


def count(pattern, root):
    return len(glob.glob(os.path.join(root, pattern), recursive=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="substrate root (the platform project directory)")
    ap.add_argument("--ledger", default=None, help="token-ledger.json path (optional)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_system_metrics.json"))
    a = ap.parse_args()
    root = a.root

    skills_root = os.path.join(root, ".claude", "skills")
    skill_dirs = [d for d in glob.glob(os.path.join(skills_root, "*")) if os.path.isdir(d) and not os.path.basename(d).startswith("_")]
    skills = [d for d in skill_dirs if os.path.exists(os.path.join(d, "SKILL.md"))]

    cascade_entries = glob.glob(os.path.join(skills_root, "cascade-log", "entries", "*.md"))
    cascade_ids = []
    for p in cascade_entries:
        m = re.match(r"(\d+)", os.path.basename(p))
        if m:
            cascade_ids.append(int(m.group(1)))

    snapshot = {
        "label": "MEASURED - live walk of the operator's substrate; counts only",
        "measured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "capability_modules_skills": len(skills),
        "build_verify_iterations_cascade_entries": len(cascade_entries),
        "highest_iteration_id": max(cascade_ids) if cascade_ids else None,
        "failure_vaccinations": count(os.path.join(".claude", "skills", "**", "_vaccinations", "*.md"), root),
        "learning_records": count(os.path.join(".claude", "skills", "**", "_learnings", "*.md"), root),
        "finding_reports": count(os.path.join(".claude", "skills", "**", "_findings", "*.md"), root),
        "consumed_vendor_packages": len(glob.glob(os.path.join(skills_root, "**", "_absorbed", "*"), recursive=False))
        or len({p for p in glob.glob(os.path.join(skills_root, "*", "_absorbed", "*")) if os.path.isdir(p)}),
        "session_logs": count(os.path.join(".claude", "skills", "session-log", "sessions", "S*.md"), root),
        "memory_files": count(os.path.join(".claude", "memory", "**", "*.md"), root),
        "named_agents": count(os.path.join(".claude", "agents", "*.md"), root),
    }

    if a.ledger and os.path.exists(a.ledger):
        led = json.load(open(a.ledger, encoding="utf-8"))
        t = led["totals"]
        total = t["in"] + t["out"] + t["cache_write"] + t["cache_read"]
        snapshot["token_ledger"] = {
            "window": f"19 recorded build days ending {led['generated_at'][:10]}",
            "total_tokens": total,
            "total_tokens_billions": round(total / 1e9, 3),
            "input_tokens": t["in"],
            "output_tokens": t["out"],
            "cache_write_tokens": t["cache_write"],
            "cache_read_tokens": t["cache_read"],
            "cache_read_share_pct": round(100 * t["cache_read"] / total, 1),
            "messages": t["messages"],
            "transcript_files": led["transcript_files"],
            "distinct_sessions": len(led["by_session"]),
            "api_equivalent_cost_usd": round(t["cost_usd"], 2),
            "note": "API-equivalent cost-to-serve at configured list rates; NOT cash (subscription).",
        }

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
