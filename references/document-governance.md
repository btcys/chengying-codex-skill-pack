# 文档治理与项目目录

## 目录

- 默认目录策略
- Skill 包自身目录
- 流程档位文档策略
- Level 1 文档
- Level 2 文档
- Level 3 文档
- 文档用途
- 写入原则

## 默认目录策略

- 根目录只建议放 `README.md` 和 `AGENTS.md`。
- 项目治理文档优先放入 `docs/codex/`。
- 已有 `README.md` / `AGENTS.md` / `CHANGELOG.md` 时，不得直接覆盖，必须先读取并合并或写入 `docs/codex/`。
- PM Thread 阶段只允许创建项目管理文档区，不得创建源码目录、初始化框架或安装依赖。
- `src/`、`app/`、`server/`、`packages/`、`database/` 等源码目录必须等技术栈确认并进入 Execution Thread 后再创建。

## Skill 包自身目录

本 Skill 包自身采用：

- `SKILL.md`：技能入口和硬规则。
- `references/`：按需读取的流程细则。
- `assets/templates/docs-codex/`：真实项目的 `docs/codex/` 模板。
- `assets/templates/project-root/`：真实项目根目录模板。
- `agents/`：Codex UI 元数据。

不要把项目模板文档散放在 Skill 包根目录。

## 流程档位文档策略

先按 `references/process-modes.md` 判断 Lean / Standard / Enterprise，再决定创建哪些文档。不要在用户确认前直接创建全部模板。

### Lean

适合小工具、Demo、单页、小改动。

必备：

- `README.md`
- `AGENTS.md`

按需：

- `docs/codex/HANDOFF.md`
- `docs/codex/VALIDATION.md`
- `docs/codex/TASKS.md`

Lean 可以把 PRD、产品原型、设计规范、阶段计划和一段式 Goal 指令合并写在 Handoff 中，但必须仍能回答“做什么、不做什么、怎么走、怎么验收、怎么回滚”。

Lean 快速路径可以不创建 `docs/codex/`，使用聊天内轻量 Work ID 和 6 字段工作单作为等价 Handoff；如果任务会延续、需要多人协作、需要复盘，或用户要求沉淀，再创建 `docs/codex/HANDOFF.md` / `TASKS.md`。

### Standard

适合正式软件项目。

PM 阶段核心文档：

- `docs/codex/PRD.md`
- `docs/codex/PROJECT_BRIEF.md`
- `docs/codex/PRODUCT_RESEARCH.md`
- `docs/codex/DESIGN.md`
- `docs/codex/VISUAL_REFERENCES.md`（有截图、设计稿、参考图或视觉对照时）
- `docs/codex/TECH_SPEC.md`
- `docs/codex/PHASE_PLAN.md`
- `docs/codex/VALIDATION.md`
- `docs/codex/HANDOFF.md`

如果 Standard / Enterprise 正式项目在 PM 对齐中已经超过三轮，不能继续只在聊天里滚动整理。必须至少输出一份可复制的结构化对齐包，包含 `PRD v0.x`、`TECH_SPEC v0.x`、`PHASE_PLAN v0.x`、`VALIDATION v0.x` 和 Handoff 草案；信息不足的字段写“待确认”，不要用空泛文本补齐。用户确认要沉淀到仓库时，再写入对应 `docs/codex/` 文件。

文档版本语义：

- `v0.1`：第一版 PM 对齐草案，用来暴露已确认、建议、待确认和缺口；允许存在待确认项，不得作为最终 Goal、Work ID 登记或 Execution Thread 派发依据。
- `v0.2 / v0.3 ...`：根据用户补充、调研、设计确认、技术评审或验收打回更新后的草案；仍属于未冻结版本。
- `v1.0`：本轮开发前冻结版。当前阶段所需范围、非目标、设计/技术/验证/回滚、线程安排和验收标准已足够支撑执行。
- `v1.1 / v1.2 ...`：执行中或验收打回后的兼容修订，不改变核心范围、架构、API、数据模型或阶段目标。
- `v2.0`：范围、架构、数据模型、API 契约、部署方式、阶段目标或业务路径发生重大变化，需要重新对齐和重新授权。

输出任何 `v0.x` 文档时，必须标注“状态：草案 / 未冻结”，并列出“可执行性：不可执行 / 缺口”。进入最终 Goal Prompt、冻结 Handoff、登记 Work ID 或派发 Execution Thread 前，当前阶段必需文档必须是 `v1.0`、明确标记“本轮冻结版”，或在 Lean 快速路径中写明等价冻结工作单。

执行后生成：

- `docs/codex/PHASE_ACCEPTANCE.md`
- `docs/codex/ACCEPTANCE.md`
- `docs/codex/CODEX_QA.md`
- `docs/codex/TASKS.md`
- `docs/codex/FEEDBACK_LOG.md`

### Enterprise

适合长期商业项目。

在 Standard 基础上增加：

- `docs/codex/ROADMAP.md`
- `docs/codex/DECISIONS.md`
- `docs/codex/CONTEXT.md`
- `docs/codex/SECURITY.md`
- `docs/codex/THREADS.md`
- `docs/codex/MERGE_PLAN.md`
- `docs/codex/REVIEW_CHECKLIST.md`
- `docs/codex/RELEASES.md`
- `docs/codex/PRIVACY_AUDIT.md`

截图和视觉证据目录按需创建：

- `docs/codex/assets/visual-references/`：用户提供或外部生成的参考截图、修改截图、设计稿截图、旧系统截图、竞品截图、目标效果图、验收目标图、Product Design/Figma 导出的参考图；这些是实现依据。
- `docs/codex/assets/qa/<Work ID>/`：Codex 执行、浏览器检查和验收过程产生的 before/after 截图、浏览器 smoke 截图、视觉回归证据、修复复验截图；这些是执行证据。

如果截图包含客户数据、个人信息、密钥、内部敏感信息或生产数据，优先脱敏后存档；不能脱敏时，只记录来源、用途、不可入库原因和可访问位置，不把敏感图片提交到仓库。

## Level 1 文档

适合轻量项目：

- `README.md`
- `AGENTS.md`

可以不创建 `docs/codex/`，除非用户要求长期维护。

## Level 2 文档

适合标准项目：

- `README.md`
- `AGENTS.md`
- Standard 核心文档
- 执行后验收文档

## Level 3 文档

适合长期商业项目：

- `README.md`
- `AGENTS.md`
- Standard 核心文档
- Enterprise 扩展文档

不要在用户确认前直接创建全部文件。

## 文档用途

- `PROJECT_BRIEF.md`：项目目标、用户、核心场景、MVP、非目标。
- `PRD.md`：完整产品需求、角色、功能清单、流程、数据权限、验收标准。
- Goal 指令：正式开发前发给用户确认的一段话；可记录在 `HANDOFF.md` 或 `CODEX_QA.md`，不作为必备独立文档。
- `PRODUCT_RESEARCH.md`：PRD 冻结前的竞品/同类产品方向校准、交互参考、开源候选、License、二开成本、采用结论和对 PRD 的影响。
- `PHASE_PLAN.md`：版本化阶段计划、阶段顺序、输入依赖、允许/禁止范围、独立审计点、独立验收标准、阻塞验证、回滚和状态。
- `VALIDATION.md`：测试命令、替代验证清单、不能自动验证的部分和阻塞项。
- `PHASE_ACCEPTANCE.md`：每轮/每阶段计划完成验收，不合格打回执行线程。
- `HANDOFF.md`：PM Thread 给 Execution / Acceptance / Review / Release 等线程的工作单，必须引用 Work ID、修改边界、参考依据、验收标准和派发条件。
- `ACCEPTANCE.md`：需求一致性审核，逐条对照 PRD、产品原型、设计、已确认 Goal 指令、Handoff 和实现结果。
- `DESIGN.md`：产品原型、用户路径、页面结构、视觉方向、交互原则。
- `TECH_SPEC.md`：技术栈、模块边界、数据/API/权限契约、依赖、风险、验证和回滚方案。
- `VISUAL_REFERENCES.md`：参考产品、截图、风格取舍、截图存档路径、对照点和禁止点。
- `ROADMAP.md`：阶段规划、版本目标。
- `TASKS.md`：PM 台账、任务池、活跃工作安排登记、当前任务、状态和完成记录；活跃区只保留未完成工作。
- `FEEDBACK_LOG.md`：用户反馈、重复问题、处理状态和升级到哪些项目文档。
- `CHANGELOG.md`：变更记录。
- `DECISIONS.md`：技术和产品决策。
- `CODEX_QA.md`：执行/验收记录、QA 验证矩阵结果、Fix Request/Fix Response、人工检查和阻塞项。
- `CONTEXT.md`：重要上下文、外部依赖、部署信息。
- `SECURITY.md`：权限、数据、上传、密钥、支付、AI 调用风险。
- `THREADS.md`：线程职责、状态、owner、修改范围。
- `MERGE_PLAN.md`：合并顺序、冲突、回滚。
- `REVIEW_CHECKLIST.md`：上线和合线检查项。
- `RELEASES.md`：版本号、发布时间、发布内容、构建结果、回滚方式。
- `PRIVACY_AUDIT.md`：隐私、权限、日志、第三方 SDK、AI 调用审计。

## 写入原则

- 文档只记录已确认事实、明确假设和待确认问题。
- 输出或更新 PRD、范围、设计或技术方案时，必须分清“已确认 / 我的建议 / 待确认”；建议和推断不得写成用户已确认事实。
- 不要把聊天流水账完整复制进文档。
- 不要把敏感信息、密钥、token 写入仓库。
- 用户提供或外部生成的参考截图、修改截图、设计截图、目标效果图或验收目标图，能访问到文件时必须复制或归档到 `docs/codex/assets/visual-references/`，并在相关文档中记录路径、来源、页面/模块、用途、对照点和确认状态；Codex 执行或验收产生的截图才作为执行证据。Lean 可在对话或轻量验收表中记录截图/观察证据，Standard/Enterprise 归档到 `docs/codex/assets/qa/<Work ID>/`。
- 每个参考资料必须登记用途：`可借鉴` / `不照搬` / `不采用` / `待验证`，并写明它影响 PRD、设计、技术、数据源还是架构；用途未定时不得进入 Handoff 作为执行依据。
- 任务完成后必须更新相关文档。
- PM 派发工作前必须先在 `TASKS.md` 或等价位置登记 PM 台账 / 活跃工作安排；验收通过后必须从活跃登记中删除该 Work ID 条目，并归档摘要到验收或 QA 记录。
- Lean 快速路径的等价位置可以是当前对话中的轻量工作单；Standard/Enterprise 的等价位置必须是仓库文档。
- 从活跃登记中删除不等于删除历史证据；已完成工作必须保留可追溯摘要、验收结论和证据路径。
- 用户反馈问题时必须先写入 `FEEDBACK_LOG.md`；重复、高影响或导致返工的问题必须升级到对应专题文档或检查清单。
- 文档冲突时，以最新用户确认和仓库事实为准。
