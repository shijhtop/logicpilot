# Reading a synthesis report

Read the synthesis report produced by the project directly. Extract headline
utilization and timing, then inspect the surrounding log for latch,
multi-driver, pruning, and constraint warnings.

## 1. Inference

- Any unintended latch usually means an incomplete combinational assignment.
- Check whether arrays mapped to the expected memory resource.
- Check whether multipliers mapped to DSP resources or general logic.
- Confirm extracted FSM count, state count, and encoding are plausible.

## 2. Optimized-away logic

Search for removed, pruned, unused, constant, and unreachable signals or
instances. Reconcile every surprising removal with design intent; it can reveal
disconnected outputs, tied-off inputs, or dead branches.

## 3. Utilization

- Compare LUT/FF/BRAM/DSP totals with the device or project budget.
- Use hierarchy reports to find the block responsible for unexpected growth.
- Review width expansion, replicated logic, `keep`/`dont_touch`, and arithmetic
  mapping before attempting broad optimization.

## 4. Timing estimate

Synthesis WNS/Fmax is an early estimate and requires valid clock constraints.
Negative WNS is actionable even if synthesis exits successfully. Name the tool,
clock, target period, and stage when reporting timing.

## Quick triage

- Failed run: report the first actionable error, fix the RTL/config cause, rerun.
- Missing tool/input: report the blocker and exact prerequisite.
- Successful run with warnings: resolve or explicitly waive each warning.
- Clean run: report inferred resources, utilization against budget, and any
  constrained timing estimate.
