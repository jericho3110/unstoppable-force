# Learning path

| Stage | Read | Concepts | Exercise | Self-check |
| --- | --- | --- | --- | --- |
| 0 | [MATH_PREREQUISITES.md](MATH_PREREQUISITES.md) | algebra, ratios, momentum, energy, limits, logic, floating point | its §14 self-test | why is `∞/∞` called indeterminate? |
| 1 | [MATH.md](MATH.md) §1–3, `python/paradox/collision.py` | momentum, restitution, solving two equations, `Fraction` | derive `v_F` by hand | why do the masses cancel to a ratio? |
| 2 | MATH.md §4–6, `limits.py`, `proof.py` | limits, paths, iterated limits, proof by contradiction | MATH.md exercise 3 (the path `m = M²`) | why does the double limit not exist? |
| 3 | `plot.py` | SVG as text, coordinate transforms, log scale | add a fourth curve for `e = 0.25` | why does the test parse the SVG back? |
| 4 | MATH.md §7, `rust/collide/src/lib.rs`, [Rust CONCEPTS](../rust/collide/docs/CONCEPTS.md) | structs, `Result`, enums, time stepping, reduced mass | MATH.md exercise 5 (stiffness ×100) | why is momentum conserved to rounding? |
| 5 | MATH.md §8, `cpp/floats/`, [C++ CONCEPTS](../cpp/floats/docs/CONCEPTS.md) | IEEE 754, overflow, inf, NaN, templates, numerical stability | MATH.md exercise 4 | why does `stable()` survive where `naive()` gives NaN? |
| 6 | [ARCHITECTURE.md](ARCHITECTURE.md), `main.py`, `tools/check_all.py` | orchestration over text, a check gate | add a `python main.py csv` command that saves Rust's sweep | why separate programs instead of FFI? |

## References

**Official**
- [The Python Tutorial](https://docs.python.org/3/tutorial/), [The Rust Book](https://doc.rust-lang.org/book/), [learncpp.com](https://www.learncpp.com/)

### Further learning
- [Brilliant / Khan Academy: limits](https://www.khanacademy.org/math/calculus-1/cs1-limits-and-continuity)
