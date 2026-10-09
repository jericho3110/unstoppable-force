"""`python main.py math <command>`: the exact-math side of the project."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

from .collision import object_speed_ratio
from .limits import along_ratio, iterated, path_table
from .plot import chart
from .proof import find_contradiction

RATIOS = [Fraction(1, 1000), Fraction(1, 10), Fraction(1, 2), Fraction(1), Fraction(2), Fraction(10), Fraction(1000)]


def show(x: Fraction) -> str:
    """Exact when short, a decimal when long."""
    text = str(x)
    return text if len(text) <= 12 else f"{float(x):.6f}"


def cmd_paths(e: Fraction) -> None:
    print(f"Both masses -> infinity with a fixed ratio r = m/M (restitution e = {e}):")
    print(f"{'r = m/M':>10}  {'object speed v_O/u':>20}  meaning")
    for r, v in path_table(RATIOS, e):
        meaning = "object barely moves" if v < Fraction(1, 10) else "object flies off" if v > 1 else "both move"
        print(f"{show(r):>10}  {show(v):>20}  {meaning}")
    print("\nThe same ratio at ever larger masses gives the SAME answer (exact, no rounding):")
    for k, v in along_ratio(Fraction(1), e, range(0, 301, 100)):
        print(f"  m = M = 10^{k:<3}  v_O/u = {show(v)}")


def cmd_iterated(e: Fraction) -> None:
    force_first, object_first = iterated(e)
    print("Iterated limits (which 'infinity' you take first):")
    print(f"  unstoppable first (m >> M):  v_O/u -> {float(force_first):.6f}   (= 1 + e = {float(1 + e)})")
    print(f"  immovable first   (M >> m):  v_O/u -> {float(object_first):.6e}   (-> 0)")
    print("  Different answers: the double limit does not exist.")


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="math", description="Exact math of the unstoppable-force paradox.")
    p.add_argument("--e", type=Fraction, default=Fraction(1), help="restitution 0..1 (default 1: elastic)")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("paths", help="v_O/u along different routes to infinity")
    sub.add_parser("iterated", help="the two iterated limits")
    sub.add_parser("proof", help="why both objects can't exist together")
    pl = sub.add_parser("plot", help="write an SVG chart")
    pl.add_argument("out", type=Path)
    args = p.parse_args(argv)
    if not 0 <= args.e <= 1:
        p.error("--e must be between 0 and 1")
    if args.command == "paths":
        cmd_paths(args.e)
    elif args.command == "iterated":
        cmd_iterated(args.e)
    elif args.command == "proof":
        print(find_contradiction())
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(chart(), encoding="utf-8")
        print(f"wrote {args.out}  (r = 1 gives v_O/u = {object_speed_ratio(1, args.e)})")
    return 0
