# Unstoppable Force

What happens when an **unstoppable force** meets an **immovable object**? A fun
math project that answers the old paradox three ways, in three languages:

| Language | Folder | Its job | Its answer |
| --- | --- | --- | --- |
| **Python** | [python/](python/) | exact math with fractions: formulas, limits, a proof | the limit doesn't exist; the definitions contradict each other |
| **Rust** | [rust/collide/](rust/collide/) | a step-by-step collision simulation | the force between them grows without bound |
| **C++** | [cpp/floats/](cpp/floats/) | what `float` / `double` do at huge numbers | `inf / inf = NaN`: no number at all |

The full explanation, with derivations, is in **[docs/MATH.md](docs/MATH.md)**.

## Contents
- [Quick start](#quick-start)
- [Setup](#setup)
- [Layout](#layout)
- [Checks](#checks)
- [Documentation](#documentation)
- [References](#references)

## Quick start

```powershell
python main.py math paths       # exact answers along different routes to infinity
python main.py math iterated    # unstoppable-first vs immovable-first
python main.py math proof       # why both can't exist together
python main.py simulate         # Rust: step-by-step collisions (CSV)
python main.py floats           # C++: overflow, infinity and NaN
python main.py report           # all of it -> out/report.md + out/paradox.svg (a chart)
```

A taste (`python main.py math paths`):

```text
   r = m/M    object speed v_O/u  meaning
    1/1000                2/1001  object barely moves
         1                     1  both move
      1000             2000/1001  object flies off

The same ratio at ever larger masses gives the SAME answer (exact, no rounding):
  m = M = 10^0    v_O/u = 1
  m = M = 10^300  v_O/u = 1
```

## Setup

| Need | For | Get it |
| --- | --- | --- |
| Python 3.11+ | `main.py`, the math | [python.org](https://www.python.org/downloads/) |
| Rust (cargo) | the simulator | [rustup.rs](https://rustup.rs/) |
| clang++ + Visual Studio Build Tools | the C++ part (Windows) | [LLVM releases](https://github.com/llvm/llvm-project/releases), [Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |
| devtools (+ gitship) | the security and link checks | `pip install -e <mr-factory-workspace>/packages/gitship -e <…>/packages/devtools` |

There are no third-party packages in any language. Compiled programs are built
outside the repo and outside OneDrive, under `%LOCALAPPDATA%\UnstoppableForce\`.
With Windows **Smart App Control** on, the Rust part still builds: it has no
dependencies, so there are no build scripts for Smart App Control to block.

## Layout

```text
main.py                  the front door
python/paradox/          collision.py · limits.py · proof.py · plot.py · cli.py
python/tests/            11 tests (exact arithmetic)
rust/collide/            src/lib.rs (simulator + 7 tests) · src/main.rs (CLI)
cpp/floats/              include/speeds.hpp · src/main.cpp · tests/ (24 checks)
tools/check_all.py       the check gate
docs/                    MATH, ARCHITECTURE, LANGUAGES, SECURITY, LEARNING_PATH, ...
```

## Checks

```powershell
python main.py check                 # python, rust (fmt + clippy + tests), cpp, security, links
python main.py check rust cpp        # some
```

Commits go through [gitship](https://github.com/jericho3110/mr-factory-workspace/tree/main/packages/gitship),
which runs this first.

## Documentation

| Doc | What's in it |
| --- | --- |
| [docs/MATH_PREREQUISITES.md](docs/MATH_PREREQUISITES.md) | the background MATH.md assumes: algebra, momentum, energy, limits, logic, springs, time stepping, floating point, with a self-test |
| [docs/MATH.md](docs/MATH.md) | **start here**: collisions, limits, iterated limits, the proof, contact forces, floating point |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | how the three parts fit together, and why |
| [docs/LANGUAGES.md](docs/LANGUAGES.md) | why each language, its strengths here, and whether one would be enough |
| [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) | a reading order with exercises |
| [docs/SECURITY.md](docs/SECURITY.md) | the (small) threat model and the checks |
| [docs/LIBRARIES_AND_BUILTINS.md](docs/LIBRARIES_AND_BUILTINS.md) · [docs/GLOSSARY.md](docs/GLOSSARY.md) · [docs/FILE_TYPES.md](docs/FILE_TYPES.md) · [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | reference |
| per language | [python](python/docs/CONCEPTS.md) · [rust](rust/collide/docs/CONCEPTS.md) · [c++](cpp/floats/docs/CONCEPTS.md) |
| [CHANGELOG.md](CHANGELOG.md) | versions |

Just for fun.

## References

**Official**
- [Python](https://docs.python.org/3/), [The Rust Book](https://doc.rust-lang.org/book/), [cppreference](https://en.cppreference.com/)

### Further learning
- [Irresistible force paradox (Wikipedia)](https://en.wikipedia.org/wiki/Irresistible_force_paradox)
