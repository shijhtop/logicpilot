---
target_skill: hardware-cdc
scenario: cdc-single-async-reset
title: Single-clock design with an asynchronously released reset
guards:
  - "any reset that can deassert asynchronously to its destination clock"
  - "Single-clock designs are exempt only when"
  - "Reset release is reviewed even in a single clock domain"
gate_text:
  - "When this skill is mandatory (MUST gate)"
  - "Definition of done (MUST gate)"
---

## Scenario prompt

> This block has one clock and one external asynchronous reset. Since there is
> no clock crossing, can we skip CDC/RDC review and use the reset directly?

## Baseline failure modes

- Exempts the block solely because it has one clock and one reset.
- Ignores recovery/removal risk when the external reset deasserts near a clock edge.
- Does not require synchronous reset release in the destination domain.

## Expected guarded behaviors

- Applies the reset-release portion of the CDC/RDC review despite there being
  only one clock domain.
- Requires asynchronous assertion and synchronous deassertion, or a documented
  project-specific alternative with timing evidence.
- Exempts only a reset that is synchronous or already synchronously released.
