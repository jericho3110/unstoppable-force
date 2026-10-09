"""Every check, one exit code:  python main.py check [python rust cpp security links]

Commits only happen when this exits 0 (gitship runs it from .gitship.json).
The security scan and link check come from the shared `devtools` package
(mr-factory-workspace, packages/devtools); install it once with
`pip install -e <workspace>/packages/gitship -e <workspace>/packages/devtools`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "UnstoppableForce"
EXE = ".exe" if os.name == "nt" else ""
WARN = ["-Wall", "-Wextra", "-Werror"]

CHECKS: dict[str, tuple[str, list[list[str]]]] = {
    "python": ("python", [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."]]),
    "rust": ("rust/collide", [
        ["cargo", "fmt", "--check"],
        ["cargo", "clippy", "--release", "--all-targets", "--", "-D", "warnings"],
        ["cargo", "test", "--release", "--quiet"],
    ]),
    "cpp": ("cpp/floats", [
        ["clang++", "-std=c++20", *WARN, "-Iinclude", "tests/test_speeds.cpp", "-o", str(BUILD / "build" / f"test_speeds{EXE}")],
        [str(BUILD / "build" / f"test_speeds{EXE}")],
        ["clang++", "-std=c++20", *WARN, "-O2", "-Iinclude", "src/main.cpp", "-o", str(BUILD / "build" / f"floats{EXE}")],
    ]),
    "security": (".", [["devtools", "scan"]]),
    "links": (".", [["devtools", "links", "--offline"]]),
}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    selected = sys.argv[1:] or list(CHECKS)
    unknown = [s for s in selected if s not in CHECKS]
    if unknown:
        print(f"unknown check(s) {unknown}; choose from {list(CHECKS)}")
        return 2
    (BUILD / "build").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, CARGO_TARGET_DIR=str(BUILD / "cargo-target"))
    env["PATH"] = os.pathsep.join([r"C:\Program Files\LLVM\bin", str(Path.home() / ".cargo" / "bin"), env["PATH"]])
    failed = []
    for name in selected:
        folder, commands = CHECKS[name]
        print(f"== {name}", flush=True)
        for argv in commands:
            program = shutil.which(argv[0], path=env["PATH"]) or argv[0]
            try:
                p = subprocess.run([program, *argv[1:]], cwd=ROOT / folder, env=env,  # noqa: S603
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
            except FileNotFoundError:
                print(f"   {argv[0]} not found: see README Setup")
                failed.append(name)
                break
            if p.returncode != 0:
                print((p.stdout + p.stderr)[-3000:])
                failed.append(name)
                break
        print(f"   {'FAIL' if name in failed else 'PASS'}", flush=True)
    print("\n" + "  ".join(f"{n}:{'FAIL' if n in failed else 'ok'}" for n in selected))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
