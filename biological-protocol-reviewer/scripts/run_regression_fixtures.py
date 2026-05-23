#!/usr/bin/env python3
"""Run Biological Protocol Reviewer regression fixtures."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "regression_fixtures"


def run(cmd: list[str]) -> int:
    print("$ " + " ".join(cmd))
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def main() -> int:
    if not FIXTURES.exists():
        print(f"No regression fixtures found: {FIXTURES}")
        return 0
    failures = 0
    for path in sorted(FIXTURES.glob("*.json")):
        if path.name.startswith("handoff_"):
            failures += run([sys.executable, str(ROOT / "scripts" / "check_claim_readout_handoff.py"), str(path)])
        elif path.name.startswith("passport_"):
            failures += run([sys.executable, str(ROOT / "scripts" / "check_protocol_passport.py"), str(path)])
        elif path.name.startswith("protocol_review_"):
            failures += run([sys.executable, str(ROOT / "scripts" / "lint_structured_protocol.py"), str(path)])
        else:
            print(f"Skipping unrecognized fixture: {path.name}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
