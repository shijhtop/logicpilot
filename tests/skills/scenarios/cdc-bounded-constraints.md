---
target_skill: hardware-cdc
scenario: cdc-bounded-constraints
title: Bounded CDC data path hidden by a blanket clock-group exception
guards:
  - "matching, non-conflicting timing strategy"
  - "Do not combine a blanket asynchronous clock-group exception"
  - "bounded data path"
gate_text:
  - "Definition of done (MUST gate)"
---

## Scenario prompt

> My bundled-data handshake has a path-specific max-delay constraint. Should I
> also declare the two clocks asynchronous with set_clock_groups?

## Baseline failure modes

- Adds both exceptions without checking precedence.
- Allows a blanket false path to disable the bounded-data requirement.

## Expected guarded behaviors

- Classifies the crossing and selects one non-conflicting timing strategy.
- Preserves the path-specific bound instead of hiding it behind a blanket
  asynchronous clock-group exception.
- Hands exact tool syntax and precedence checks to `hardware-constraints`.
