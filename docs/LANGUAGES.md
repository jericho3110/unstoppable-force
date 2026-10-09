# Why three languages

| | Python | Rust | C++ |
| --- | --- | --- | --- |
| Job here | exact math, the proof, the chart, the orchestrator | the time-stepped simulation | floating-point behaviour at the extremes |
| Why it fits | `fractions.Fraction`: arbitrary-size exact rationals in the standard library | fast loops (the sweep runs 80,000+ steps per collision), and the compiler catches mistakes | templates run one formula on `float`/`double`/`long double`; direct access to IEEE 754 behaviour |
| Memory | automatic (reference counting + GC) | ownership: no GC, no manual `free`; everything here lives on the stack | RAII and values; nothing on the heap in this code |
| Paradigm | procedural, immutable dataclasses | procedural with structs, enums and `Result` | generic (templates) and procedural |
| Weakness here | slow for big loops (the simulation would take seconds) | more ceremony: types, `Result`, a build step | easy to write undefined behaviour (none here), and platform quirks like `long double` |
| Effectiveness | ★★★★★ | ★★★★ | ★★★★ |

## How they complement each other

- **Python is exact but slow.** It proves things about the formulas.
- **Rust is fast and safe.** It runs the many tiny steps the formulas skip.
- **C++ exposes the machine.** It shows where numbers themselves give out.

Each one checks the others: Rust's simulated speeds match Python's exact
formulas (a Rust test), and C++'s stable formula matches the same exact
values for ordinary numbers (a C++ test).

## Could one language do it all?

**Yes. Python alone could do all of it:** `fractions` for the math, a loop for
the simulation (slower, but fine), and NumPy or plain floats for the IEEE 754
part. The three-language version is for learning: each part sits in the
language that shows its idea most clearly (exactness, speed and safety, the
bare machine). For a real tool, use one language.

## References

**Official**
- [Python fractions](https://docs.python.org/3/library/fractions.html), [The Rust Book: ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html), [cppreference: templates](https://en.cppreference.com/w/cpp/language/templates)

### Further learning
- [Exercism tracks](https://exercism.org/tracks) for [Python](https://exercism.org/tracks/python), [Rust](https://exercism.org/tracks/rust) and [C++](https://exercism.org/tracks/cpp)
