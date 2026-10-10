# Math prerequisites: what to know before reading MATH.md

[MATH.md](MATH.md) explains the paradox itself. This guide covers the
**background** it assumes, from school algebra up to floating point. Each
section gives the idea, a small example from this project, where MATH.md
uses it, and a self-check question.

If a section feels easy, skip it. If one feels hard, try the linked
Further learning material before moving on.

## Contents

0. [How the ideas depend on each other](#0-how-the-ideas-depend-on-each-other)
1. [Algebra: variables and solving two equations](#1-algebra-variables-and-solving-two-equations)
2. [Fractions, ratios and cancelling](#2-fractions-ratios-and-cancelling)
3. [Signs and direction in one dimension](#3-signs-and-direction-in-one-dimension)
4. [Mass, velocity, momentum, force](#4-mass-velocity-momentum-force)
5. [Energy and restitution](#5-energy-and-restitution)
6. [Functions, graphs and asymptotes](#6-functions-graphs-and-asymptotes)
7. [Infinity and limits](#7-infinity-and-limits)
8. [Limits in two variables, and order of limits](#8-limits-in-two-variables-and-order-of-limits)
9. [Logic: definitions, "for all" and proof by contradiction](#9-logic-definitions-for-all-and-proof-by-contradiction)
10. [Powers, roots and scientific notation](#10-powers-roots-and-scientific-notation)
11. [Springs, oscillation and damping](#11-springs-oscillation-and-damping)
12. [Stepping through time: numerical integration](#12-stepping-through-time-numerical-integration)
13. [How computers store numbers](#13-how-computers-store-numbers)
14. [Self-test](#14-self-test)
15. [References](#references)

---

## 0. How the ideas depend on each other

```text
 algebra (1) ──► fractions & ratios (2) ──────────────► MATH §2–3  collision formulas
      │                                                      ▲
      ├──► signs & direction (3) ──► momentum & force (4) ───┤
      │                                    │                 │
      │                                    └► energy (5) ────┘
      │
      ├──► functions & graphs (6) ──► limits (7) ──► two-variable limits (8) ──► MATH §4–5
      │
      ├──► logic (9) ─────────────────────────────────────────────────────────► MATH §6
      │
      ├──► powers & roots (10) ──► springs (11) ──► time stepping (12) ───────► MATH §7  (Rust)
      │
      └──► scientific notation (10) ──► floating point (13) ──────────────────► MATH §8  (C++)
```

## 1. Algebra: variables and solving two equations

**Idea.** A *variable* is a name for a number you don't know yet. Two
unknowns need two equations. **Substitution** solves them: rearrange one
equation for one unknown, then put that into the other.

**Example.** Solve `x + y = 10` and `y − x = 4`.
The second gives `y = x + 4`. Substituting: `x + (x + 4) = 10`, so `x = 3` and `y = 7`.

**In this project.** MATH.md §2 does exactly this with the unknowns `v_F`
and `v_O` (the speeds after the hit). `python/paradox/collision.py` is the
result written as code.

**Self-check.** Why can't you find two unknowns from one equation?

## 2. Fractions, ratios and cancelling

**Idea.** Dividing the top and bottom of a fraction by the same nonzero
number doesn't change it: `6/8 = 3/4`. A **ratio** `r = m/M` compares two
quantities: it says "how many times bigger", not "how big".

**Example.** `2m/(m + M)`. Divide top and bottom by `M`:
`2(m/M) / (m/M + 1) = 2r/(r + 1)`. The individual masses are gone; only `r` is left.

**In this project.** MATH.md §3 ("only the ratio matters"). That's why
`m = M = 10^300` gives the same answer as `m = M = 1`. Python's `Fraction`
type (`fractions` module) keeps these exact, so `2/1001` stays `2/1001`
instead of `0.001998…`.

**Self-check.** If you triple both masses, what happens to `r`?

## 3. Signs and direction in one dimension

**Idea.** On a line, a velocity's **sign** is its direction. Here, positive
means "toward the object" and negative means "back the way it came". Speed
is the size, without the sign.

**Example.** A ball hits a wall at `+5 m/s` and bounces back at `−4 m/s`.
Its speed fell from 5 to 4, but its velocity *changed* by `−9 m/s`.

**In this project.** MATH.md §2: when `M` is huge, `v_F ≈ −e·u`. The minus
sign is the bounce.

**Self-check.** After a bounce, why is `v_F` negative while `v_O` is positive?

## 4. Mass, velocity, momentum, force

**Idea.**
- **Mass** `m`: how hard something is to speed up or slow down (inertia).
- **Momentum** `p = m·v`: "mass in motion".
- **Newton's second law**: force is the rate momentum changes, `F = m·a`.
- **Newton's third law**: when two bodies push on each other, the pushes
  are equal and opposite. So whatever momentum one loses, the other gains.
  **Total momentum is conserved.**

**Example.** A 2 kg ball at 3 m/s has momentum 6 kg·m/s. If it hits a still
1 kg ball and they stick, they move together at `6 / 3 = 2 m/s`.

**In this project.** MATH.md §2 (the first law in the box), and the Rust
simulator, which applies equal and opposite forces each step, so momentum is
kept to rounding error (a Rust test checks it).

**Self-check.** Why does "immovable" translate to "infinite mass"?

## 5. Energy and restitution

**Idea.** **Kinetic energy** is `½·m·v²`. Momentum is always conserved in a
collision, but energy may be lost to heat, sound or dents. The **coefficient
of restitution** `e` measures that: the speed they separate at divided by the
speed they approach at.

| `e` | name | energy |
| --- | --- | --- |
| 1 | elastic | none lost (ideal billiard balls) |
| between | partly elastic | some lost |
| 0 | perfectly inelastic | the most possible lost; they stick together |

The energy lost is `½·μ·(1 − e²)·u²`, where `μ = m·M/(m + M)` is the reduced
mass (§11). Checked exactly with `Fraction` for `m=3, M=1, u=2, e=½`: both
ways give `9/8`.

**In this project.** MATH.md §1–2 (the second law in the box) and §7 (the
damper sets `e`).

**Self-check.** Why is `e = 1` the only case where no energy is lost?

## 6. Functions, graphs and asymptotes

**Idea.** A **function** maps an input to one output: `f(r) = 2r/(1 + r)`.
Its graph can approach a line without reaching it; that line is an
**asymptote**.

**Example.** `f(1) = 1`, `f(1000) = 2000/1001 ≈ 1.998`, `f(10⁶) ≈ 1.999998`.
The outputs creep toward 2 but never reach it: `y = 2` is a horizontal
asymptote.

**In this project.** `out/paradox.svg` (from `python main.py report`) draws
`v_O/u` against `r` on a **log scale** (each step along the axis is ×10),
so you can see the curve level off at `1 + e`.

**Self-check.** What does `f(r)` approach as `r → 0`?

## 7. Infinity and limits

**Idea.** Infinity (`∞`) isn't a number you can calculate with. "As `x`
grows without bound" is written `x → ∞`, and the **limit** is the value the
output settles toward. Informally: `lim f(x) = L` means you can get `f(x)` as
close to `L` as you like by making `x` large enough.

**Indeterminate forms.** Some expressions have no fixed value, because the
answer depends on *how* you got there: `∞/∞`, `∞ − ∞`, `0·∞`, `0/0`.

| expression, as `x → ∞` | form | limit |
| --- | --- | --- |
| `x / x` | ∞/∞ | 1 |
| `2x / x` | ∞/∞ | 2 |
| `x² / x` | ∞/∞ | ∞ |
| `x / x²` | ∞/∞ | 0 |

Same form, four different answers. That's the whole paradox in miniature.

**In this project.** MATH.md §4 and `python/paradox/limits.py`.

**Self-check.** Why can't you "just plug in ∞" to `m/(m + M)`?

## 8. Limits in two variables, and order of limits

**Idea.** With two variables `m` and `M`, you can head to infinity along
many **paths** (both together, one faster, one after the other). A
two-variable limit **exists only if every path gives the same answer.**

An **iterated limit** takes one variable to infinity first, then the other.
The two orders can disagree. Swapping them is safe only under extra
conditions (uniform convergence), which a first analysis course covers.

**Example.** `f(m, M) = m/(m + M)`:
- along `m = M`: always `1/2`
- along `m = 2M`: always `2/3`
- `m` first, then `M`: `lim f = 1`, then 1
- `M` first, then `m`: `lim f = 0`, then 0

**In this project.** MATH.md §4–5; `python main.py math paths` and
`python main.py math iterated`.

**Self-check.** If two paths give different answers, what can you conclude
about the limit?

## 9. Logic: definitions, "for all" and proof by contradiction

**Idea.**
- A **definition** turns a vague word ("immovable") into a precise rule
  ("after *any* collision, `v_O = 0`").
- **"For all"** (∀) means *every* case must satisfy it; one counterexample
  breaks it.
- **Proof by contradiction**: assume the statement, reason correctly,
  reach something false, so the assumption was false.

**Example.** Claim: there's a largest whole number `N`. But `N + 1` is a
whole number bigger than `N`. Contradiction, so there's no largest one.

**In this project.** MATH.md §6 and `python/paradox/proof.py`.

**Self-check.** In MATH.md §6, which assumption gets thrown out, and why
that one?

## 10. Powers, roots and scientific notation

**Idea.** `10⁵⁰` means 1 followed by 50 zeros. Rules: `10ᵃ·10ᵇ = 10ᵃ⁺ᵇ`,
`√(10ᵃ) = 10^(a/2)`. **Scientific notation** writes `120 000` as
`1.2·10⁵`; computers print it as `1.2e5`.

**Example.** If the mass grows ×10⁵⁰, a quantity proportional to `√mass`
grows ×10²⁵.

**In this project.** MATH.md §7 (the peak force grows like a square root) and
§8 (`1.8·10³⁰⁸`, the largest `double`).

**Self-check.** What's `√(10¹⁰⁰)`?

## 11. Springs, oscillation and damping

**Idea.**
- **Hooke's law**: a spring pushes back in proportion to how far it's
  squeezed, `F = k·x`. `k` is the stiffness.
- A mass on a spring **oscillates**. The equation `m·x″ = −k·x` (a
  *differential equation*: it links `x` to how fast it changes) has the
  solution `x = A·sin(ω·t)` with `ω = √(k/m)`.
- A **damper** (like a shock absorber) pushes against the *velocity*,
  `F = c·v`, and turns motion into heat. The **damping ratio** `ζ` says how
  strong it is; `ζ = 1` is "critical" (no wobble).
- **Reduced mass** `μ = m·M/(m + M)`: two bodies pressing on one spring
  behave like a single body of mass `μ`.

**Example.** Half an oscillation takes `π/ω = π·√(μ/k)`. That's the contact
time in MATH.md §7.

**In this project.** `rust/collide/src/lib.rs`: the force is
`k·overlap + c·closing`, clamped at 0 so the contact never pulls.
`damping_ratio(e)` turns the restitution you ask for into `ζ`.

**Self-check.** If `μ → ∞` and `k` stays fixed, what happens to the contact
time?

## 12. Stepping through time: numerical integration

**Idea.** Most differential equations are solved by computers in small
steps of length `dt`:

```text
a = F / m            (acceleration from the force)
v = v + a·dt         (update the velocity first...)
x = x + v·dt         (...then the position with the NEW velocity)
```

Updating `v` first is **semi-implicit (symplectic) Euler**. It's as cheap as
plain Euler, but it keeps an oscillator's energy from drifting upward. A
smaller `dt` is more accurate and slower.

**In this project.** `rust/collide/src/lib.rs` uses 4000 steps per expected
contact time (`STEPS_PER_CONTACT`).

**Self-check.** What goes wrong if `dt` is larger than the whole contact?

## 13. How computers store numbers

**Idea.**
- **Integers** are exact but limited in size.
- **Floating point** (IEEE 754) is scientific notation in base 2: a sign,
  some significant digits, and an exponent. That gives a huge range, but only
  about 7 (`float`) or 16 (`double`) significant decimal digits.
- Past the largest value, a result **overflows** to `inf`. Undefined results
  like `inf/inf` or `0/0` give **NaN** ("not a number"), and NaN isn't even
  equal to itself.
- **Rounding**: `0.1 + 0.2` isn't exactly `0.3` in a `double`.
- Exact alternatives cost speed: Python's `Fraction` and `int` grow as large
  as needed.

**Example.** In Python, `1e308 * 10` gives `inf`, and `inf - inf` gives `nan`.

**In this project.** MATH.md §8 and `cpp/floats/`. See also
[C++ CONCEPTS](../cpp/floats/docs/CONCEPTS.md).

**Self-check.** Why does dividing *before* adding (`r/(1 + r)`) avoid overflow?

## 14. Self-test

You're ready for MATH.md if you can do these without looking:

1. Solve `2x + y = 7`, `x − y = 2`.
2. Simplify `3m/(m + 2M)` in terms of `r = m/M`.
3. A 1 kg ball at 4 m/s sticks to a 3 kg ball at rest. How fast do they move?
4. What does `5x/(x + 1)` approach as `x → ∞`? As `x → 0`?
5. Give two paths to infinity where `m/(m + M)` gives different answers.
6. What's `√(10⁶⁰)`?
7. Why is `float("inf") - float("inf")` NaN rather than 0?

<details><summary>Answers</summary>

1. `x = 3, y = 1`
2. `3r/(r + 2)`
3. `4/4 = 1 m/s`
4. `5`; `0`
5. e.g. `m = M` gives `1/2`; `m = M²` gives `1`
6. `10³⁰`
7. Both infinities could have come from anything large; their difference could be any value (§7)

</details>

## References

**§1–2 Algebra, fractions, ratios**
- OpenStax *College Algebra 2e*: [Systems of Linear Equations: Two Variables](https://openstax.org/books/college-algebra-2e/pages/7-1-systems-of-linear-equations-two-variables)
- Python docs: [fractions — Rational numbers](https://docs.python.org/3/library/fractions.html) ✔ (`Fraction` keeps exact results, as used in `collision.py`)

**§3–5 Motion, momentum, energy**
- OpenStax *University Physics Vol. 1*: [Linear Momentum](https://openstax.org/books/university-physics-volume-1/pages/9-1-linear-momentum), [Conservation of Linear Momentum](https://openstax.org/books/university-physics-volume-1/pages/9-3-conservation-of-linear-momentum), [Types of Collisions](https://openstax.org/books/university-physics-volume-1/pages/9-4-types-of-collisions)
- [Coefficient of restitution](https://en.wikipedia.org/wiki/Coefficient_of_restitution) (the energy-loss formula; ✔ checked numerically above)

**§6–8 Functions and limits**
- OpenStax *Calculus Vol. 1*: [The Limit of a Function](https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function), [Limits at Infinity and Asymptotes](https://openstax.org/books/calculus-volume-1/pages/4-6-limits-at-infinity-and-asymptotes)
- OpenStax *Calculus Vol. 3*: [Limits and Continuity (two variables)](https://openstax.org/books/calculus-volume-3/pages/4-2-limits-and-continuity)
- [Indeterminate form](https://en.wikipedia.org/wiki/Indeterminate_form), [Iterated limit](https://en.wikipedia.org/wiki/Iterated_limit)

**§9 Logic**
- Richard Hammack, [*Book of Proof*](https://richardhammack.github.io/BookOfProof/) (free; Chapter 6 is proof by contradiction)

**§10–12 Springs and time stepping**
- OpenStax *University Physics Vol. 1*: [Simple Harmonic Motion](https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion), [Damped Oscillations](https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations)
- [Reduced mass](https://en.wikipedia.org/wiki/Reduced_mass), [Semi-implicit Euler method](https://en.wikipedia.org/wiki/Semi-implicit_Euler_method)

**§13 Floating point**
- Python docs: [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html) ✔
- David Goldberg, [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)

### Further learning
- [Khan Academy: Algebra 1](https://www.khanacademy.org/math/algebra) and [Calculus 1: Limits and continuity](https://www.khanacademy.org/math/calculus-1/cs1-limits-and-continuity)
- [3Blue1Brown: Essence of calculus](https://www.3blue1brown.com/topics/calculus)
- [Khan Academy: Linear momentum](https://www.khanacademy.org/science/physics/linear-momentum)
- [Float Toy](https://evanw.github.io/float-toy/): flip the bits of a float and watch the value change
- [*Book of Proof*](https://richardhammack.github.io/BookOfProof/) exercises for logic practice
