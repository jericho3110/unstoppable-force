# python/: exact math

`paradox` solves the collision exactly with fractions, shows that the
"both infinite" limit depends on the path, checks the iterated limits, proves
by contradiction that both objects can't exist, and draws the SVG chart.

```powershell
python main.py math paths | iterated | proof
python main.py math --e 1/2 paths       # a less bouncy collision
python main.py math plot out/paradox.svg
python -m unittest discover -s tests -t .   # from this folder: 11 tests
```

| Module | Job |
| --- | --- |
| `collision.py` | `collide(m, M, u, e)` and `object_speed_ratio(r, e)` |
| `limits.py` | paths `m = r·M`, iterated limits |
| `proof.py` | the contradiction, checked against real collisions |
| `plot.py` | the hand-written SVG chart |
| `cli.py` | the `math` commands |

Concepts: [docs/CONCEPTS.md](docs/CONCEPTS.md). The math: [../docs/MATH.md](../docs/MATH.md).

## References

**Official**
- [fractions](https://docs.python.org/3/library/fractions.html)

### Further learning
- [Exercism Python](https://exercism.org/tracks/python)
