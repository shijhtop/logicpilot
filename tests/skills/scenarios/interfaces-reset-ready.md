---
target_skill: hardware-rtl-design
scenario: interfaces-reset-ready
title: READY is unnecessarily forced low after reset
guards:
  - "only `valid` is universally required to be low after reset"
  - "`ready` follows the destination protocol and capacity"
  - "no transfer occurs while reset is active"
gate_text:
  - "Definition of done"
---

## Scenario prompt

> Our AXI-stream sink can accept data immediately after reset. Must READY stay
> low for an extra cycle because both sides of ready/valid must reset low?

## Baseline failure modes

- Treats READY-low as a universal ready/valid requirement.
- Adds an unnecessary bubble or assertion.

## Expected guarded behaviors

- Requires VALID to be low after reset.
- Allows READY to reflect destination capacity and the protocol contract.
- Ensures reset cannot produce a transfer or unstable payload.
