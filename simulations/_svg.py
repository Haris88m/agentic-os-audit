"""Minimal stdlib SVG chart renderer for the simulation suite.

No third-party dependencies by design: every figure in this repository can be
regenerated on a clean Python 3.10+ install with `python run_all.py`.
Two chart shapes are provided — multi-series line charts and grouped bar
charts — with a deliberately plain, print-friendly style.
"""

from __future__ import annotations

PALETTE = ["#1f6feb", "#d97757", "#2da44e", "#8250df", "#cf222e", "#57606a"]
W, H = 920, 480
ML, MR, MT, MB = 70, 30, 64, 86  # margins: left, right, top, bottom


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _ticks(lo, hi, n=6):
    """Round-number axis ticks covering [lo, hi]."""
    if hi <= lo:
        hi = lo + 1.0
    span = hi - lo
    raw = span / max(1, n - 1)
    mag = 10 ** int(__import__("math").floor(__import__("math").log10(raw)))
    for mult in (1, 2, 2.5, 5, 10):
        step = mult * mag
        if span / step <= n:
            break
    start = step * int(lo / step)
    if start > lo:
        start -= step
    ticks, v = [], start
    while v <= hi + step * 0.5:
        ticks.append(round(v, 10))
        v += step
    return ticks


def _frame(title, subtitle, note):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{ML}" y="28" font-size="19" font-weight="600" fill="#1f2328">{_esc(title)}</text>',
        f'<text x="{ML}" y="48" font-size="13" fill="#57606a">{_esc(subtitle)}</text>',
        f'<text x="{ML}" y="{H - 14}" font-size="11" fill="#8b949e">{_esc(note)}</text>',
    ]
    return parts


def _axes(parts, xlo, xhi, ylo, yhi, xlabel, ylabel, xfmt, yfmt):
    pw, ph = W - ML - MR, H - MT - MB

    def X(x):
        return ML + (x - xlo) / (xhi - xlo) * pw

    def Y(y):
        return MT + ph - (y - ylo) / (yhi - ylo) * ph

    for t in _ticks(ylo, yhi):
        if ylo <= t <= yhi:
            y = Y(t)
            parts.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{W - MR}" y2="{y:.1f}" stroke="#eaeef2" stroke-width="1"/>')
            parts.append(f'<text x="{ML - 8}" y="{y + 4:.1f}" font-size="11" fill="#57606a" text-anchor="end">{yfmt(t)}</text>')
    for t in _ticks(xlo, xhi):
        if xlo <= t <= xhi:
            x = X(t)
            parts.append(f'<line x1="{x:.1f}" y1="{MT}" x2="{x:.1f}" y2="{H - MB}" stroke="#f6f8fa" stroke-width="1"/>')
            parts.append(f'<text x="{x:.1f}" y="{H - MB + 18}" font-size="11" fill="#57606a" text-anchor="middle">{xfmt(t)}</text>')
    parts.append(f'<line x1="{ML}" y1="{H - MB}" x2="{W - MR}" y2="{H - MB}" stroke="#57606a" stroke-width="1.2"/>')
    parts.append(f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{H - MB}" stroke="#57606a" stroke-width="1.2"/>')
    parts.append(f'<text x="{(ML + W - MR) / 2:.0f}" y="{H - MB + 40}" font-size="12" fill="#1f2328" text-anchor="middle">{_esc(xlabel)}</text>')
    parts.append(
        f'<text x="20" y="{(MT + H - MB) / 2:.0f}" font-size="12" fill="#1f2328" text-anchor="middle" '
        f'transform="rotate(-90 20 {(MT + H - MB) / 2:.0f})">{_esc(ylabel)}</text>'
    )
    return X, Y


def _legend(parts, names):
    x = ML
    y = H - MB + 58
    for i, name in enumerate(names):
        c = PALETTE[i % len(PALETTE)]
        parts.append(f'<rect x="{x}" y="{y - 9}" width="14" height="14" rx="3" fill="{c}"/>')
        parts.append(f'<text x="{x + 20}" y="{y + 3}" font-size="12" fill="#1f2328">{_esc(name)}</text>')
        x += 24 + 7.2 * len(name) + 26


def line_chart(path, title, subtitle, note, xlabel, ylabel, series, xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}"):
    """series: list of (name, [(x, y), ...])"""
    xs = [p[0] for _, pts in series for p in pts]
    ys = [p[1] for _, pts in series for p in pts]
    xlo, xhi = min(xs), max(xs)
    ylo, yhi = min(0.0, min(ys)), max(ys) * 1.06
    parts = _frame(title, subtitle, note)
    X, Y = _axes(parts, xlo, xhi, ylo, yhi, xlabel, ylabel, xfmt, yfmt)
    for i, (name, pts) in enumerate(series):
        c = PALETTE[i % len(PALETTE)]
        d = " ".join(f"{'M' if j == 0 else 'L'}{X(x):.1f},{Y(y):.1f}" for j, (x, y) in enumerate(pts))
        parts.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4"/>')
    _legend(parts, [n for n, _ in series])
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def bar_chart(path, title, subtitle, note, xlabel, ylabel, categories, series, yfmt=lambda v: f"{v:g}", log_hint=False):
    """categories: x labels; series: list of (name, [v per category])"""
    allv = [v for _, vs in series for v in vs]
    ylo, yhi = 0.0, max(allv) * 1.12
    parts = _frame(title, subtitle, note)
    pw, ph = W - ML - MR, H - MT - MB
    for t in _ticks(ylo, yhi):
        if ylo <= t <= yhi:
            y = MT + ph - (t - ylo) / (yhi - ylo) * ph
            parts.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{W - MR}" y2="{y:.1f}" stroke="#eaeef2"/>')
            parts.append(f'<text x="{ML - 8}" y="{y + 4:.1f}" font-size="11" fill="#57606a" text-anchor="end">{yfmt(t)}</text>')
    parts.append(f'<line x1="{ML}" y1="{H - MB}" x2="{W - MR}" y2="{H - MB}" stroke="#57606a" stroke-width="1.2"/>')
    parts.append(f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{H - MB}" stroke="#57606a" stroke-width="1.2"/>')
    ncat, nser = len(categories), len(series)
    slot = pw / ncat
    bw = min(46.0, slot * 0.72 / nser)
    for ci, cat in enumerate(categories):
        cx = ML + slot * (ci + 0.5)
        group_w = bw * nser
        for si, (name, vs) in enumerate(series):
            v = vs[ci]
            bh = (v - ylo) / (yhi - ylo) * ph
            x = cx - group_w / 2 + si * bw
            y = MT + ph - bh
            c = PALETTE[si % len(PALETTE)]
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw - 3:.1f}" height="{bh:.1f}" rx="3" fill="{c}"/>')
            parts.append(f'<text x="{x + (bw - 3) / 2:.1f}" y="{y - 5:.1f}" font-size="10.5" fill="#1f2328" text-anchor="middle">{yfmt(v)}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{H - MB + 18}" font-size="11.5" fill="#1f2328" text-anchor="middle">{_esc(cat)}</text>')
    parts.append(f'<text x="{(ML + W - MR) / 2:.0f}" y="{H - MB + 40}" font-size="12" fill="#1f2328" text-anchor="middle">{_esc(xlabel)}</text>')
    parts.append(
        f'<text x="20" y="{(MT + H - MB) / 2:.0f}" font-size="12" fill="#1f2328" text-anchor="middle" '
        f'transform="rotate(-90 20 {(MT + H - MB) / 2:.0f})">{_esc(ylabel)}</text>'
    )
    _legend(parts, [n for n, _ in series])
    parts.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
