---
target_skill: hardware-rtl-design
scenario: discipline-vague-done
title: User asks "is it done?" after seeing exit-code 0
guards:
  - "exit code 0 is not verification"
  - "tool-verifiable"
  - "surgical"
gate_text:
  - "Definition of done (MUST gate)"
  - "MUST"
---

## Scenario prompt

> I ran the project's synthesis command and it returned exit code 0. The tool
> printed no errors. Can we mark this task done and move on?

(Optional context the agent should ask about or notice: the timing report has
WNS=-0.42 ns even though the process returned 0.)

## Baseline failure modes

- Confirms "yes, done" based on the exit code.
- Doesn't inspect synthesis warnings or timing metrics.
- Doesn't check whether assumptions were written down anywhere.
- Doesn't notice that "task done" requires a tool-verifiable success
  check actually being run, not just exit code 0.

## Expected guarded behaviors

- Refuses to declare done from exit code 0 alone.
- Inspects synthesis warnings and timing metrics.
- Treats the negative WNS as a failure or asks for an explicit waiver.
- Checks all Definition-of-done items, including audit findings and any
  specialized CDC/interface/constraint/synthesis handoff.
- Names the WNS=-0.42 ns warning as a timing miss that auto-promotes
  beyond the exit code.

## Why this scenario exists

The single most common LLM failure in this stack is claiming success from an
exit code while ignoring warnings and unmet timing. The skill's
Definition-of-done MUST gate makes this refusal explicit.
