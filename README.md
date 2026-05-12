# harness-agent

> PBH 协议驱动的自主代码修复代理 — 我们不教 AI 怎么思考，我们为它提供最佳的执行环境。

## 快速开始

```bash
pip install -e ".[dev]"
make verify
```

## 开发命令

| 命令 | 说明 |
|------|------|
| `make verify` | lint + 测试 + 覆盖率 |
| `make test` | 运行测试 |
| `make lint` | 代码风格检查 |
| `make fix` | 自动修复风格问题 |

## 项目结构

```
harness-agent/
├── src/harness_agent/   # 主代码
├── tests/                # 测试
├── tasks/                # 任务拆解
├── docs/                 # 文档
├── AGENTS.md             # AI 协作协议
├── Makefile
└── pyproject.toml
```

## AI 协作

本项目遵循 PBH 协议。AI 助手请阅读 `AGENTS.md` 了解项目规则和工作准则。

## 生态

本项目是 PBH 生态的第三个产品，与以下项目协同工作：

| 项目 | 说明 |
|------|------|
| [PBH](https://github.com/renjianguojinqianfan/Project-Bootstrap-Harness) | 为项目播种 AI 协作协议（AGENTS.md / make verify / progress.json） |
| [Harness-Lint](https://github.com/renjianguojinqianfan/harness-lint) | 检测 AI 生成代码的典型缺陷，提供归因锚定报告 |

Harness Agent 的行为完全由 PBH 播种的协议文件驱动——当项目规则改变时，只需修改 AGENTS.md，无需改动任何 Agent 代码。

## 许可证

MIT