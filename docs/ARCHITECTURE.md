# Architecture

## The shape

**Three independent programs and one orchestrator.** The languages don't call
each other. They answer the same question from three angles, and Python's
`main.py` runs them and gathers the results.

```text
                    python main.py ...
                           │
     ┌─────────────────────┼──────────────────────┐
  math ...           simulate               floats         report = all three
     │                     │                      │                 │
python/paradox     cargo build → collide.exe   clang++ → floats.exe  out/report.md
(in-process)        (CSV on stdout)            (table on stdout)    out/paradox.svg
```

| Part | Kind | Talks to the others by |
| --- | --- | --- |
| `python/paradox` | library + CLI, imported by `main.py` | a Python import |
| `rust/collide` | library (`lib.rs`) + small binary (`main.rs`) | text on stdout (CSV) |
| `cpp/floats` | header-only library + small binary | text on stdout |

**Why separate programs with text between them,** and not Rust compiled into a
Python module (PyO3) or C++ called through FFI?
- **Simplicity:** text is the easiest interface to debug. You can run each
  program on its own.
- **No build-script dependencies:** PyO3 needs a build step that Windows Smart
  App Control may block. A plain binary doesn't.
- **YAGNI:** the programs exchange a few lines of numbers, not millions, so
  there's nothing to gain from in-process speed.

(The Teto project shows the in-process alternatives: FFI and WebAssembly.)

## One command, end to end

`python main.py report`:

```text
main.py  report()
  python_cli(["plot", out/paradox.svg])      import paradox.cli → plot.chart() → SVG text
  python_cli(["paths"]) …                    exact Fractions, captured with redirect_stdout
  rust_binary()                              cargo build --release (CARGO_TARGET_DIR outside OneDrive)
  run([collide.exe, "sweep"])                argument list, no shell → CSV
  cpp_binary()                               clang++ -std=c++20 -O2 -Wall -Wextra -Werror
  run([floats.exe])                          → overflow / NaN table
  write out/report.md                        out/ is git-ignored
```

## Design choices

| Choice | Alternatives | Why |
| --- | --- | --- |
| exact `Fraction`s in Python | floats, `decimal`, SymPy | 10³⁰⁰ is exact with no rounding; the standard library is enough (SymPy would be a dependency) |
| semi-implicit Euler in Rust | explicit Euler, RK4 | stable for springs (explicit Euler gains energy), simple, and momentum stays exact because forces are applied pairwise |
| time step = contact time / 4000 | a fixed dt | the contact time ranges from 10⁻⁴ to 10⁹⁷ seconds across the sweep; a fixed step would be wrong for most of it |
| header-only C++ with templates | one function per type | one formula, instantiated for `float`, `double`, `long double` |
| hand-written SVG | matplotlib | no dependency; SVG is just text (and the test parses it back as XML) |
| shared `devtools` for security and links | a local copy | the duplication the code graph found (see mr-factory-workspace docs/CODE_GRAPH.md) |

## Principles used

| Principle | Where |
| --- | --- |
| Single responsibility | one question per language; one job per Python module |
| Functional core | `collision.py`, `limits.py`, `speeds.hpp`, `simulate()` are pure: inputs to outputs |
| Value objects | `Outcome` (Python dataclass, Rust struct), `Speeds<T>` |
| Validate at the boundary | `collide()` and `simulate()` refuse non-positive masses and bad `e` |
| Numerical stability | `reduced_mass` written as `m/(1 + m/M)`; C++ `stable()` divides first |
| Tests pin discoveries | the "livelier bounce than asked for" and "never perfectly sticky" findings are tests, not just comments |

## Known limits

- One dimension, point masses, linear contact spring: the simplest model that
  shows the effect. Real impacts involve 3-D shapes and materials that break.
- The Rust "e" setting is approximate (see MATH.md §7). It reports the real
  `effective_restitution`.
- On Windows `long double` = `double` (8 bytes), so the C++ comparison has only
  two distinct precisions there. On Linux/GCC it usually has three.

## References

**Official**
- Python [fractions](https://docs.python.org/3/library/fractions.html), [subprocess](https://docs.python.org/3/library/subprocess.html)
- [The Cargo Book: build cache / CARGO_TARGET_DIR](https://doc.rust-lang.org/cargo/reference/build-cache.html)
- [PyO3 user guide](https://pyo3.rs/) (the in-process alternative not used)

**Other**
- [Semi-implicit Euler method](https://en.wikipedia.org/wiki/Semi-implicit_Euler_method)
- Glenn Fiedler, [Integration Basics](https://gafferongames.com/post/integration_basics/)

### Further learning
- [The Nature of Code, ch. 2 Forces](https://natureofcode.com/forces/) (free, visual)
