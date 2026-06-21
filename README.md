# 橙影 Codex 开发工作流 Skill Pack

<p align="center">
  <img src="assets/readme/hero.svg" alt="橙影 Codex 开发工作流 Skill Pack" width="100%">
</p>

<p align="center">
  <img alt="Codex Skill Pack" src="https://img.shields.io/badge/Codex-Skill%20Pack-0f766e?style=flat-square">
  <img alt="Workflow" src="https://img.shields.io/badge/Workflow-Codex%20Dev-2563eb?style=flat-square">
  <img alt="Dev Threads" src="https://img.shields.io/badge/Dev%20Threads-up%20to%203--5-7c3aed?style=flat-square">
  <img alt="Review" src="https://img.shields.io/badge/Code%20Review-independent-b45309?style=flat-square">
</p>

面向正式项目 / 长期项目的 Codex 开发工作流。用户定目标，AI 先判断任务强度，再生成必要的 PRD、设计规范、原型依据和开发计划；需要并行且 ownership 清楚时，PM 主控线程最多拆 3-5 个互不依赖开发线程，最后独立总 Code Review、交付和自进化沉淀。

> 人定目标和关键取舍，AI 负责规划、开发、审查、修复和沉淀。

## 一眼看懂

| 项目 | 说明 |
| --- | --- |
| 它是什么 | Codex 正式项目 / 长期项目开发工作流 |
| 核心链路 | Goal -> PRD -> Design Brief -> Prototype -> Dev Plan -> Dev Threads -> Review -> Release -> Evolution |
| 线程策略 | PM 主控编排；需要时最多 3-5 个开发线程；UI 可独立；总 Code Review 独立；发布/运维外置 |
| 解决什么 | 既保留可开发 PRD、可执行设计决策、可验收开发计划，又避免人工推进过慢和文档过重 |
| 长期保障 | `docs/codex/CURRENT_STATE.md`、QA、决策和反馈持续沉淀，换电脑/新线程也能接手 |

## 主流程

```text
1. Goal Contract
2. Product Spec Builder
3. Design Brief Builder
4. Design Maker
5. Dev Planner
6. Dev Builders
7. Code Reviewer
8. Release Builder
9. Evolution Runner
```

## 产物

| 阶段 | 默认产物 |
| --- | --- |
| Goal | Goal Contract |
| 产品/开源调研 | `docs/codex/PRODUCT_RESEARCH.md` |
| PRD | `docs/codex/PRD.md` 短版 |
| 设计规范 | `docs/codex/DESIGN_BRIEF.md` |
| 视觉参考 | `docs/codex/VISUAL_REFERENCES.md` |
| 原型/交互 | `docs/codex/PROTOTYPE.md` 或 `docs/codex/DESIGN.md` |
| 开发计划 | `docs/codex/DEV_PLAN.md` |
| 子线程任务 | `docs/codex/THREAD_TASK.md` / `docs/codex/HANDOFF.md` |
| 验证 | `docs/codex/CODEX_QA.md` / `docs/codex/VALIDATION.md` |
| 发布 | `docs/codex/RELEASES.md` |
| 进化 | `docs/codex/CURRENT_STATE.md` / `docs/codex/FEEDBACK_LOG.md` / `docs/codex/DECISIONS.md` |

## 线程硬规则

- 需要拆线程时，开发线程最多 3-5 个，不含 PM、总 Code Review、运维/发布线程。
- 有 UI 且需要拆开发线程时，UI 必须独立成一个开发线程。
- 子线程必须互不依赖或依赖契约已冻结，能并行最佳。
- 禁止多个开发线程同时修改同一文件、同一 API contract、同一 schema/migration、同一权限模块、同一 shared utils/types。
- 必须修改共享文件时，只能指定唯一 owner。

## 安装

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/btcys/chengying-codex-skill-pack.git ~/.codex/skills/chengying-codex-enterprise-skill
```

## 快速开始

```text
启动橙影 Codex 开发工作流。请先判断任务强度，把我的目标整理成 Goal Contract，再按需要生成短 PRD、设计规范、原型依据和开发计划；需要并行且 ownership 清楚时，最多拆 3-5 个互不依赖开发线程推进。
```

```text
按橙影工作流接管这个已有项目。先读 README、AGENTS、docs/codex/CURRENT_STATE.md 和相关代码，确认运行入口、验证入口和当前未完成任务，再生成 Dev Plan 和线程 ownership 表。
```

## 详细规则

| 文件 | 内容 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Skill 入口和 Codex 开发工作流 |
| [`AGENTS.md`](AGENTS.md) | 主控线程、子线程和审查线程规则 |
| [`references/pm-thread.md`](references/pm-thread.md) | Goal Contract / Product Spec Builder |
| [`references/prd-design-plan.md`](references/prd-design-plan.md) | Design Brief / Prototype / Dev Plan |
| [`references/architecture-threading.md`](references/architecture-threading.md) | 最多 3-5 个开发线程和 ownership |
| [`references/execution-contract.md`](references/execution-contract.md) | Dev Builder 自动循环 |
| [`references/release-review-evolution.md`](references/release-review-evolution.md) | Code Review / Release / Evolution |
| [`references/document-governance.md`](references/document-governance.md) | 文档和 `docs/codex/CURRENT_STATE.md` |
