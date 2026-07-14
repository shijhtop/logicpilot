# LogicPilot

> A Codex skills plugin for RTL/HDL design and review.

**License:** MIT

LogicPilot provides five independently triggered hardware skills. It does not
maintain a second build system: lint, simulation, formal verification, and
synthesis use the target repository's existing Makefile, scripts, project files,
or CI commands.

## Skills

| Skill | Purpose |
|---|---|
| `hardware-rtl-design` | RTL, handshake/bus interfaces, synthesizability, source audit |
| `hardware-cdc` | Clocks, resets, CDC/RDC, and crossing inventories |
| `hardware-constraints` | SDC/XDC clocks, I/O constraints, and timing exceptions |
| `hardware-verification` | Self-checking TBs, assertions, coverage, formal, regressions |
| `hardware-synthesis` | Synthesis reports, FPGA architecture, and timing iteration |

Each skill loads its full instructions only for relevant work. Project-specific
conventions belong in that project's own `AGENTS.md`, not in this plugin.

## Installation

Open Codex `/plugins`, choose **Add marketplace**, enter
`shijhtop/LogicPilot`, then install **LogicPilot**.

## Development

```bash
python3 -m pytest tests -q
```

中文版：[README.md](README.md)

## Disclaimer

LogicPilot assists engineering work; it does not replace engineering judgment.
Skill output is not CDC, timing, implementation, or tape-out
sign-off. A qualified engineer must review critical design and tool results.
