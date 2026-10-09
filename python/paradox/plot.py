"""An SVG line chart of v_O/u against the mass ratio, written by hand.

SVG is just text (XML), so a chart is a few <line>, <polyline> and <text>
elements. No plotting library is needed. The x axis is log10(r), because the
interesting range spans from r = 1/1000 to r = 1000.
"""

from __future__ import annotations

from fractions import Fraction
from html import escape

from .collision import object_speed_ratio

W, H, PAD = 640, 360, 56


def chart(es: tuple[Fraction, ...] = (Fraction(1), Fraction(1, 2), Fraction(0)), lo: int = -3, hi: int = 3) -> str:
    def x(log_r: float) -> float:
        return PAD + (log_r - lo) / (hi - lo) * (W - 2 * PAD)

    def y(v: float) -> float:
        return H - PAD - v / 2 * (H - 2 * PAD)  # v from 0 to 2 (the most is 1 + e = 2)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="sans-serif" font-size="12">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<line x1="{PAD}" y1="{H - PAD}" x2="{W - PAD}" y2="{H - PAD}" stroke="black"/>',
             f'<line x1="{PAD}" y1="{PAD}" x2="{PAD}" y2="{H - PAD}" stroke="black"/>']
    for k in range(lo, hi + 1):
        parts.append(f'<text x="{x(k):.1f}" y="{H - PAD + 18}" text-anchor="middle">10^{k}</text>')
    for v in (0, 0.5, 1, 1.5, 2):
        parts.append(f'<text x="{PAD - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    colors = ("#c0392b", "#2471a3", "#1e8449")
    steps = 120
    for e, color in zip(es, colors, strict=False):
        pts = []
        for i in range(steps + 1):
            log_r = lo + (hi - lo) * i / steps
            v = float(object_speed_ratio(Fraction(10 ** log_r), e))  # a chart only needs floats
            pts.append(f"{x(log_r):.1f},{y(v):.1f}")
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{" ".join(pts)}"/>')
        parts.append(f'<text x="{W - PAD + 4}" y="{y(float(1 + e)) + 4:.1f}" fill="{color}">e = {escape(str(e))}</text>')
    parts.append(f'<text x="{W / 2}" y="{H - 12}" text-anchor="middle">mass ratio r = m / M (both masses → ∞)</text>')
    parts.append(f'<text x="16" y="{H / 2}" transform="rotate(-90 16 {H / 2})" text-anchor="middle">'
                 "object speed after the hit, v_O / u</text>")
    parts.append(f'<text x="{W / 2}" y="24" text-anchor="middle" font-size="14">'
                 "Same 'infinite' masses, any answer: it depends on the ratio</text>")
    parts.append("</svg>")
    return "\n".join(parts)
