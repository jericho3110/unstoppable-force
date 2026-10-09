# Libraries and built-ins

No third-party packages in any language. To re-check:
`git grep -nE "^(import|from) |^use |#include"`.

## Python (standard library)

| Module | Where | What for | Why |
| --- | --- | --- | --- |
| `fractions.Fraction` | `collision.py`, `limits.py`, `proof.py`, `cli.py` | exact rational numbers of any size | 10³⁰⁰ with no rounding; `float` would round and overflow |
| `dataclasses` | `collision.py` (`Outcome`, frozen) | immutable result records | less boilerplate |
| `html.escape` | `plot.py` | escape text placed into the SVG | correct XML even if labels change |
| `xml.etree.ElementTree` | tests | parse the SVG back to prove it's valid XML | standard library |
| `argparse` | `cli.py` | sub-commands, `--e` typed as `Fraction` | `type=Fraction` parses `"1/2"` directly |
| `subprocess`, `shutil.which`, `runpy`, `contextlib`, `io` | `main.py`, `tools/` | run cargo/clang/the binaries; capture output | argument lists, no shell |
| `unittest` | tests | test runner | built in |

Built-ins and features: `float()` (only for charts and printing), `zip(..., strict=False)`,
`isinstance`, f-strings with format specs (`{x:.6e}`), `__init__.py`.

## Rust (standard library only)

| Item | Where | What for |
| --- | --- | --- |
| `f64` methods `sqrt`, `ln`, `powi`, `is_finite`, `max`, `abs` | `lib.rs` | the physics |
| `std::f64::consts::PI` | `lib.rs` | contact time, damping formula |
| `std::fmt::Display`, `std::error::Error` | `SimError` | readable error messages, usable with `?` |
| `#[derive(Clone, Copy, Debug, PartialEq)]` | `Setup`, `Outcome` | value semantics, printing, comparing in tests |
| `std::env::args`, `std::process::ExitCode` | `main.rs` | the command line and exit status |
| `#[cfg(test)]`, `#[test]`, `assert!` | `lib.rs` | unit tests next to the code |

## C++ (standard library only)

| Header | Used | What for |
| --- | --- | --- |
| `<cmath>` | `std::isinf`, `std::isnan`, `std::fabs` | classify and compare floating-point results |
| `<limits>` | `std::numeric_limits<T>::max()`, `::infinity()` | the largest finite value and infinity, per type |
| `<cstdio>` | `std::printf` (`%Lg`, `%Le`) | formatted output, including `long double` |

## Tools (not libraries)

`cargo` (build, test, `fmt`, `clippy`), `clang++`, and the workspace's
`devtools` and `gitship` for checks and commits.

## References

**Official**
- [fractions](https://docs.python.org/3/library/fractions.html), [argparse type=](https://docs.python.org/3/library/argparse.html#type), [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [Rust std::f64](https://doc.rust-lang.org/std/primitive.f64.html), [std::error::Error](https://doc.rust-lang.org/std/error/trait.Error.html)
- [cppreference: numeric_limits](https://en.cppreference.com/w/cpp/types/numeric_limits), [isnan](https://en.cppreference.com/w/cpp/numeric/math/isnan), [printf](https://en.cppreference.com/w/cpp/io/c/fprintf)

### Further learning
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
