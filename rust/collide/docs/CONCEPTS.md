# Rust concepts

## Python → Rust

| Python | Rust here |
| --- | --- |
| `@dataclass(frozen=True)` | `#[derive(Clone, Copy, Debug, PartialEq)] pub struct Setup { … }` |
| `raise ValueError(...)` | `return Err(SimError::BadRestitution)`; the caller must handle the `Result` |
| `class SimError(Exception)` | `pub enum SimError { NotPositive(&'static str), … }` + `impl Display` + `impl Error` |
| `for x in [a, b]:` | `for (value, name) in [(s.m, "m"), …]` (tuples, destructured) |
| `if __name__ == "__main__"` | `fn main() -> ExitCode` in `main.rs`; the library is `lib.rs` |
| `unittest` | `#[cfg(test)] mod tests { #[test] fn … }`, in the same file |

## `Result` and `?`

`simulate` returns `Result<Outcome, SimError>`: either a value or an error,
and the compiler won't let you use the value without dealing with the error.
In `main.rs`, `simulate(&s).map_err(|err| err.to_string())?` converts the
error into a message, and `?` returns early if it's an error. Python's
exceptions can be forgotten; a `Result` can't.

## Ownership (and why there's so little of it here)

Every value has one owner and is freed when the owner goes out of scope (no
GC, no manual `free`). This crate barely needs it: `Setup` and `Outcome` are
`Copy` (a handful of `f64`s copied like integers), and `simulate(&s)` *borrows*
the setup (`&`), which reads it without taking ownership. The only heap value
is the `Vec<String>` of command-line arguments, freed automatically at the end
of `main`.

## `f64` and the special values

`f64` is an IEEE 754 double, the same as Python's `float`. `is_finite()`
rejects `inf` and `NaN` at the boundary (`simulate` refuses them). The mass
formula is written as `m / (1.0 + m / big_m)` instead of `m*M/(m+M)`, because
`m*M` overflows for masses around 10²⁰⁰. That's the same stability idea as
the C++ part.

## Time stepping

```rust
v_f -= force / s.m * dt;     // velocities first…
v_o += force / s.big_m * dt;
x_f += v_f * dt;             // …then positions, using the NEW velocities
x_o += v_o * dt;
```

This is **semi-implicit (symplectic) Euler**. Updating position with the *old*
velocity (explicit Euler) slowly adds energy to a spring, so a "perfectly
elastic" bounce would come out faster than it went in. Equal and opposite
forces (`-=` / `+=`) make momentum conserved up to rounding, which a test
checks (`< 1e-9`).

## Tests found two real effects

`restitution_sets_the_separation_speed_slightly_high_because_contacts_cannot_pull`
pins what the first version of the test revealed: the damping formula
assumes the contact can pull, so the bounce is livelier than asked for, and
a spring-damper contact is never perfectly sticky (≈ 0.135 rebound at e = 0).
The code now reports `effective_restitution` instead of pretending.

## Tooling

| Command | Does |
| --- | --- |
| `cargo build --release` | optimised build (`opt-level = 3`) |
| `cargo test --release` | the 7 unit tests |
| `cargo clippy -- -D warnings` | lints; warnings fail the build |
| `cargo fmt --check` | formatting matches `rustfmt` |
| `CARGO_TARGET_DIR` | puts build output outside OneDrive (set by `main.py`) |

## Exercises

1. Replace semi-implicit Euler with explicit Euler and watch the `e = 1` test fail. Why does it gain energy?
2. Add a `max_steps` field to `Setup` instead of the constant.
3. Return the contact force over time as a `Vec<f64>` and plot it from Python.

## References

**Official**
- The Rust Book: [Result and `?`](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html), [ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html), [tests](https://doc.rust-lang.org/book/ch11-01-writing-tests.html), [derive](https://doc.rust-lang.org/book/appendix-03-derivable-traits.html)
- [std::f64](https://doc.rust-lang.org/std/primitive.f64.html), [Clippy](https://doc.rust-lang.org/clippy/)

**Other**
- [Semi-implicit Euler method](https://en.wikipedia.org/wiki/Semi-implicit_Euler_method)

### Further learning
- [Rustlings](https://github.com/rust-lang/rustlings) (small exercises)
