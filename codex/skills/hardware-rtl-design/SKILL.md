---
name: hardware-rtl-design
description: >-
  Design, edit, review, and audit synthesizable Verilog, SystemVerilog, or VHDL and on-chip interfaces. Use for RTL modules, FSMs, pipelines, memories, arithmetic, latches, width/sign issues, blocking versus nonblocking assignments, valid/ready handshakes, AXI/APB/AHB/Avalon/Wishbone, register maps, backpressure, or simulation/synthesis mismatches.
---

# Hardware RTL Design and Audit

Treat HDL as hardware structure and preserve the stated clocks, reset, latency,
throughput, protocol, widths, and target assumptions.

## Workflow

1. Inspect the contract, RTL, tests, constraints, local instructions, and existing
   tool commands.
2. Define a tool-verifiable success criterion before editing.
3. Make a surgical change without restyling adjacent RTL.
4. Run the relevant existing lint, elaboration, simulation, and synthesis checks;
   read warnings and metrics, not only the return code.
5. Audit changed source with parser-based tools and `references/audit-rules.md`.

## RTL rules

- Use one driver per signal, nonblocking assignments in sequential logic, and
  blocking assignments in combinational logic.
- Assign combinational outputs and next-state values on every path.
- Size values explicitly and review signedness, truncation, extension, packed
  dimensions, and arithmetic growth.
- Keep delays, waits, classes, randomization, DPI, and simulation system tasks
  out of synthesizable RTL.
- Prefer clock enables to hand-built gated clocks. Reset visible control state,
  not wide data or memories solely for cosmetic simulation values.
- Check latches, incomplete cases, multiple drivers, implicit nets, compile-order
  dependencies, testbench constructs in RTL, and CDC/RDC handoffs.

## Interface rules

- A valid/ready source must not wait for `ready` before asserting `valid`.
- Hold `valid` and payload stable until transfer; propagate backpressure without
  dropping or duplicating data and avoid combinational ready/valid loops.
- On reset, only `valid` is universally required to be low after reset.
  `ready` follows the destination protocol and capacity.
  Ensure no transfer occurs while reset is active and no unstable payload is
  accepted on release.
- Follow the named protocol's ordering, response, and reset requirements rather
  than treating every bus as generic valid/ready.

## Specialized handoffs

Use `hardware-cdc` for clock/reset crossings, `hardware-constraints` for timing
exceptions, `hardware-verification` for assertions and tests, and
`hardware-synthesis` for utilization or timing optimization.

## Definition of done (MUST gate)

Before declaring the RTL task complete, you MUST verify:

- [ ] Assumptions and the tool-verifiable success criterion are explicit.
- [ ] The diff is surgical and relevant checks, warnings, and metrics were read.
- [ ] Audit findings and applicable interface/reset/backpressure rules are resolved.
- [ ] Required CDC, constraint, verification, or synthesis handoffs are complete.

An exit code 0 is not verification. Unresolved warnings, negative slack, missing
checks, or an untested contract change mean the task is not done.
