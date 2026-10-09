# rust/collide: the collision, step by step

Simulates the hit as a stiff spring with a damper between the two bodies,
thousands of tiny time steps per collision. It shows what the instant formulas
skip: **the force between the bodies grows without bound as both masses grow.**

```powershell
python main.py simulate          # builds, then: collide sweep
python main.py simulate 0.5      # with restitution 0.5
cargo run --release -- one 1 1 1 1     # one collision: m M u e
cargo test --release             # 7 tests
```

Sweep excerpt (real output; masses grow ×10⁵⁰, speeds identical, force ×10²⁵):

```text
ratio,M,v_force_over_u,v_object_over_u,peak_force,...
1,1e0,-0.000000,1.000000,7.071e2,...
1,1e50,-0.000000,1.000000,7.071e27,...
1,1e100,-0.000000,1.000000,7.071e52,...
```

Concepts: [docs/CONCEPTS.md](docs/CONCEPTS.md). The physics: [../../docs/MATH.md](../../docs/MATH.md#7-up-close-the-force-between-them-rust).

## References

**Official**
- [The Rust Book](https://doc.rust-lang.org/book/)

### Further learning
- [Exercism Rust](https://exercism.org/tracks/rust)
