# Harness Agent 设计文档

**项目名称**：Harness Agent  
**核心定位**：PBH 协议驱动的自主代码修复代理  
**技术栈**：Python + OpenAI Agents SDK + MiMo-V2.5-Pro  
**设计日期**：2026-05-12  
**状态**：Phase 0 完成（最小可行闭环），Phase 1 完成（交互式对话升级）

---

## 1. 项目背景与核心价值

Harness Agent 是 PBH 生态的第三个核心产品。PBH 负责为项目播种 AI 协作协议（AGENTS.md / make verify / progress.json），Harness-Lint 负责检测 AI 生成代码的典型缺陷并提供归因锚定报告。Harness Agent 的使命是补全最后一块拼图——**当 CI 或 Harness-Lint 发现代码问题时，Harness Agent 自动读取项目协议，诊断问题根因，并自主进行修复，最终通过质量门禁验证，形成完整的“发现→诊断→修复→证明”闭环。**

**核心差异化价值**：Agent 的行为不由硬编码的规则驱动，而是由 PBH 播种的协议文件（AGENTS.md、Makefile）驱动。当项目规则改变时，只需要修改协议文件，无需改动任何 Agent 代码。

**技术思想来源**：吸收 Pi 的“极简内核 + Skills 驱动”哲学（Agent 的核心只需要 `read`、`write`、`edit`、`bash`，高级能力通过扩展注入，规则通过文件注入），使用 OpenAI Agents SDK 的 Handoffs 和 Guardrails 原语在 Python 生态中落地。

---

## 2. 系统架构

### 2.1 三层协作架构

```text
┌─────────────────────────────────────────────┐
│            PBH 协议层（规则来源）             │
│  AGENTS.md / make verify / progress.json    │
└────────────────┬────────────────────────────┘
                 │ 驱动 Agent 行为
                 ▼
┌─────────────────────────────────────────────┐
│     三智能体协作层（OpenAI Agents SDK）       │
│                                             │
│  🧠 Architect（规划者）                      │
│  · 读取 AGENTS.md 理解项目规则               │
│  · 分析 CI/Harness-Lint 报告                │
│  · 制定修复计划（只规划，不执行）            │
│        │                                     │
│        │ 委派修复任务（Handoff）              │
│        ▼                                     │
│  🔧 Builder（执行者）—— 待实现               │
│  · 严格按 Architect 计划修改代码             │
│  · 运行 make verify 验证修复                 │
│  · 遵循“手术式修改”原则，不越界              │
│        │                                     │
│        │ 提交修复结果                         │
│        ▼                                     │
│  🔍 Reviewer（审查者）—— 待实现              │
│  · 对照 AGENTS.md 逐条审查修复质量            │
│  · 使用异源模型（DeepSeek V4-Flash）对抗     │
│     “自我评价失真”                           │
│  · 只读不写，输出结构化审查报告               │
└─────────────────────────────────────────────┘
```

### 2.2 核心设计原则

- **协议驱动**：Agent 的行为由 PBH 播种的文件（AGENTS.md、Makefile、progress.json）驱动，不包含硬编码的项目规则。
- **极简工具内核**：核心工具只有 `read`、`write`、`edit`、`bash`，PBH 专属工具（如 `read_agents_md`、`run_make_verify`）作为扩展注入。
- **三智能体分工**：规划、执行、审查三方分离，通过 SDK 的 Handoffs 实现委派，通过 Guardrails 实现质量门禁。
- **自举验证**：Harness Agent 自身的开发也遵循 PBH 协议，`make verify` 检查自身代码。

---

## 3. 核心工作流

```text
CI/Harness-Lint 报告问题
    │
    ▼
┌────────────────────────────────┐
│  Architect 读取 AGENTS.md       │
│  → 理解项目规则                 │
│  → 分析报告中的违规             │
│  → 制定修复计划（不执行）       │
└──────────┬─────────────────────┘
           │ Handoff：委派修复任务
           ▼
┌────────────────────────────────┐
│  Builder 执行修复               │
│  → 严格按计划修改代码           │
│  → 运行 make verify 验证        │
│  → 失败则自修复（最多 2 次）    │
└──────────┬─────────────────────┘
           │ Handoff：委派审查任务
           ▼
┌────────────────────────────────┐
│  Reviewer 独立审查              │
│  → 对照 AGENTS.md 逐条检查      │
│  → 使用异源模型                │
│  → 输出结构化审查报告           │
└──────────┬─────────────────────┘
           │ 审查通过 / 打回修复
           ▼
      交付用户 / 自动合并
```

---

## 4. 技术实现要点

### 4.1 模型配置

- **Architect & Builder**：使用 MiMo Token Plan（MiMo-V2.5-Pro），通过环境变量 `MIMO_API_KEY` 管理密钥。
- **Reviewer（计划中）**：使用 DeepSeek V4-Flash 作为异源模型，对抗“自我评价失真”。
- **API 路由**：MiMo 仅支持 Chat Completions API（不支持 Responses API），需在代码中显式配置 `set_default_openai_api("chat_completions")`。
- **Tracing**：本地开发时禁用 OpenAI Tracing，防止超时日志污染输出。

### 4.2 部署与运行

- **开发环境**：Python 3.11+，虚拟环境 `.venv`，`make verify` 作为质量门禁。
- **运行方式**：通过 `agent.py` 中的 `main()` 函数启动，后续升级为 `chat_loop()` 交互模式。
- **无硬编码密钥**：所有密钥通过环境变量读取（`MIMO_API_KEY`）。

---

## 5. 分阶段开发计划

### Phase 0：最小可行闭环 ✅ 已完成

- [x] 用 PBH 初始化项目骨架
- [x] 安装 OpenAI Agents SDK
- [x] 实现 `agent.py`：Architect Agent 核心逻辑
- [x] 配置 MiMo 自定义客户端（环境变量 + chat_completions API）
- [x] 修复 subprocess 编码问题
- [x] 禁用 Tracing 避免日志污染
- [x] Architect 成功读取 AGENTS.md 并执行 make verify
- [x] **自举验证**：Agent 用 Harness-Lint 检查了自身代码，发现了 I001/UP015/W292 违规，并基于 AGENTS.md §5 进行了归因分析
- [x] 推送 GitHub 仓库

### Phase 1：交互式对话升级 ✅ 已完成

- [x] 增加 `chat_loop()` 函数，让 Architect 支持多轮对话
- [x] 保持对话历史（记忆），避免上下文丢失（使用 SQLiteSession）
- [x] 修复 Architect 自身代码的 3 个 lint 违规（make fix → make verify）
- [x] 编写基本的单元测试（19 个测试，覆盖率 98%）

### Phase 2：执行者引入 🟡 待启动

- [ ] 实现 Builder Agent 角色
- [ ] 通过 SDK Handoffs 实现 Architect → Builder 任务委派
- [ ] Builder 的核心工具：read、write、edit、bash、run_make_verify
- [ ] Builder 遵循“手术式修改”原则，只改必须改的地方
- [ ] Builder 具备自修复机制（最多重试 2 次）

### Phase 3：审查者引入 🟡 待启动

- [ ] 实现 Reviewer Agent 角色
- [ ] 配置异源模型（DeepSeek V4-Flash）
- [ ] Reviewer 只读不写（工具限制）
- [ ] 输出结构化审查报告（通过/不通过 + 问题清单 + 修复建议）
- [ ] 通过 SDK Handoffs 实现 Builder → Reviewer 审查委派

### Phase 4：完整闭环验证 🟢 未来

- [ ] 完整的“发现问题 → Architect 诊断 → Builder 修复 → Reviewer 审查 → make verify 验证”闭环
- [ ] 跨项目测试：用 Harness Agent 修复其他项目的代码问题
- [ ] 文档完善：README、DESIGN.md、CONTRIBUTING.md
- [ ] PyPI 发布