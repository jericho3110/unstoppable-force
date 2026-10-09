# Python concepts

## `fractions.Fraction`: exact arithmetic

```python
>>> from fractions import Fraction
>>> Fraction(1, 3) + Fraction(1, 6)
Fraction(1, 2)
>>> 0.1 + 0.2              # float: binary rounding
0.30000000000000004
>>> Fraction(10) ** 300 + 1 - Fraction(10) ** 300
Fraction(1, 1)             # exact even at 10^300; a float would give 0
```

A `Fraction` is a pair of Python integers (numerator, denominator), always
in lowest terms. Python integers have no size limit, so a fraction can't
overflow or round. Every formula in `collision.py` stays exact. That's how
the project *proves* that `m = M = 10^300` gives exactly the same answer as
`m = M = 1`, rather than "about the same". The cost is speed: fractions are
slower than floats and get slower as the numbers grow.

`argparse` can use `Fraction` as a type: `p.add_argument("--e", type=Fraction)`
turns `--e 1/2` into `Fraction(1, 2)`.

## Frozen dataclasses

`@dataclass(frozen=True) class Outcome` writes `__init__`, `__repr__` and
`__eq__` for you, and `frozen=True` makes the result immutable: a computed
collision can't be changed afterwards by accident.

## Generators

`limits.along_ratio` uses `yield`: it produces one (k, value) pair at a time.
The caller decides how many to consume. Nothing is computed until asked for.

## Writing SVG by hand

SVG is XML text: `<line x1=… />`, `<polyline points="x,y x,y …"/>`, `<text>`.
`plot.py` maps math coordinates to pixels with two small functions:

```python
def x(log_r): return PAD + (log_r - lo) / (hi - lo) * (W - 2*PAD)   # log10(r) → pixels, left to right
def y(v):     return H - PAD - v / 2 * (H - 2*PAD)                  # 0..2 → pixels, bottom to top
```

The screen's y axis points *down*, so `y` subtracts from the bottom edge.
`html.escape` makes any text safe inside XML. The test parses the output
back with `xml.etree.ElementTree`, which proves it's valid.

## Memory and paradigm

Python manages memory automatically: reference counting, plus a collector for
reference cycles. The code is procedural: small pure functions over immutable
data, and no classes with behaviour. That fits math well. A formula is a
function.

## Exercises

1. Time `collide(10**k, 10**k, 1)` for k = 10, 1000, 100000. Why does it slow down?
2. Make `along_ratio` also yield `v_F`. Update the test.
3. Add `--lo/--hi` options to the plot command.

## References

**Official**
- [fractions](https://docs.python.org/3/library/fractions.html), [Floating-point arithmetic: issues and limitations](https://docs.python.org/3/tutorial/floatingpoint.html), [dataclasses](https://docs.python.org/3/library/dataclasses.html), [Generators (glossary)](https://docs.python.org/3/glossary.html#term-generator)

### Further learning
- Real Python: [Representing Rational Numbers With Python Fractions](https://realpython.com/python-fractions/)
