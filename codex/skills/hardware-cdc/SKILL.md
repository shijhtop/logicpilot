---
name: hardware-cdc
description: >-
  Review clock-domain and reset-domain crossings (CDC/RDC) in RTL. Use for multi-clock designs, resets that assert or release asynchronously, metastability, synchronizers, async FIFOs, Gray code, cross-domain handshakes, or any signal written in one clock/reset domain and read in another.
---

# Clock- and Reset-Domain Crossing Review

Plain RTL simulation does not model metastability. STA can analyze defined
inter-clock paths, but it does not prove that an asynchronous protocol, reset
release, or multi-bit transfer is coherent. Review CDC/RDC structurally and use
a dedicated CDC tool or formal flow when the project provides one.

## When this skill is mandatory (MUST gate)

Invoke this skill and satisfy its Definition of done when a design has:

- two or more unrelated or asynchronous clocks;
- any reset that can deassert asynchronously to its destination clock; or
- any signal written in one clock/reset domain and read in another.

Single-clock designs are exempt only when every reset is synchronous or already
has a proven synchronous release in that clock domain.
Reset release is reviewed even in a single clock domain.

There is no "obviously safe" multi-bit crossing. Review it structurally or
record a written waiver with evidence.

## Workflow

1. Enumerate clocks and reset sources. Group sequential state by its destination
   `(clock, reset)` domain.
2. Find every signal written in one domain and read in another, including reset
   release and status/control feedback.
3. Classify each crossing as single bit, pulse, bus, handshake, FIFO pointer, or
   reset release.
4. Match the crossing to a synchronizer pattern. Read
   `references/cdc-rdc-reference.md` and, for FIFOs,
   `references/async-fifo-patterns.md`.
5. Give every crossing a safe, unsafe, or needs-waiver verdict with evidence.
6. Hand timing-exception selection to `hardware-constraints` and verify the
   final exception report from the target tool.

## Reset architecture

- Follow the project's reset convention. When none exists, prefer asynchronous
  assertion with synchronous deassertion for external or power-on resets.
- **Assert async, deassert sync.** Each destination clock owns its reset
  synchronizer; share the raw reset source, not a synchronized reset output.
- Do not drive asynchronous reset pins from combinational logic. Register reset
  sequencing in the destination domain.
- Reset architecturally visible state, valid bits, interface outputs, and
  pointers. Avoid resetting wide data pipelines or memories when valid state
  already masks them.
- Preserve recovery/removal checks on release. Scope any exception to the
  asynchronous assertion path and verify tool-specific precedence.

See `references/reset-patterns.md` for reset synchronizer and sequencing
patterns.

## Structural boundaries

Prefer one functional clock per leaf module because it makes domain ownership
and constraints easier to inspect. A documented CDC primitive, protocol bridge,
multi-clock IP wrapper, or subsystem boundary may legitimately contain multiple
clocks. Do not split a valid boundary merely to satisfy hierarchy style; require
all crossings inside it to remain explicit and reviewable.

## Hazards to check

- No synchronizer on a cross-domain signal that feeds destination logic.
- Multi-bit bus through **parallel** 2-FF chains. Use an async FIFO, Gray-coded
  counter, or req/ack protocol with held data.
- Reconvergence before synchronization, or separate synchronizers whose outputs
  must be coherent in the same destination cycle.
- Combinational logic between the asynchronous source and the first
  synchronizer stage.
- A pulse that can be shorter than the destination's guaranteed observation
  window. Stretch it with a proven clock/uncertainty margin or use a closed-loop
  handshake/toggle protocol.
- Reset-domain crossing from state reset by source A into active state reset by
  source B.
- Generated, divided, ripple, or gated clocks that are not represented in the
  domain inventory and constraints.

## Timing-strategy handoff

Each crossing needs a matching, non-conflicting timing strategy. Typical choices
include an asynchronous clock-group or narrow false-path exception for truly
untimed paths, a path-specific max-delay/bus-skew constraint for a bounded data path,
and setup/hold multicycle constraints for a genuinely synchronous
clock-enable path.

Do not combine a blanket asynchronous clock-group exception with a bounded data
path constraint on the same path unless the target tool's documented precedence
and exception report prove that the bound remains active. `set_multicycle_path`
is not a generic CDC primitive. Read the timing-exception section in
`hardware-constraints` before writing tool syntax.

For CDC-tool waiver files, read `references/cdc-tool-waiver.md`.

## Multi-bit data and async FIFOs

- Keep binary read/write pointers local to their domains.
- Register Gray-coded pointers before synchronizing them across domains.
- Constrain inter-bit skew so the destination cannot observe transitions from
  multiple source increments as a mixed code word.
- Derive full/empty from the local pointer and synchronized opposite pointer.
- Write memory only in the write domain and read it only in the read domain.
- Use FIFO flags only in the domain that generates them.

## Definition of done (MUST gate)

Before declaring a CDC/RDC task complete, verify all of the following:

- [ ] A crossing inventory lists every crossing, source/destination domain, and
      crossing class.
- [ ] Every crossing has a safe, unsafe, or explicitly waived verdict.
- [ ] No multi-bit bus uses parallel 2-FF chains.
- [ ] Reset deassertion is synchronized per domain. Reset release is reviewed
      even in a single clock domain.
- [ ] Every crossing uses a matching, non-conflicting timing strategy, and the
      target tool's exception report confirms the intended paths remain checked.

Output the crossing inventory and verdicts. A clean simulation, synthesis, or
STA exit code alone does not satisfy this gate.
