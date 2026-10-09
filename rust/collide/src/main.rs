//! `collide sweep [e]`   : CSV of collisions where both masses grow together (ratio kept)
//! `collide one m M u e` : one collision, printed as key=value lines
//!
//! Arguments are parsed by hand (no clap): there are only two commands.

use collide::{simulate, Setup};
use std::process::ExitCode;

const STIFFNESS: f64 = 1.0e6;

fn parse(text: &str, name: &str) -> Result<f64, String> {
    text.parse::<f64>()
        .map_err(|_| format!("{name}: '{text}' is not a number"))
}

fn sweep(e: f64) -> Result<(), String> {
    println!("ratio,M,v_force_over_u,v_object_over_u,peak_force,contact_time,momentum_error");
    for ratio in [0.001, 0.1, 1.0, 10.0, 1000.0] {
        for power in [0, 50, 100, 200] {
            let big_m = 10f64.powi(power);
            let s = Setup {
                m: ratio * big_m,
                big_m,
                u: 1.0,
                stiffness: STIFFNESS,
                restitution: e,
            };
            let o = simulate(&s).map_err(|err| err.to_string())?;
            println!(
                "{ratio},{big_m:e},{:.6},{:.6},{:.3e},{:.3e},{:.1e}",
                o.v_force, o.v_object, o.peak_force, o.contact_time, o.momentum_error
            );
        }
    }
    Ok(())
}

fn one(args: &[String]) -> Result<(), String> {
    if args.len() != 4 {
        return Err("usage: collide one <m> <M> <u> <e>".into());
    }
    let s = Setup {
        m: parse(&args[0], "m")?,
        big_m: parse(&args[1], "M")?,
        u: parse(&args[2], "u")?,
        stiffness: STIFFNESS,
        restitution: parse(&args[3], "e")?,
    };
    let o = simulate(&s).map_err(|err| err.to_string())?;
    println!(
        "v_force={}\nv_object={}\npeak_force={:e}\ncontact_time={:e}\nmomentum_error={:e}\n\
              effective_restitution={}\nsteps={}",
        o.v_force,
        o.v_object,
        o.peak_force,
        o.contact_time,
        o.momentum_error,
        o.effective_restitution,
        o.steps
    );
    Ok(())
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let result = match args.first().map(String::as_str) {
        Some("sweep") => args
            .get(1)
            .map_or(Ok(1.0), |t| parse(t, "e"))
            .and_then(sweep),
        Some("one") => one(&args[1..]),
        _ => Err("usage: collide sweep [e] | collide one <m> <M> <u> <e>".into()),
    };
    match result {
        Ok(()) => ExitCode::SUCCESS,
        Err(msg) => {
            eprintln!("collide: {msg}");
            ExitCode::from(2)
        }
    }
}
