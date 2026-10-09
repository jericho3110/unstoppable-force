"""Approaching infinity in different ways.

"Unstoppable" means m -> infinity. "Immovable" means M -> infinity. Both at
once is a DOUBLE limit, and a double limit only exists if every way of
getting there gives the same answer. Here they don't:

- Along any path m = r * M (both grow, ratio fixed), v_O/u stays exactly
  (1+e)*r/(1+r). Choose r and you can get any value between 0 and 1+e.
- The two ITERATED limits disagree too:
      lim_{M->inf} lim_{m->inf} v_O/u = 1 + e   (make F unstoppable first: O flies off)
      lim_{m->inf} lim_{M->inf} v_O/u = 0       (make O immovable first: it stays put)

So "what happens" has no answer. The question hides a choice of path, and the
answer depends on the choice.
"""

from __future__ import annotations

from collections.abc import Iterator
from fractions import Fraction

from .collision import collide, object_speed_ratio


def along_ratio(r: int | Fraction, e: int | Fraction = 1, powers: range = range(0, 301, 50)) \
        -> Iterator[tuple[int, Fraction]]:
    """(k, v_O/u) for M = 10**k and m = r * M. Exact, however big k is."""
    for k in powers:
        M = Fraction(10) ** k
        yield k, collide(r * M, M, 1, e).v_object


def iterated(e: int | Fraction = 1, big: int = 10**60) -> tuple[Fraction, Fraction]:
    """Approximate both iterated limits with one mass 'infinite' (huge) relative to the other.

    The inner limit is taken first: the inner variable is made `big`**2 times
    larger than the outer one, which is itself `big`.
    """
    force_first = collide(big * big * big, big, 1, e).v_object   # m >> M: the unstoppable side wins
    object_first = collide(big, big * big * big, 1, e).v_object  # M >> m: the immovable side wins
    return force_first, object_first


def path_table(ratios: list[Fraction], e: int | Fraction = 1) -> list[tuple[Fraction, Fraction]]:
    """(r, exact v_O/u) for each ratio: the whole 'answer space' of the paradox."""
    return [(Fraction(r), object_speed_ratio(r, e)) for r in ratios]
