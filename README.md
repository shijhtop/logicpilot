# LogicPilot

> 面向 RTL/HDL 设计与审查的 Codex skills 插件。

**License:** MIT

LogicPilot 提供 5 个可独立触发的硬件 skills。插件不维护第二套构建系统：
Lint、仿真、形式验证和综合直接使用目标仓库已有的 Makefile、脚本、工程
文件或 CI 命令。

## Skills

| Skill | 用途 |
|---|---|
| `hardware-rtl-design` | RTL、握手/总线接口、可综合规则与源码审查 |
| `hardware-cdc` | 时钟、复位、CDC/RDC 与 crossing inventory |
| `hardware-constraints` | SDC/XDC 时钟、I/O 与时序例外 |
| `hardware-verification` | 自检 TB、断言、覆盖率、形式验证与回归 |
| `hardware-synthesis` | 综合报告、FPGA 架构优化与时序迭代 |

每个 skill 只在相关任务中加载完整内容。项目级约定仍应写在项目自己的
`AGENTS.md`，而不是由插件覆盖。

## 安装

打开 Codex 的 `/plugins`，选择 **Add marketplace**，输入
`shijhtop/LogicPilot`，再安装 **LogicPilot**。

## 开发

```bash
python3 -m pytest tests -q
```

English version: [README.en.md](README.en.md)

## 免责声明

LogicPilot 是辅助工具，不替代工程师判断。Skill 输出不构成 CDC、
时序、实现或流片签核；关键设计与工具结果必须由合格工程师复核。
