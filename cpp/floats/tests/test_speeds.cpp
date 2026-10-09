// Tests for speeds.hpp. Exit code 0 = all checks passed.
#include <cmath>
#include <cstdio>
#include <limits>

#include "speeds.hpp"

static int checks = 0, failures = 0;
#define CHECK(cond)                                                      \
    do {                                                                 \
        ++checks;                                                        \
        if (!(cond)) {                                                   \
            ++failures;                                                  \
            std::fprintf(stderr, "FAIL line %d: %s\n", __LINE__, #cond); \
        }                                                                \
    } while (0)

template <typename T>
void same_formula_for_normal_numbers() {
    // For everyday masses both forms agree (to rounding).
    auto n = speeds::naive<T>(3, 7, 10, T(0.5));
    auto s = speeds::stable<T>(3, 7, 10, T(0.5));
    CHECK(std::fabs(n.v_object - s.v_object) < T(1e-5));
    CHECK(std::fabs(n.v_force - s.v_force) < T(1e-5));
    CHECK(std::fabs(s.v_object - T(4.5)) < T(1e-5));  // (1 + 0.5) * 3 * 10 / 10
}

template <typename T>
void naive_breaks_near_the_top_stable_does_not() {
    const T huge = std::numeric_limits<T>::max() / T(1.5);  // representable on its own...
    CHECK(std::isinf(huge + huge));                          // ...but the sum is not
    auto n = speeds::naive<T>(huge, huge, 1, 1);
    auto s = speeds::stable<T>(huge, huge, 1, 1);
    CHECK(std::isnan(n.v_object));  // inf / inf
    CHECK(s.v_object == T(1));      // exact: r = 1 gives (1+1)*1/(1+1)
    CHECK(s.v_force == T(0));       // equal masses, elastic: the force stops dead
}

int main() {
    same_formula_for_normal_numbers<float>();
    same_formula_for_normal_numbers<double>();
    same_formula_for_normal_numbers<long double>();
    naive_breaks_near_the_top_stable_does_not<float>();
    naive_breaks_near_the_top_stable_does_not<double>();
    naive_breaks_near_the_top_stable_does_not<long double>();

    const double inf = std::numeric_limits<double>::infinity();
    auto unstoppable = speeds::stable(inf, 1.0, 1.0, 1.0);
    CHECK(unstoppable.v_force == 1.0 && unstoppable.v_object == 2.0);  // the r -> infinity limit
    auto immovable = speeds::stable(1.0, inf, 1.0, 1.0);
    CHECK(immovable.v_object == 0.0 && immovable.v_force == -1.0);     // r = 0: F bounces straight back
    CHECK(std::isnan(speeds::stable(inf, inf, 1.0, 1.0).v_object));     // both infinite: no answer

    std::printf("%d checks, %d failures\n", checks, failures);
    return failures ? 1 : 0;
}
