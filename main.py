"""The front door: one command for everything.

    python main.py math paths            Python: exact answers along different routes to infinity
    python main.py math iterated         Python: the two iterated limits
    python main.py math proof            Python: why both objects can't exist together
    python main.py simulate [e]          Rust: step-by-step collisions, CSV
    python main.py floats                C++: what float/double do at huge numbers
    python main.py report                all three, into out/report.md + out/paradox.svg
    python main.py check [name ...]      every test, lint, build and the security/link checks

Compiled programs are built outside the repo and outside OneDrive, under
%LOCALAPPDATA%\\UnstoppableForce (Rust's target dir and the C++ build dir).
"""

from __future__ import annotations

import os
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_ROOT = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "UnstoppableForce"
CARGO_TARGET = BUILD_ROOT / "cargo-target"
CPP_BUILD = BUILD_ROOT / "build"
EXE = ".exe" if os.name == "nt" else ""
TOOL_DIRS = [r"C:\Program Files\LLVM\bin", str(Path.home() / ".cargo" / "bin")]


def env() -> dict[str, str]:
    e = dict(os.environ, CARGO_TARGET_DIR=str(CARGO_TARGET))
    e["PATH"] = os.pathsep.join([*[d for d in TOOL_DIRS if Path(d).is_dir()], e.get("PATH", "")])
    return e


def run(argv: list[str], cwd: Path, capture: bool = False) -> str:
    """Run a program (argument list, no shell). Raise on failure."""
    program = shutil.which(argv[0], path=env()["PATH"]) or argv[0]
    result = subprocess.run([program, *argv[1:]], cwd=cwd, env=env(), check=True,  # noqa: S603
                            capture_output=capture, text=True, encoding="utf-8", errors="replace")
    return result.stdout if capture else ""


def rust_binary() -> Path:
    run(["cargo", "build", "--release", "--quiet"], ROOT / "rust" / "collide")
    return CARGO_TARGET / "release" / f"collide{EXE}"


def cpp_binary() -> Path:
    CPP_BUILD.mkdir(parents=True, exist_ok=True)
    out = CPP_BUILD / f"floats{EXE}"
    run(["clang++", "-std=c++20", "-O2", "-Wall", "-Wextra", "-Werror", "-Iinclude", "src/main.cpp", "-o", str(out)],
        ROOT / "cpp" / "floats")
    return out


def python_cli(args: list[str], capture: bool = False) -> str:
    sys.path.insert(0, str(ROOT / "python"))
    from paradox.cli import main as paradox_main

    if not capture:
        paradox_main(args)
        return ""
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        paradox_main(args)
    return buf.getvalue()


def report() -> None:
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    python_cli(["plot", str(out / "paradox.svg")], capture=True)
    sections = [
        "# Unstoppable force vs immovable object: report\n",
        "![v_O/u against the mass ratio](paradox.svg)\n",
        "## 1. Exact math (Python)\n", "```text", python_cli(["paths"], True), python_cli(["iterated"], True),
        python_cli(["proof"], True), "```\n",
        "## 2. Simulation (Rust)\n", "```text", run([str(rust_binary()), "sweep"], ROOT, capture=True), "```\n",
        "## 3. The computer's limits (C++)\n", "```text", run([str(cpp_binary())], ROOT, capture=True), "```\n",
    ]
    (out / "report.md").write_text("\n".join(sections), encoding="utf-8")
    print(f"wrote {out / 'report.md'} and {out / 'paradox.svg'}")


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    try:
        if cmd == "math":
            return python_cli(rest) or 0
        if cmd == "simulate":
            run([str(rust_binary()), "sweep", *rest], ROOT)
        elif cmd == "floats":
            run([str(cpp_binary())], ROOT)
        elif cmd == "report":
            report()
        elif cmd == "check":
            sys.argv = [str(ROOT / "tools" / "check_all.py"), *rest]
            runpy.run_path(sys.argv[0], run_name="__main__")
        else:
            print(f"unknown command {cmd!r}\n{__doc__}")
            return 2
    except subprocess.CalledProcessError as e:
        print(f"failed: {' '.join(map(str, e.cmd))} (exit {e.returncode})", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"missing tool: {e}. See README Setup.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
