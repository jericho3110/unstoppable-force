# Conventions

- **Layout:** one folder per language (`python/`, `rust/collide/`, `cpp/floats/`), each with README, CHANGELOG and `docs/CONCEPTS.md`. Workspace docs live in `docs/`.
- **Naming:** Python `snake_case`; Rust `snake_case` functions, `PascalCase` types (`Setup`, `Outcome`, `SimError`); C++ `snake_case` in `namespace speeds`. In Rust and C++, the object's mass is `big_m`, because `M` and `m` can't both be variable names in idiomatic Rust.
- **Dependencies:** none in any language. Adding one needs a written reason in [LIBRARIES_AND_BUILTINS.md](LIBRARIES_AND_BUILTINS.md).
- **Warnings are errors:** `clippy -D warnings`, `cargo fmt --check`, `clang++ -Wall -Wextra -Werror`.
- **Build output** goes to `%LOCALAPPDATA%\UnstoppableForce\`, never into the repo or OneDrive.
- **Discoveries become tests** (e.g. the restitution findings in `lib.rs`), plus a line in the CHANGELOG.
- **Commits:** `gitship ship -F msg.txt <files>`, which runs `python main.py check`. Summary in the imperative, at most 72 characters; the body explains why and how it was verified.
- **Repo:** private.

## References

**Official**
- [PEP 8](https://peps.python.org/pep-0008/), [Rust API Guidelines: naming](https://rust-lang.github.io/api-guidelines/naming.html), [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

### Further learning
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/)
