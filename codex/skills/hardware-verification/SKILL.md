---
name: hardware-verification
description: >-
  Plan and implement HDL verification with self-checking simulation, Verilog/SystemVerilog/VHDL testbenches, cocotb, assertions, SymbiYosys formal checks, constrained random stimulus, scoreboards, coverage, interfaces, clocking blocks, classes, and UVM-like components. Use when writing or debugging a testbench, waveform, simulator run, property, formal proof, coverage plan, or regression.
---

# Hardware Verification

A waveform is diagnostic evidence, not a regression. Map each requirement and
failure mode to stimulus, an automated checker or property, and needed coverage.

## Core workflow

- Use the repository's existing simulation/formal commands and the smallest
  self-checking environment that covers the risk.
- Exercise reset, boundaries, back-to-back traffic, stalls, errors, and recovery.
- Compare against expected values or a reference model; emit unambiguous failure
  and log replayable random seeds.
- Reproduce the first divergent cycle/property before analyzing later symptoms.
- Use waveforms to diagnose failed checks, never as the only checker.

## Assertions and formal

- Use temporal assertions for protocol rules and procedural assertions for local
  invariants; disable reset-sensitive properties explicitly.
- Prefer assertions for stable-while-valid, FIFO bounds, and legal FSM states;
  use scoreboards for end-to-end data correctness.
- State assumptions, properties, engine/depth, and result. A bounded proof is not
  an unbounded proof.

## Coverage

- Do not merge coverage from failing tests.
- Treat functional coverage as specification evidence and code coverage as a way
  to locate unexercised implementation.
- Close each meaningful hole or document why it is unreachable or waived.

Read the references when race avoidance, formal, coverage, or a larger
verification architecture is involved.

## Definition of done

Relevant requirements have automated checks, failures are reproducible, coverage
obligations are addressed, and exact commands, seeds, warnings, and results are
reported.
