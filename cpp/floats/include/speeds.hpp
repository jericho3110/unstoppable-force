// speeds.hpp: the collision formulas, written two ways, for any floating-point type.
//
// On paper these are the SAME formula. On a computer they are not:
//
//   naive:   v_O = (1 + e) * m * u / (m + M)
//   stable:  v_O = (1 + e) * u * r / (1 + r)      with r = m / M
//
// Floating-point numbers have a largest value (about 3.4e38 for float,
// 1.8e308 for double). Past it, a result becomes +infinity. For huge but
// still representable masses, m + M overflows to infinity, so does the
// numerator, and infinity / infinity is NaN ("not a number"). That's the
// computer's own answer to the paradox. The stable form divides first,
// keeping numbers near 1, and stays exact.
#pragma once

#include <cmath>

namespace speeds {

template <typename T>
struct Speeds {
    T v_force;
    T v_object;
};

// Straight from the textbook. Overflows for huge masses.
template <typename T>
Speeds<T> naive(T m, T big_m, T u, T e) {
    T total = m + big_m;
    return {(m - e * big_m) * u / total, (T(1) + e) * m * u / total};
}

// The same algebra divided through by M first. Only the ratio r = m / M is used,
// and the limits r -> infinity (an unstoppable force) and r -> 0 are handled exactly.
template <typename T>
Speeds<T> stable(T m, T big_m, T u, T e) {
    T r = m / big_m;
    if (std::isinf(r)) {                    // m infinitely heavier than M: F barely notices O
        return {u, (T(1) + e) * u};
    }
    return {(r - e) * u / (T(1) + r), (T(1) + e) * u * r / (T(1) + r)};
}

}  // namespace speeds
