# SDC / XDC templates — pasteable snippets

Vendor-oriented snippets for the constraints that go wrong most often.
The examples cover generic SDC, Xilinx Vivado XDC, and Intel Quartus SDC.
The semantics are the same; the syntax has small but real differences.

When two cells look identical, they ARE identical for that pattern.
When they differ, the difference is real — don't copy the wrong one.

## 1. Primary clock

```tcl
# open / Quartus / Vivado — same syntax
create_clock -name clk_sys -period 10.000 [get_ports clk_sys]   ;# 100 MHz
```

For multiple primary clocks driven by separate pins, repeat per clock.

## 2. PLL / generated clock

| | Syntax |
|---|---|
| **Open / Vivado** | `create_generated_clock -name clk_div2 -source [get_pins div_reg/Q] -divide_by 2 [get_pins div_reg/Q]` |
| **Intel (Quartus)** | `derive_pll_clocks` — auto-generates names; OR `create_generated_clock -name pll_out0 -source [get_pins pll_inst/refclk] -multiply_by 4 -divide_by 1 [get_pins pll_inst/outclk0]` |

`derive_pll_clocks` is Intel-only. If you want repeatable cross-vendor
constraints, write the `create_generated_clock` lines explicitly.

## 3. I/O delay (board timing)

```tcl
# All three vendors — same syntax. Min/max for setup+hold realism.
set_input_delay  -clock clk_sys -max 4.0 [get_ports data_in]
set_input_delay  -clock clk_sys -min 1.0 [get_ports data_in]
set_output_delay -clock clk_sys -max 3.0 [get_ports data_out]
set_output_delay -clock clk_sys -min 0.5 [get_ports data_out]
```

For source-synchronous interfaces (DDR, SPI), constrain against the
forwarded clock, not the system clock. Use `-clock_fall` for double-edge
transfers.

## 4. Async clock-group declaration (CDC sign-off)

```tcl
# All three vendors — same syntax.
# Use only when every path between the groups is intentionally untimed.
# Do not use this blanket exception for a bounded CDC data path.
set_clock_groups -asynchronous \
    -group {clk_a clk_a_div2} \
    -group {clk_b}
```

Group together every clock that is **synchronous to each other** (a
clock and its divider are one group). Different groups are async.

## 5. CDC data path — bound the skew

```tcl
# All three vendors — same syntax.
# Preserve the protocol's physical delay/skew assumption. Derive the
# bound from the source stability contract and target tool semantics.
set_max_delay <BOUND_NS> \
    -from [get_cells {src_dom/data_reg[*]}] \
    -to   [get_cells dst_dom/u_sync/rff1]
```

Use this for "MCP formulation" (data held stable on the source side,
enable synchronized) crossings. Add the target tool's bus-skew constraint for
Gray-coded or coherency-sensitive buses, and verify both constraints in its
exception/skew reports.

## 6. False path (for genuinely async, not "to silence")

```tcl
# Reset synchronizer async-assert side (release path stays timed).
set_false_path -to [get_pins reset_sync_*/rff1/CLR]    ;# open / Vivado
set_false_path -to [get_pins reset_sync_*/rff1/CLRN]   ;# Intel — pin name differs by library
```

```tcl
# Static config bits set once before clocks start.
set_false_path -through [get_pins cfg_reg/Q]
```

**Don't** false-path a real synchronous path to silence a warning. Every
false path needs an architectural reason.

## 7. Multicycle path (clock-enable / slow data)

```tcl
# All three vendors — same syntax.
# Path runs every Nth cycle (clock enable, slow handshake). Hold MUST be
# adjusted to N-1; setup-only multicycle is a common sign-off bug.
set_multicycle_path 4 -setup -from [get_cells slow_src_reg] -to [get_cells slow_dst_reg]
set_multicycle_path 3 -hold  -from [get_cells slow_src_reg] -to [get_cells slow_dst_reg]
```

For an N-cycle setup multicycle, hold = N - 1. Always write both.

## Common mistakes to scan for

| Mistake | Symptom | Fix |
|---|---|---|
| Forgot `create_clock` | Tool reports "no clock" → no timing → `fmax_mhz` missing | Always start with `create_clock` for every primary clock |
| Blanket `set_clock_groups` plus a bounded path on the same clock pair | Bound may be disabled by exception precedence | Use one matching strategy per path and inspect the exception report |
| `set_max_delay` without `-from` / `-to` | Applies to wrong paths or to all of them | Always scope with `-from` and `-to` |
| Setup-only multicycle | Hold violation in silicon | Add `-hold N-1` alongside `-setup N` |
| Wildcard `set_false_path -from * -to *` | "Closes" timing by ignoring real bugs | Each false path needs a named architectural reason |
| `derive_pll_clocks` in non-Intel flow | Tool error or silent no-op | Use explicit `create_generated_clock` |

For tool-level violation waivers, read `references/cdc-tool-waiver.md` in the
`hardware-cdc` skill.
