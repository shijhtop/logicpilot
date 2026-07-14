---
target_skill: hardware-synthesis
scenario: synthesis-report-review
title: Review an existing report without rerunning synthesis
guards:
  - "For report-only review"
  - "Do not require a new synthesis run or measured improvement"
  - "State missing context as a limitation"
gate_text:
  - "Definition of done"
---

## Scenario prompt

> I only have a synthesis report from another machine. Explain its utilization
> and timing warnings; do not modify RTL or rerun the build.

## Baseline failure modes

- Refuses to review until a self-checking simulation and new synthesis run exist.
- Claims an optimization improvement even though no change was requested.

## Expected guarded behaviors

- Reviews the supplied evidence and names missing target, constraints, or tool
  context as limitations.
- Does not require a new run or measured improvement for a report-only task.
- Avoids proposing RTL edits unless the user asks for optimization.
