# The math: what happens when an unstoppable force meets an immovable object?

Short answer: **the question has no answer, and the math shows exactly why.**
Three separate arguments, one per language in this project, each say "no
answer" in a different way.

## Contents

1. [Setting it up as physics](#1-setting-it-up-as-physics)
2. [Solving a collision](#2-solving-a-collision)
3. [Only the ratio matters](#3-only-the-ratio-matters)
4. [Infinity is a direction, not a number: limits](#4-infinity-is-a-direction-not-a-number-limits)
5. [Order matters: iterated limits](#5-order-matters-iterated-limits)
6. [The proof that both can't exist](#6-the-proof-that-both-cant-exist)
7. [Up close: the force between them (Rust)](#7-up-close-the-force-between-them-rust)
8. [The computer's answer: NaN (C++)](#8-the-computers-answer-nan-c)
9. [So what is the answer?](#9-so-what-is-the-answer)
10. [Exercises](#10-exercises)
11. [References](#references)

---

## 1. Setting it up as physics

| Thing | Symbol | Meaning |
| --- | --- | --- |
| the "force" F | mass `m`, speed `u` | it moves toward O |
| the "object" O | mass `M`, at rest | it waits |
| restitution | `e`, from 0 to 1 | 1 = perfectly bouncy, 0 = they stick |
| after the hit | `v_F`, `v_O` | their velocities |

"Unstoppable" and "immovable" become statements about mass:

- **unstoppable:** nothing slows F down, so `m` is far larger than anything it meets: `m → ∞`
- **immovable:** nothing moves O, so `M → ∞`

## 2. Solving a collision

Two laws hold in every collision:

```text
momentum is conserved:     m·u = m·v_F + M·v_O
restitution:               v_O − v_F = e·u
```

That's two equations in two unknowns. Solve the second for `v_O = v_F + e·u`,
substitute into the first, and simplify:

```text
v_F = (m − e·M)·u / (m + M)
v_O = (1 + e)·m·u / (m + M)
```

Checks you can do by hand (all in `python/tests/test_paradox.py`):

- **Equal masses, elastic (`m = M`, `e = 1`):** `v_F = 0`, `v_O = u`. The force stops dead and the object takes all its speed. That's Newton's cradle.
- **`M` much larger than `m`:** `v_O ≈ 0` and `v_F ≈ −e·u`. A ball bounces off a wall.
- **`m` much larger than `M`:** `v_F ≈ u` and `v_O ≈ (1+e)·u`. A truck hits a ping-pong ball.

## 3. Only the ratio matters

Divide the top and bottom of `v_O` by `M` and write `r = m / M`:

```text
v_O / u = (1 + e) · r / (1 + r)
```

**The masses themselves have disappeared.** Only their ratio is left. Doubling
both masses changes nothing. That's why Python's table shows
`m = M = 10^300` giving exactly the same answer as `m = M = 1`, and why Rust's
sweep shows identical speeds at `M = 1` and `M = 10^200`.

## 4. Infinity is a direction, not a number: limits

"Both masses infinite" isn't a value you can plug in: `∞/∞` has no meaning. In
calculus, "at infinity" means **a limit**: what the answer approaches as the
masses grow without bound.

A limit in two variables (`m → ∞` and `M → ∞` together) **exists only if every
path gives the same answer.** Take the paths `m = r·M` with a fixed `r`:

| path (r = m/M) | v_O / u as both masses → ∞ (e = 1) | what you'd see |
| --- | --- | --- |
| 1/1000 | 2/1001 ≈ 0.002 | the object barely moves: "immovable" wins |
| 1 | exactly 1 | a draw: they swap speeds |
| 1000 | 2000/1001 ≈ 1.998 | the object flies off: "unstoppable" wins |

Every value between 0 and `1 + e` happens on some path. Different paths give
different answers, so **the double limit does not exist**. "Both infinite"
hides a choice, *how fast each one grows*, and the outcome depends entirely
on that hidden choice. See `out/paradox.svg` (`python main.py report`).

## 5. Order matters: iterated limits

Instead of growing both together, grow them one after the other:

```text
unstoppable first:  lim (M→∞) [ lim (m→∞) v_O/u ] = lim (M→∞) (1 + e) = 1 + e
immovable first:    lim (m→∞) [ lim (M→∞) v_O/u ] = lim (m→∞) 0     = 0
```

The two orders give **different answers**. This is a classic lesson from
analysis: **limits do not always commute.** Swapping their order is only
allowed when certain conditions hold (uniform convergence), and here they
don't. `python main.py math iterated` shows it numerically:
`2.000000` versus `2e-120`.

## 6. The proof that both can't exist

The paradox has a logical answer too. Define:

- **immovable:** after *any* collision, `v_O = 0`
- **unstoppable:** after *any* collision, `v_F = u` (it isn't slowed at all)

Momentum: `m·u = m·u + M·0`. That's true, so no contradiction yet. But solid
bodies can't pass through each other, so after the hit the one behind can't be
moving faster than the one in front: `v_F ≤ v_O`. Substituting gives `u ≤ 0`,
which contradicts `u > 0`.

**So the two definitions can't both hold in one universe.** That's a *proof by
contradiction*: assume both exist, derive something false, and conclude the
assumption was false. If an unstoppable force exists, there is no immovable
object, and the other way round. `python main.py math proof` checks
every collision setting against all three rules.

## 7. Up close: the force between them (Rust)

The formulas jump from "before" to "after". In reality the bodies press
into each other briefly. The Rust simulator models the contact as a spring
(stiffness `k`) with a damper, and steps through time.

For an undamped spring contact, the peak force and the contact time follow from
the **reduced mass** `μ = m·M/(m+M)`:

```text
peak force   ≈ u · √(k·μ)
contact time ≈ π · √(μ/k)
```

As both masses → ∞, `μ → ∞`, so **the force between them → ∞**. The sweep shows
the peak force growing by ×10²⁵ each time the masses grow by ×10⁵⁰ (the square
root). In any real material, infinite force means something breaks before
"winning" means anything.

Two things found by the tests:
- **The damping formula gives a livelier bounce than asked for.** The usual
  formula linking damping to restitution, `e = exp(−ζπ/√(1−ζ²))`, assumes the
  contact can also *pull*. A real contact can't, so the simulator clamps the
  force at 0, the bodies part earlier, and the bounce is livelier: asking for
  `e = 0.5` gives about 0.55.
- **A spring-damper contact is never perfectly sticky.** Even critical damping
  (`e = 0`) rebounds at about 0.135.

## 8. The computer's answer: NaN (C++)

Computers store real numbers as **IEEE 754 floating point**, which has a
largest value: about `3.4·10³⁸` (`float`) or `1.8·10³⁰⁸` (`double`). Beyond it, a
result becomes `+inf`.

With `m = M = 1.2·10³⁰⁸` (fine on its own), the textbook formula computes
`m + M = 2.4·10³⁰⁸`, which **overflows to `inf`**. The numerator overflows too,
and `inf / inf = NaN` ("not a number"). The computer's answer to "unstoppable
meets immovable" is literally *no number*.

The rearranged formula `(1+e)·u·r/(1+r)` divides first, so its numbers stay
near 1. It gives exactly 1. **Two formulas that are equal on paper can behave
differently on a computer.** That's numerical stability, the everyday version
of this paradox. Even the stable form returns `NaN` for `m = M = inf`,
because `inf/inf` really has no value. The hardware agrees with the math.

## 9. So what is the answer?

| Viewpoint | Answer |
| --- | --- |
| algebra (§3) | only the ratio of masses matters; "both infinite" doesn't fix a ratio |
| calculus (§4–5) | the limit doesn't exist: every outcome from "O stays" to "O flies at 2u" is reachable |
| logic (§6) | the two definitions contradict each other: they can't both exist |
| physics (§7) | the force between them grows without bound: both are destroyed |
| computers (§8) | `inf / inf = NaN`: no number |

The paradox is a question with a hidden assumption. Each subject finds that
assumption in a different place.

## 10. Exercises

1. Derive `v_F` and `v_O` yourself from the two laws in §2. Then check `m = M`, `e = 0`: what does "sticking together" give?
2. Find the path `r` that gives `v_O/u = 1/2` when `e = 1`. Check it with `python main.py math paths`.
3. Use the path `m = M²`: both still → ∞. What does `v_O/u` tend to? Which "infinity" wins?
4. In C++, find the smallest power of ten where the naive formula breaks in `float`.
5. Change the Rust stiffness `k` by ×100. What happens to the peak force and the contact time? Does the outcome change?

**Self-check:** why doesn't plugging `m = M = ∞` into a formula count as solving the paradox?

## References

**Official / textbook**
- OpenStax *University Physics Vol. 1*: [Conservation of Linear Momentum](https://openstax.org/books/university-physics-volume-1/pages/9-3-conservation-of-linear-momentum), [Types of Collisions](https://openstax.org/books/university-physics-volume-1/pages/9-4-types-of-collisions)
- OpenStax *Calculus Vol. 3*: [Limits and Continuity (two variables)](https://openstax.org/books/calculus-volume-3/pages/4-2-limits-and-continuity)
- IEEE 754 explained: [cppreference: std::numeric_limits](https://en.cppreference.com/w/cpp/types/numeric_limits), [std::isnan](https://en.cppreference.com/w/cpp/numeric/math/isnan)
- [Coefficient of restitution](https://en.wikipedia.org/wiki/Coefficient_of_restitution), [Reduced mass](https://en.wikipedia.org/wiki/Reduced_mass)

**Other**
- David Goldberg, [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)
- [Irresistible force paradox](https://en.wikipedia.org/wiki/Irresistible_force_paradox)
- [Iterated limit](https://en.wikipedia.org/wiki/Iterated_limit), [Proof by contradiction](https://en.wikipedia.org/wiki/Proof_by_contradiction)

### Further learning
- [3Blue1Brown: Essence of calculus](https://www.3blue1brown.com/topics/calculus) (limits, visually)
- [Khan Academy: Elastic and inelastic collisions](https://www.khanacademy.org/science/physics/linear-momentum/elastic-and-inelastic-collisions/v/elastic-and-inelastic-collisions)
