# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions: [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-10-10

### Added
- `docs/MATH_PREREQUISITES.md`: the background math and physics MATH.md assumes, from algebra up to floating point, each section tied to the code, with a self-test. Linked from the README, MATH, LEARNING_PATH (new stage 0) and GLOSSARY.

## [0.1.0] - 2026-10-09

### Added
- Python `paradox`: exact collision formulas with `Fraction`, paths to infinity (`m = r·M`), iterated limits, the proof by contradiction, and a hand-written SVG chart. 11 tests.
- Rust `collide`: a time-stepped spring-damper collision with a `sweep` and a `one` command. 7 tests; clippy and rustfmt clean.
- C++ `floats`: naive vs stable formulas in `float`/`double`/`long double`, showing overflow to `inf` and `NaN`. 24 checks.
- `main.py` front door (`math`, `simulate`, `floats`, `report`, `check`) and a check gate using the shared `devtools` scan and link check.
- Docs: MATH, ARCHITECTURE, LANGUAGES, SECURITY, LEARNING_PATH, CONVENTIONS, LIBRARIES_AND_BUILTINS, GLOSSARY, FILE_TYPES, and CONCEPTS per language.

### Found live
- A spring-damper contact bounces more than the damping formula predicts (asking for `e = 0.5` gives about 0.55), because a real contact can't pull. Even critical damping rebounds at about 0.135. Pinned by a Rust test, reported as `effective_restitution`.
- On Windows (clang with the Microsoft ABI), `long double` is 8 bytes, the same as `double`.
- The Rust crate builds with Smart App Control on: it has no dependencies, so no build scripts.
