# cpp/floats: the computer's answer

Runs the collision formula at the edge of what `float`, `double` and
`long double` can hold. The textbook formula overflows to `inf / inf = NaN`;
the rearranged one stays exact. With both masses truly infinite, both give
`NaN`, because the question has no numeric answer.

```powershell
python main.py floats      # builds with clang++, then runs
```

| File | Job |
| --- | --- |
| [include/speeds.hpp](include/speeds.hpp) | `naive<T>()` and `stable<T>()`, templates over the number type |
| [src/main.cpp](src/main.cpp) | the demo table |
| [tests/test_speeds.cpp](tests/test_speeds.cpp) | 24 checks |

Concepts: [docs/CONCEPTS.md](docs/CONCEPTS.md).

## References

**Official**
- [cppreference: numeric_limits](https://en.cppreference.com/w/cpp/types/numeric_limits)

### Further learning
- [Exercism C++](https://exercism.org/tracks/cpp)
