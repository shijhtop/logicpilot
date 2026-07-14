---
name: hardware-synthesis
description: >-
  Synthesize RTL, interpret utilization and timing reports, and optimize FPGA RTL architecture. Use for elaboration, inferred RAM/DSP/FSM review, latches, multi-drivers, missing modules, optimized-away logic, LUT/FF/BRAM/DSP budgets, Fmax, WNS/TNS, critical paths, fanout, pipelining, resource sharing, or timing closure.
---

# Hardware Synthesis and FPGA Optimization

Use measured reports to confirm inferred hardware and improve speed or area
without silently changing latency, throughput, or behavior.

## Task modes

- **New run:** use the repository's existing flow after relevant self-checking
  verification.
- **For report-only review:** analyze supplied evidence without requiring the
  original environment. State missing context as a limitation.
- **Optimization:** change one issue class, then compare the same tool, settings,
  verification, and metric against the baseline.

Do not require a new synthesis run or measured improvement for report-only
review. Do not claim sign-off without the target, tool version, constraints, and
implementation stage.

Read `references/report-reading.md` for report interpretation and
`references/timing-area-playbook.md` for optimization patterns.

## Report checks

- Confirm inferred RAM/DSP/FSM structures and reconcile optimized-away logic.
- Treat latches, multiple drivers, combinational loops, and unconstrained clocks
  as failures even when synthesis exits successfully.
- Report LUT/FF/BRAM/DSP and WNS/TNS/Fmax only when present, naming tool, target,
  constraints, and implementation stage.
- Treat pre-route timing as an estimate, not implementation sign-off.

## Optimization order

1. Correct clocks, I/O constraints, CDC exceptions, and multicycle paths.
2. Pipeline deep paths and align valid/control latency.
3. Balance trees and remove accidental priority depth.
4. Address measured fanout/routing and target-specific RAM/DSP/SRL inference.
5. Right-size or share resources only when throughput permits.

State evidence and expected latency/area/throughput impact before editing.

## Definition of done

- **Report review:** explain actionable findings and evidence limitations.
- **New run:** inferred hardware matches intent and constrained metrics are valid.
- **Optimization:** measured improvement and the same verification still pass.
