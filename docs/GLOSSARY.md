# Glossary

| Term | Meaning | Explained in |
| --- | --- | --- |
| restitution `e` | how bouncy a collision is: 1 elastic, 0 sticky | [MATH §1–2](MATH.md#2-solving-a-collision) |
| indeterminate form | `∞/∞`, `0/0`, `∞ − ∞`, `0·∞`: no fixed value; the answer depends on how you got there | [PREREQ §7](MATH_PREREQUISITES.md#7-infinity-and-limits) |
| reduced mass `μ` | `m·M/(m+M)`: two bodies on one spring act like one body of this mass | [PREREQ §11](MATH_PREREQUISITES.md#11-springs-oscillation-and-damping) |
| momentum | mass × velocity; conserved in every collision | [MATH §2](MATH.md#2-solving-a-collision) |
| limit | the value a quantity approaches, not a value it takes | [MATH §4](MATH.md#4-infinity-is-a-direction-not-a-number-limits) |
| double limit | a limit in two variables; exists only if every path agrees | [MATH §4](MATH.md#4-infinity-is-a-direction-not-a-number-limits) |
| iterated limit | one limit taken inside another; the order can matter | [MATH §5](MATH.md#5-order-matters-iterated-limits) |
| proof by contradiction | assume it, derive something false, reject the assumption | [MATH §6](MATH.md#6-the-proof-that-both-cant-exist) |
| reduced mass `μ` | `m·M/(m+M)`: the "effective" mass of a two-body contact | [MATH §7](MATH.md#7-up-close-the-force-between-them-rust) |
| semi-implicit Euler | update velocity, then position with the new velocity | [ARCHITECTURE](ARCHITECTURE.md#design-choices) |
| IEEE 754 | the standard for floating-point numbers | [MATH §8](MATH.md#8-the-computers-answer-nan-c) |
| overflow / `inf` / `NaN` | too big to store / infinity / "not a number" (e.g. `inf/inf`) | [MATH §8](MATH.md#8-the-computers-answer-nan-c) |
| numerical stability | rearranging a formula so a computer gets it right | [C++ CONCEPTS](../cpp/floats/docs/CONCEPTS.md) |
| exact rational | a fraction of two integers, no rounding (`Fraction`) | [Python CONCEPTS](../python/docs/CONCEPTS.md) |

## References

**Official**
- [IEEE 754 (Wikipedia overview)](https://en.wikipedia.org/wiki/IEEE_754)

### Further learning
- [Paul's Online Math Notes: limits](https://tutorial.math.lamar.edu/classes/calci/limitsintro.aspx)
