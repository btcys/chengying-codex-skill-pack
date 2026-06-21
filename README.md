# 橙影 · Codex 正式项目工作流 Skill Pack

<p align="center">
  <img src="assets/readme/hero.svg" alt="橙影 Codex 正式项目工作流 Skill Pack" width="100%">
</p>

<p align="center">
  <img alt="Codex Skill Pack" src="https://img.shields.io/badge/Codex-Skill%20Pack-0f766e?style=flat-square">
  <img alt="Workflow" src="https://img.shields.io/badge/Workflow-Formal%20Project-2563eb?style=flat-square">
  <img alt="Autopilot" src="https://img.shields.io/badge/Assisted%20Autopilot-default-7c3aed?style=flat-square">
  <img alt="Validation" src="https://img.shields.io/badge/Validation-required-b45309?style=flat-square">
</p>

面向 Codex 的正式项目 / 长期项目开发工作流。它不再维护多档流程，而是把项目快速收敛成短任务卡，然后连续开发、测试、修复；只有出现风险、长期沉淀或跨线程需要时才补文档。

> 先思考后动手，能开发就开发，风险出现再加治理。

## 一眼看懂

| 项目 | 说明 |
| --- | --- |
| 它是什么 | 正式项目和长期项目的 Codex 开发协作规则 |
| 不做什么 | 不再为临时原型设计流程；原型可先直接开发，后续再接管 |
| 解决什么 | 防止流程臃肿、上下文被文档吃掉、PM 线程一直推进不了开发 |
| 默认方式 | 任务前短思考 -> 短任务卡 -> 当前线程开发/测试/修复 -> 必要文档沉淀 |
| 长期保障 | 用 `docs/codex/CURRENT_STATE.md`、任务卡、验证记录和决策文档保持项目连续性 |

## 核心原则

| 原则 | 要求 |
| --- | --- |
| 先思考后动手 | 动手前说明需求、目标、现状、影响范围、方案和验收标准 |
| 简洁优先 | 最少代码、最少文档，不加未请求功能和未来抽象 |
| 手术式修改 | 先读相关文件，只改必须改的部分，不顺手重构 |
| 目标驱动 | 把模糊任务变成可验证目标，开发后必须验证或说明未验证 |
| 风险直说 | 发现逻辑漏洞、体验问题、技术风险或维护成本，直接指出 |
| 长期记忆 | 重要状态写入 `docs/codex/CURRENT_STATE.md`，避免线程忘记安排 |

<p align="center">
  <img src="assets/readme/workflow.svg" alt="橙影 Codex 工作流主链路" width="100%">
</p>

## 默认流程

1. 读取相关文件和已有项目文档。
2. 输出短任务卡：目标、已知事实、不确定、影响范围、方案、验收、风险/回滚。
3. 信息足够时直接开发，不让流程卡住。
4. 运行测试、构建、lint、浏览器检查或替代验证。
5. 验证失败就继续修复；遇到关键不确定或高风险才停下问。
6. 长期项目更新 `docs/codex/CURRENT_STATE.md`、`TASKS.md`、`DECISIONS.md` 或 QA 记录。

## 什么时候补文档

| 情况 | 文档 |
| --- | --- |
| 新正式项目或长期接管 | `CURRENT_STATE.md`，必要时 `PRD.md` |
| 跨模块或多阶段 | `PHASE_PLAN.md` 或短阶段表 |
| 架构、API、数据、权限、部署、密钥、外部服务 | `TECH_SPEC.md` 或 ADR |
| 验证路径不清 | `VALIDATION.md` 或 QA 清单 |
| 派给其他线程/人 | `HANDOFF.md` |
| 重要取舍和用户确认 | `DECISIONS.md` |
| 反馈导致返工 | `FEEDBACK_LOG.md` |

## 安装

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/btcys/chengying-codex-skill-pack.git ~/.codex/skills/chengying-codex-enterprise-skill
```

安装后重启 Codex，或开启新的 Codex 对话，让 Skill 列表重新加载。

## 快速开始

```text
启动橙影 Codex 正式项目工作流。先梳理任务卡，然后能开发就继续开发；只有关键不确定或高风险再停下问我。
```

```text
按橙影工作流接管这个已有项目。先读 README、AGENTS、docs/codex/CURRENT_STATE.md 和相关代码，给我任务卡后继续执行。
```

```text
这个项目准备长期维护，请建立 CURRENT_STATE.md，并按短任务卡推进后续开发。
```

## 项目文档

真实项目建议把治理文档放到 `docs/codex/`。不要一开始创建全套文档，只按任务需要创建。

模板在 [`assets/templates/docs-codex/`](assets/templates/docs-codex/) 和 [`assets/templates/project-root/`](assets/templates/project-root/)。

## 详细规则

| 文件 | 内容 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Skill 触发入口和核心工作流 |
| [`AGENTS.md`](AGENTS.md) | 面向 Codex 的协作和执行约束 |
| [`references/pm-thread.md`](references/pm-thread.md) | 需求收敛和任务卡 |
| [`references/workflow-gates.md`](references/workflow-gates.md) | 最小门禁 |
| [`references/document-governance.md`](references/document-governance.md) | `docs/codex/` 与 `CURRENT_STATE.md` |
| [`references/technical-spec.md`](references/technical-spec.md) | 技术方案 / ADR |
| [`references/validation-strategy.md`](references/validation-strategy.md) | 验证策略 |
| [`references/execution-contract.md`](references/execution-contract.md) | 自动开发和修复 |
| [`references/architecture-threading.md`](references/architecture-threading.md) | 多线程和跨模块 |
| [`references/release-review-evolution.md`](references/release-review-evolution.md) | 审查、发布和反馈 |
