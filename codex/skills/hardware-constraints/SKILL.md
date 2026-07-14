---
name: hardware-constraints
description: >-
  Author and review SDC/XDC timing constraints: primary and generated clocks, I/O delays, asynchronous clock groups, false paths, multicycle paths, and max/min delays. Use when timing or Fmax is missing or suspicious, or when a project has multiple clocks, clock enables, or CDC exceptions.
---

# Timing Constraints

A timing number is meaningful only when the clocks and path relationships are
correct. Write constraints alongside the RTL and review them before interpreting
synthesis timing.

## Minimum constraints

1. Define every primary clock:

   ```tcl
   create_clock -name clk -period 10.000 [get_ports clk]
   ```

2. Define generated clocks or use vendor-derived PLL constraints.
3. Add min/max input and output delays when chip-boundary timing matters.
4. Classify every clock-domain crossing with `hardware-cdc`, then declare the
   corresponding asynchronous relationship or bounded data path.
5. Add both setup and hold multicycle exceptions for paths that genuinely have
   multiple cycles (`hold = setup - 1`).

## Exception rules

- Use `set_clock_groups -asynchronous` only when every path between the selected
  clock groups is intentionally untimed by STA.
- Use narrow `set_false_path` exceptions for genuine asynchronous or static
  paths. Never false-path a synchronous violation to make a report green.
- Use scoped `set_max_delay`, `set_min_delay`, or bus-skew checks when a CDC
  protocol requires a bounded data path rather than a blanket false path.
- Give every exception a named architectural rationale and matching RTL pattern.
- Do not apply a blanket false path or asynchronous clock group to a path that
  must retain a bounded constraint unless the target tool proves the bound has
  higher precedence and remains active.

## Workflow

1. Inventory clocks, frequencies, generated relationships, and I/O contracts.
2. Review the CDC inventory and reset-release behavior.
3. Write or generate the SDC/XDC file.
4. Run the project's constraint and synthesis checks; inspect warnings and
   timing metrics.
5. Hand real negative slack with correct constraints to `hardware-synthesis`;
   fix constraint mistakes here.

See `references/sdc-cookbook.md` for exception selection and common commands and
`references/sdc-templates.md` for vendor syntax.

## Definition of done

Every clock is defined, I/O is constrained where required, multicycle
setup/hold pairs are complete, and each crossing has one matching,
non-conflicting timing strategy with an architectural reason. The target tool's
exception report confirms which paths remain timed, and the resulting timing
estimate names its tool and constraint set.
