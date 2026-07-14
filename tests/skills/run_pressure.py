#!/usr/bin/env python3
"""Manual pressure-test harness for LogicPilot skills.

The static layer (``test_skill_guards.py``) verifies that each scenario's
``guards`` strings still appear in the target ``SKILL.md``. That catches
silent drift but cannot verify the agent actually *uses* the guard under
pressure. This script is the manual half of that loop:

1. **RED**: paste the scenario prompt into a fresh agent session that
   does NOT have the target skill loaded. Confirm the baseline-failure-
   mode bullets actually happen.
2. **GREEN**: do it again with the skill loaded. Confirm the
   guarded-behavior bullets actually happen.
3. **REFACTOR**: if (1) does not fail or (2) does not pass, the skill is
   wrong — edit ``codex/skills/<target>/SKILL.md`` and re-run.

The script prints the scenario fields so a human can copy/paste them into
whichever agent harness is convenient.

Usage:

    python3 tests/skills/run_pressure.py tests/skills/scenarios/cdc-multibit-bus.md
    python3 tests/skills/run_pressure.py --list

This is intentionally low-tech: no PyYAML, no subprocess piping of API
keys, no implicit network calls. The goal is a portable harness any
contributor can run, not a closed evaluation rig.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from conftest import (  # noqa: E402  (import after sys.path tweak)
    SCENARIOS_DIR,
    Scenario,
    discover_scenarios,
    load_scenario,
)


def _scenario_body(scenario: Scenario) -> str:
    """Return the markdown body (everything after the YAML front matter)."""
    text = scenario.path.read_text(encoding="utf-8")
    _, _, after = text.partition("---\n")
    _, _, body = after.partition("---\n")
    return body.strip()


def _print_scenario(scenario: Scenario) -> None:
    body = _scenario_body(scenario)
    print()
    print(f"# {scenario.title}")
    print(f"  scenario: {scenario.name}")
    print(f"  target skill: {scenario.target_skill}")
    print(f"  guards ({len(scenario.guards)}):")
    for g in scenario.guards:
        print(f"    - {g!r}")
    if scenario.gate_text:
        print(f"  gate_text ({len(scenario.gate_text)}):")
        for g in scenario.gate_text:
            print(f"    - {g!r}")
    print()
    print("-" * 72)
    print(body)
    print("-" * 72)


def _list_scenarios() -> int:
    scenarios = discover_scenarios()
    if not scenarios:
        print(f"(no scenarios under {SCENARIOS_DIR})")
        return 1
    width = max(len(s.name) for s in scenarios)
    for s in scenarios:
        print(f"  {s.name:<{width}}  [{s.target_skill}]  {s.title}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Manual pressure-test harness for LogicPilot skills."
    )
    parser.add_argument(
        "scenario",
        nargs="?",
        help="path to a scenario file under scenarios/, or its bare name "
        "(e.g. 'cdc-multibit-bus').",
    )
    parser.add_argument(
        "--list", action="store_true", help="list all discovered scenarios"
    )
    args = parser.parse_args(argv)

    if args.list:
        return _list_scenarios()

    if not args.scenario:
        parser.print_help()
        return 0

    # Accept either a path or a bare scenario name.
    candidate = Path(args.scenario)
    if not candidate.exists():
        candidate = SCENARIOS_DIR / f"{args.scenario}.md"
    if not candidate.exists():
        print(f"error: scenario not found: {args.scenario}", file=sys.stderr)
        return 2

    scenario = load_scenario(candidate)
    _print_scenario(scenario)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
