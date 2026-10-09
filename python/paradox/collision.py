"""A head-on collision in one dimension, solved exactly.

The "force" F (mass m) flies at speed u into the "object" O (mass M), which
is at rest. Two laws fix the outcome:

1. Momentum is conserved:       m*u = m*v_F + M*v_O
2. Restitution e (0..1) sets how bouncy the hit is:
                                v_O - v_F = e * u
   (e = 1: perfectly elastic, no energy lost; e = 0: they stick together.)

Solving the two equations for the two unknowns gives

    v_F = (m - e*M) * u / (m + M)
    v_O = (1 + e) * m * u / (m + M)

Every function takes and returns `Fraction`s (exact rational numbers), so a
mass of 10**300 is no problem and nothing is ever rounded.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

Number = int | Fraction


@dataclass(frozen=True)
class Outcome:
    v_force: Fraction    # the force's velocity after the hit
    v_object: Fraction   # the object's velocity after the hit
    impulse: Fraction    # momentum handed from F to O: J = M * v_O
    energy_lost: Fraction


def collide(m: Number, M: Number, u: Number, e: Number = 1) -> Outcome:
    m, M, u, e = Fraction(m), Fraction(M), Fraction(u), Fraction(e)
    if m <= 0 or M <= 0:
        raise ValueError("masses must be positive")
    if not 0 <= e <= 1:
        raise ValueError("restitution e must be between 0 and 1")
    v_f = (m - e * M) * u / (m + M)
    v_o = (1 + e) * m * u / (m + M)
    before = m * u * u / 2
    after = (m * v_f * v_f + M * v_o * v_o) / 2
    return Outcome(v_f, v_o, M * v_o, before - after)


def object_speed_ratio(r: Number, e: Number = 1) -> Fraction:
    """v_O / u written with only the mass RATIO r = m / M.

    Divide the top and bottom of (1+e)*m/(m+M) by M:  (1+e) * r / (1 + r).
    The individual masses have disappeared: only their ratio matters.
    """
    r, e = Fraction(r), Fraction(e)
    return (1 + e) * r / (1 + r)
