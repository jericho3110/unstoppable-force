# Security

A small, offline project, so the threat model is small too. It still gets the
same review as every project.

| Path | Risk | Why it's fine |
| --- | --- | --- |
| `main.py` runs cargo, clang++ and the two built programs | command injection | fixed argument lists, no shell; the only user input (`simulate [e]`) goes to the Rust program as one argument, which parses it as a number or refuses |
| Rust CLI arguments | bad numbers | `parse::<f64>()`, then `simulate()` refuses non-finite or non-positive values and `e` outside 0..1 |
| C++ | memory bugs | no pointers, arrays or string copies: only arithmetic on values; built with `-Wall -Wextra -Werror` |
| Python CLI `--e` | bad input | parsed as a `Fraction`, range-checked |
| Generated files | committing build output or local paths | `out/`, `*.exe` and `graphify-out/` are git-ignored; build output lives outside the repo |
| Dependencies | supply chain | none in any language |

**Automated:** `python main.py check` runs `devtools scan` (code patterns,
secrets, personal data, never-commit files) and `devtools links --offline`,
from the shared mr-factory-workspace package.

## References

**Official**
- [Python subprocess: security considerations](https://docs.python.org/3/library/subprocess.html#security-considerations)
- MITRE [CWE-78](https://cwe.mitre.org/data/definitions/78.html)

### Further learning
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/) (what safe Rust protects you from)
