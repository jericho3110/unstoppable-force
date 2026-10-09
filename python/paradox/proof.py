"""Why an unstoppable force and an immovable object can't share a universe.

Definitions (in one dimension, F moving at speed u > 0 toward O at rest):
    immovable O:    after ANY collision, v_O = 0
    unstoppable F:  after ANY collision, v_F = u   (nothing slows it down)

Momentum must be conserved:   m*u = m*v_F + M*v_O
Put both definitions in:      m*u = m*u + M*0         (true, so far)

But two solid bodies can't pass through each other. After the hit, the one
behind can't be faster than the one in front:   v_F <= v_O
With the definitions:                            u <= 0
That contradicts u > 0. So the two definitions can't both hold: at most
one of the two objects can exist. This is a proof by contradiction.

`check_definitions` tests the definitions against a candidate outcome, and
`find_contradiction` searches the collision formulas for one.
"""

from __future__ import annotations

from fractions import Fraction

from .collision import collide


def check_definitions(u: Fraction, v_force: Fraction, v_object: Fraction) -> dict[str, bool]:
    return {
        "immovable (v_O = 0)": v_object == 0,
        "unstoppable (v_F = u)": v_force == u,
        "no passing through (v_F <= v_O)": v_force <= v_object,
    }


def find_contradiction(u: int = 1) -> str:
    """Try every restitution and mass ratio; no real collision satisfies all three rules."""
    for e in (Fraction(0), Fraction(1, 2), Fraction(1)):
        for m, M in ((1, 10**9), (10**9, 1), (10**9, 10**9)):
            out = collide(m, M, u, e)
            rules = check_definitions(Fraction(u), out.v_force, out.v_object)
            if all(rules.values()):
                return f"counter-example found: m={m}, M={M}, e={e}"
    return ("no collision satisfies 'immovable', 'unstoppable' and 'no passing through' at once: "
            "the definitions contradict each other (u <= 0 would be needed, but u > 0)")
