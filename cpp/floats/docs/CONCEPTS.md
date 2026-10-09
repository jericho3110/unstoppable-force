# C++ concepts

## IEEE 754 floating point

A `double` stores a number as sign × 1.fraction × 2^exponent in 64 bits. That
gives about 15–16 decimal digits of precision and a range up to about
1.8·10³⁰⁸. Special values exist for when results leave that range:

| Value | Comes from | Test with |
| --- | --- | --- |
| `+inf` | overflow (`1e308 * 10`), `1.0/0.0` | `std::isinf` |
| `NaN` | `inf - inf`, `inf / inf`, `0.0/0.0` | `std::isnan` (`NaN != NaN`, so `x == NaN` never works) |

Real output from `floats.exe`:

```text
float         4 bytes, largest finite value 3.403e+38
double        8 bytes, largest finite value 1.798e+308
long double   8 bytes, largest finite value 1.798e+308
```

**Found live:** on Windows, `long double` is just `double`. The Microsoft ABI,
which clang follows there, makes them the same. On Linux with GCC it's
usually an 80-bit extended type (16 bytes). Portable code can't rely on
`long double` being more precise.

## Numerical stability: same algebra, different results

```cpp
naive:  (1 + e) * m * u / (m + M)      // m + M overflows → inf/inf = NaN
stable: (1 + e) * u * r / (1 + r)      // r = m / M ≈ 1: stays exact
```

Mathematically identical, but numerically very different. The rule of thumb:
**divide or scale first, so the numbers stay near 1.** Rust's
`reduced_mass` uses the same trick.

## Templates

```cpp
template <typename T>
Speeds<T> naive(T m, T big_m, T u, T e);
```

One definition, and the compiler generates a separate version for each type it's
used with (`naive<float>`, `naive<double>`, …). It's like a Python function that
works for any number type, except the type is fixed at compile time, so there's
no runtime cost. `T(1)` writes "1 in whatever type T is".

## Header-only

`speeds.hpp` holds the whole library. Templates must be visible where they're
used, so they live in headers. `#pragma once` stops a header being included twice.

## Memory and paradigm

Nothing here touches the heap: every value is a local, copied like an `int`.
That's the easiest kind of C++ memory to get right (no RAII objects needed, no
`new`). The style is generic and procedural: templated pure functions.

## Building

```powershell
clang++ -std=c++20 -Wall -Wextra -Werror -O2 -Iinclude src/main.cpp -o floats.exe
```

`-std=c++20` sets the language version; `-Wall -Wextra -Werror` enables warnings
and makes them fatal; `-O2` optimises; `-Iinclude` finds `speeds.hpp`.

## Exercises

1. Make the naive formula survive by reordering it (without the ratio). How far can you get?
2. Print `0.1 + 0.2 == 0.3` in C++. Explain the result.
3. Use `std::nextafter` to print the largest `double` and the one just below it.

## References

**Official**
- cppreference: [numeric_limits](https://en.cppreference.com/w/cpp/types/numeric_limits), [isnan](https://en.cppreference.com/w/cpp/numeric/math/isnan), [isinf](https://en.cppreference.com/w/cpp/numeric/math/isinf), [templates](https://en.cppreference.com/w/cpp/language/templates), [long double](https://en.cppreference.com/w/cpp/language/types)
- Microsoft: [Type long double (C/C++)](https://learn.microsoft.com/en-us/cpp/c-language/type-long-double)

**Other**
- [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)
- [Float Toy](https://evanw.github.io/float-toy/) (see the bits of a float)

### Further learning
- [learncpp.com: floating point numbers](https://www.learncpp.com/cpp-tutorial/floating-point-numbers/)
