// floats.exe: the paradox as the computer sees it.
// For m = M = a larger and larger number, compare the naive and stable formulas
// in float, double and long double.
#include <cstdio>
#include <limits>

#include "speeds.hpp"

namespace {

template <typename T>
void row(const char* type, T mass) {
    const T u = 1, e = 1;
    auto n = speeds::naive(mass, mass, u, e);
    auto s = speeds::stable(mass, mass, u, e);
    // %Lg prints a long double; every type is widened to it for printing only.
    std::printf("  %-12s m = M = %.3Le   naive v_O/u = %-5Lg   stable v_O/u = %Lg\n", type,
                static_cast<long double>(mass), static_cast<long double>(n.v_object),
                static_cast<long double>(s.v_object));
}

template <typename T>
void limits(const char* type) {
    std::printf("%-12s %2zu bytes, largest finite value %.3Le\n", type, sizeof(T),
                static_cast<long double>(std::numeric_limits<T>::max()));
}

}  // namespace

int main() {
    std::printf("How big can a number get?\n");
    limits<float>("float");
    limits<double>("double");
    limits<long double>("long double");

    std::printf("\nm = M = (largest value / 1.5): representable, but m + M overflows\n");
    row<float>("float", std::numeric_limits<float>::max() / 1.5f);
    row<double>("double", std::numeric_limits<double>::max() / 1.5);
    row<long double>("long double", std::numeric_limits<long double>::max() / 1.5L);

    std::printf("\nm = infinity, M = 1 (a truly unstoppable force)\n");
    const double inf = std::numeric_limits<double>::infinity();
    auto n = speeds::naive(inf, 1.0, 1.0, 1.0);
    auto s = speeds::stable(inf, 1.0, 1.0, 1.0);
    std::printf("  naive  v_F = %g, v_O = %g\n", n.v_force, n.v_object);
    std::printf("  stable v_F = %g, v_O = %g   (the force keeps going; the object flies off at 2u)\n",
                s.v_force, s.v_object);

    std::printf("\nm = M = infinity (unstoppable meets immovable)\n");
    auto both = speeds::naive(inf, inf, 1.0, 1.0);
    auto both_s = speeds::stable(inf, inf, 1.0, 1.0);
    std::printf("  naive v_O = %g, stable v_O = %g: inf/inf has no value. IEEE 754 agrees with the math.\n",
                both.v_object, both_s.v_object);
    return 0;
}
