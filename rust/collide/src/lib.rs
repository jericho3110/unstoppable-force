//! A head-on collision simulated step by step.
//!
//! The formulas (see python/paradox/collision.py) jump straight from "before"
//! to "after". Up close, real bodies squash into each other for a short time.
//! Here the contact is a spring (stiffness `k`) with a damper (which turns
//! some energy into heat, setting the restitution `e`). Every time step:
//!
//! ```text
//! overlap  δ  = x_F - x_O            (how far they've pressed into each other)
//! force    f  = k·δ + c·(v_F - v_O)  (spring + damper, never pulling: f ≥ 0)
//! velocity v += (force / mass) · dt  (F pushed back, O pushed forward)
//! position x += v · dt               (semi-implicit Euler: new v, then x)
//! ```
//!
//! What this adds to the paradox: the peak contact force is about
//! `u·sqrt(k·μ)`, where `μ = m·M/(m+M)` is the "reduced mass". If both bodies
//! become infinitely heavy, μ → ∞, so the force between them → ∞. Whatever
//! they are made of breaks first.

/// One collision to simulate.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Setup {
    /// Mass of the "unstoppable" force F.
    pub m: f64,
    /// Mass of the "immovable" object O (at rest before the hit).
    pub big_m: f64,
    /// F's speed toward O.
    pub u: f64,
    /// Contact spring stiffness (force per unit of overlap).
    pub stiffness: f64,
    /// Restitution: 1 = perfectly bouncy, 0 = no bounce.
    pub restitution: f64,
}

/// What came out.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Outcome {
    pub v_force: f64,
    pub v_object: f64,
    pub peak_force: f64,
    pub contact_time: f64,
    /// |momentum after - momentum before| / |momentum before|: should be tiny.
    pub momentum_error: f64,
    /// The bounce actually achieved: (v_O - v_F) / u. A little above the
    /// requested `restitution` when damping is on: see `damping_ratio`.
    pub effective_restitution: f64,
    pub steps: u64,
}

/// Why a setup was refused.
#[derive(Debug, PartialEq)]
pub enum SimError {
    NotPositive(&'static str),
    BadRestitution,
    DidNotSeparate,
}

impl std::fmt::Display for SimError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SimError::NotPositive(what) => write!(f, "{what} must be a positive, finite number"),
            SimError::BadRestitution => write!(f, "restitution must be between 0 and 1"),
            SimError::DidNotSeparate => {
                write!(f, "the bodies did not separate within the step limit")
            }
        }
    }
}

impl std::error::Error for SimError {}

/// μ = m·M/(m+M), written to avoid overflowing m·M for huge masses.
pub fn reduced_mass(m: f64, big_m: f64) -> f64 {
    m / (1.0 + m / big_m)
}

/// Damping ratio ζ that makes a spring-damper contact bounce back with restitution `e`.
///
/// For a linear spring-damper, e = exp(-ζπ/√(1-ζ²)). Solving for ζ gives
/// ζ = -ln e / √(π² + ln² e). At e = 0 that formula is undefined, and
/// ζ = 1 (critical damping: no rebound) is used.
///
/// Found by the tests: that formula assumes the contact may also PULL at the
/// end of the half-cycle. A real contact can't (the force is clamped at 0), so
/// the bodies part a little earlier and bounce a little more (asking for
/// e = 0.5 gives about 0.55), and even e = 0 (critical damping) rebounds at
/// about 0.135: a spring-damper contact cannot be perfectly sticky.
/// `Outcome::effective_restitution` reports the real value.
pub fn damping_ratio(e: f64) -> f64 {
    if e <= 0.0 {
        return 1.0;
    }
    let ln_e = e.ln();
    -ln_e / (std::f64::consts::PI.powi(2) + ln_e * ln_e).sqrt()
}

const STEPS_PER_CONTACT: f64 = 4000.0;
const MAX_STEPS: u64 = 1_000_000;

pub fn simulate(s: &Setup) -> Result<Outcome, SimError> {
    for (value, name) in [
        (s.m, "m"),
        (s.big_m, "M"),
        (s.u, "u"),
        (s.stiffness, "stiffness"),
    ] {
        if !(value.is_finite() && value > 0.0) {
            return Err(SimError::NotPositive(name));
        }
    }
    if !(0.0..=1.0).contains(&s.restitution) {
        return Err(SimError::BadRestitution);
    }

    let mu = reduced_mass(s.m, s.big_m);
    let omega = (s.stiffness / mu).sqrt(); // natural frequency of the contact spring
    let zeta = damping_ratio(s.restitution);
    let damping = 2.0 * zeta * (s.stiffness * mu).sqrt();
    let dt = std::f64::consts::PI / omega / STEPS_PER_CONTACT; // time step: a sliver of one contact

    // Start touching (overlap 0); F moving at u, O at rest.
    let (mut x_f, mut x_o) = (0.0_f64, 0.0_f64);
    let (mut v_f, mut v_o) = (s.u, 0.0_f64);
    let momentum_before = s.m * s.u;
    let (mut peak, mut contact_time, mut steps) = (0.0_f64, 0.0_f64, 0_u64);

    loop {
        let overlap = x_f - x_o;
        let closing = v_f - v_o;
        if steps > 0 && overlap <= 0.0 && closing <= 0.0 {
            break; // apart, and moving apart: the collision is over
        }
        if steps >= MAX_STEPS {
            return Err(SimError::DidNotSeparate);
        }
        let force = if overlap > 0.0 {
            (s.stiffness * overlap + damping * closing).max(0.0) // a contact can push, never pull
        } else {
            0.0
        };
        peak = peak.max(force);
        if force > 0.0 {
            contact_time += dt;
        }
        // Equal and opposite (Newton's third law): this is why momentum is conserved.
        v_f -= force / s.m * dt;
        v_o += force / s.big_m * dt;
        x_f += v_f * dt;
        x_o += v_o * dt;
        steps += 1;
    }

    let momentum_after = s.m * v_f + s.big_m * v_o;
    Ok(Outcome {
        v_force: v_f,
        v_object: v_o,
        peak_force: peak,
        contact_time,
        momentum_error: ((momentum_after - momentum_before) / momentum_before).abs(),
        effective_restitution: (v_o - v_f) / s.u,
        steps,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn setup(m: f64, big_m: f64, e: f64) -> Setup {
        Setup {
            m,
            big_m,
            u: 1.0,
            stiffness: 1.0e6,
            restitution: e,
        }
    }

    fn close(a: f64, b: f64, rel: f64) -> bool {
        (a - b).abs() <= rel * a.abs().max(b.abs()).max(1e-12)
    }

    #[test]
    fn elastic_matches_the_exact_formula() {
        for (m, big_m) in [(1.0, 1.0), (1.0, 3.0), (5.0, 1.0)] {
            let out = simulate(&setup(m, big_m, 1.0)).unwrap();
            let exact_o = 2.0 * m / (m + big_m);
            let exact_f = (m - big_m) / (m + big_m);
            assert!(close(out.v_object, exact_o, 2e-3), "{out:?} vs {exact_o}");
            assert!((out.v_force - exact_f).abs() < 2e-3, "{out:?} vs {exact_f}");
        }
    }

    #[test]
    fn momentum_is_conserved_to_rounding() {
        for e in [0.0, 0.5, 1.0] {
            assert!(simulate(&setup(2.0, 7.0, e)).unwrap().momentum_error < 1e-9);
        }
    }

    #[test]
    fn restitution_sets_the_separation_speed_slightly_high_because_contacts_cannot_pull() {
        let out = simulate(&setup(1.0, 1.0, 0.5)).unwrap();
        assert!(close(
            out.effective_restitution,
            out.v_object - out.v_force,
            1e-12
        ));
        // Requested 0.5; the no-pull clamp ends contact early, so the bounce is a bit livelier.
        assert!((0.5..0.6).contains(&out.effective_restitution), "{out:?}");
        // Undamped (e = 1) is exact.
        assert!(close(
            simulate(&setup(1.0, 1.0, 1.0))
                .unwrap()
                .effective_restitution,
            1.0,
            2e-3
        ));
        // Found by this test: even critical damping (the e = 0 setting) rebounds at about
        // 0.135 (≈ e^-2). A spring-damper contact cannot be perfectly sticky.
        let sticky = simulate(&setup(1.0, 1.0, 0.0))
            .unwrap()
            .effective_restitution;
        assert!((0.13..0.14).contains(&sticky), "{sticky}");
    }

    #[test]
    fn peak_force_follows_u_sqrt_k_mu() {
        let s = setup(4.0, 4.0, 1.0);
        let expected = s.u * (s.stiffness * reduced_mass(s.m, s.big_m)).sqrt();
        assert!(close(simulate(&s).unwrap().peak_force, expected, 1e-2));
    }

    #[test]
    fn only_the_mass_ratio_sets_the_speeds() {
        let small = simulate(&setup(2.0, 1.0, 1.0)).unwrap();
        let huge = simulate(&setup(2.0e200, 1.0e200, 1.0)).unwrap();
        assert!(close(small.v_object, huge.v_object, 1e-9));
        assert!(huge.peak_force > small.peak_force * 1e90); // but the force between them explodes
    }

    #[test]
    fn bad_inputs_are_refused() {
        assert_eq!(
            simulate(&setup(0.0, 1.0, 1.0)),
            Err(SimError::NotPositive("m"))
        );
        assert_eq!(
            simulate(&setup(1.0, f64::INFINITY, 1.0)),
            Err(SimError::NotPositive("M"))
        );
        assert_eq!(
            simulate(&setup(1.0, 1.0, 1.5)),
            Err(SimError::BadRestitution)
        );
    }

    #[test]
    fn reduced_mass_does_not_overflow() {
        assert!(close(reduced_mass(1e300, 1e300), 5e299, 1e-12));
    }
}
