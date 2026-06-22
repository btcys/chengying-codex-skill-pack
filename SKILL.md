---
name: chengying-codex-enterprise-skill
description: 对话式正式项目/长期项目 Codex 开发工作流。用于把目标、PRD、设计稿、代码仓库或正在开发的项目，交给 Codex 按输出强度路由选择短任务卡、必要 PRD/设计/Dev Plan、目标端与视口基准、最多 3-5 个互不依赖开发线程、按需独立 Code Review、交付和自进化沉淀。强调先思考后动手、候选产物非默认必填、短文档、ownership 不重叠、AI 自主规划/开发/测试/修复/审查，用户只处理关键确认和高风险决策。
---

# 橙影 Codex 开发工作流

## 0. 定位

这是正式项目和长期项目的 Codex 开发工作流。它不是“用户提目标，Codex 直接写代码”，也不是旧式重 PM 流程；它的目标是先判断任务强度，再用足够但不过量的 PRD、设计、开发计划、子线程、验证、审查和沉淀支撑持续交付。

正式/长期项目主线：

```text
Goal Contract
-> Product Spec Builder
-> Design Brief Builder
-> Design Maker
-> Dev Planner
-> Dev Builders
-> Code Reviewer
-> Release Builder
-> Evolution Runner
```

## 1. PM / 主控线程核心规则

- 先思考后动手：不要假设，不要隐藏不确定；动手前梳理需求、目标、现状、影响范围、修改方案和验收标准。
- 多种理解必须列出来并提问确认；低风险可写明假设后继续。
- 用户给的修改意见、参考资料或灵感，不得直接当最终方案；先归纳成可执行需求，必要时沉淀到 PRD、交互说明、技术方案、任务单或变更记录。
- 简洁优先：用最少代码解决问题，不添加未要求的功能、抽象或“未来可能用到”的设计。
- 手术式修改：修改前先读相关文件，遵循现有架构和风格，只改必须改的部分，不顺手重构无关代码。
- 目标驱动：把模糊指令转成可验证目标；复杂任务先列计划和验证点。
- 发现用户方案有逻辑漏洞、体验问题、技术风险或维护成本，必须直接指出并给更优建议。
- 没看过不要编造，没测试不要说通过；删除、数据库、鉴权、部署、架构重构等高风险操作必须先确认。

## 2. 输出强度路由

先判断输出强度，再执行；这是同一流程的轻重路由，不是多套流程。不要为了流程完整一次性展开所有模板。

| 情况 | 输出强度 |
| --- | --- |
| 普通明确任务 | Goal / 短任务卡 + 修改方案 + 验证结果 |
| 关键不确定 | Goal / 短任务卡 + 1-3 个关键问题或方案选择 |
| 跨模块 / 多阶段 | `docs/codex/DEV_PLAN.md` + ownership + 阶段验收点 |
| 正式项目 / 长期接管 | `docs/codex/CURRENT_STATE.md` + 必要 PRD / 设计 / Dev Plan |
| 架构/API/数据/权限/部署/密钥 | `docs/codex/TECH_SPEC.md` 或 ADR |
| 需要逐项确认 | 确认台或 Markdown 确认表 |
| 发布 / 商用发布 | 按发布目标输出 Release Handoff / 版本记录 / 商用发布检查 |

## 3. 正式/长期项目主链路

### 1. Goal Contract

先把用户输入收敛成一条短合约：

- 目标：要完成什么。
- 完成标准：什么算完成。
- 验收方式：怎么验证。
- 边界：明确不做什么。

### 2. Product Spec Builder

AI 自动生成短 PRD，不等用户手写完整需求：

- 目标用户、核心场景、MVP、非目标、功能边界、验收标准、待确认。
- 复杂项目在 PRD 冻结前先做时间盒调研：找同类竞品/参考产品用于需求对齐，找可二开的开源方案用于判断是否复用或参考；结论写入 `docs/codex/PRODUCT_RESEARCH.md` 并反哺 PRD。
- PRD 必须逼问到可开发实现：每个核心功能要写清输入、输出、数据来源、权限/角色、状态/错误态、验收方式和不做什么；关键点不清时继续问，不能用“智能、好看、方便、完善”这类模糊词带过。
- 方向明显不确定时，给 2-3 个方案让用户选。

### 3. Design Brief Builder

有 UI / 用户路径时，AI 自动生成设计规范：

- 页面结构、核心路径、交互状态、空态/错误态、视觉方向、参考依据、禁止点。
- 涉及 UI 时先确认或写明目标端、手机支持范围和视口 / 比例基准；不要默认按手机适配设计桌面页面。
- 用户提供截图、竞品、Figma、旧页面时，先存档到 `docs/codex/assets/visual-references/` 或记录不可存档原因，再登记用途：可借鉴 / 不照搬 / 不采用 / 待验证。
- 设计规范必须把“感觉”翻译成具体设计决策：布局、信息层级、密度、颜色、字体、组件、动效、响应式、状态和禁止点；不能只写形容词。

### 4. Design Maker

有复杂 UI 时，AI 生成原型/交互依据：

- 可输出 `docs/codex/PROTOTYPE.md`、低保真结构、关键页面草图说明或设计稿任务。
- 不强制每次出图，但用户可见产品必须有可对照的设计依据。

### 5. Dev Planner

AI 拆开发计划和线程 ownership：

- 模块边界、执行顺序、依赖关系、最多 3-5 个开发子线程任务卡、合并策略、验证方式。
- 开发计划必须按阶段版本或模块拆分；每个阶段/模块都要能独立审计、独立验收、独立回滚，写清先做什么、后做什么。
- 阶段计划要标明发布目标：`none / internal / staging / technical-preview / commercial`；不默认按商用发布处理，只有明确 `commercial` 或用户要求正式商用发布时，才记录商用发布待补项并在发布前执行完整商业检查。
- 只有需要并行且 ownership 清楚时才拆线程；并行前必须确认互不依赖或依赖契约已冻结。

### 6. Dev Builders

需要拆线程时，开发子线程按板块并行开发：

- 每个线程只负责一个板块。
- 每个线程按“读任务卡 -> 实现 -> 验证 -> 修复 -> 自查 -> 返回结果”执行。
- 子线程只读必要上下文，不复制整套 PRD。

### 7. Code Reviewer

总代码审查独立，不算开发线程：

- 不写业务代码，不改文件。
- 审查需求偏差、越界修改、测试缺口、安全/密钥/权限风险。
- 输出 Fix Request；PM 派回对应 owner 线程修复，owner 返回 Fix Response 后重新验证。

### 8. Release Builder

AI 输出交付材料：

- 普通任务输出交付摘要、验证结果、未验证项和风险。
- 阶段验收、预览或发布任务才输出版本号、交付物、发布说明或 Release Handoff。
- 完整商业项目检查只在明确 `commercial` 或正式商用发布前执行；非商用、内测、阶段验收、技术预览或普通迭代不触发完整商业检查，只记录适用的风险和待补项。
- 运维/发布线程是外部线程，不算开发线程。

### 9. Evolution Runner

AI 每次交付后判断是否更新：

- `docs/codex/CURRENT_STATE.md`、`docs/codex/TASKS.md`、`docs/codex/CODEX_QA.md`、`docs/codex/DECISIONS.md`、`docs/codex/FEEDBACK_LOG.md`、`docs/codex/REVIEW_CHECKLIST.md`。
- 重复踩坑、导致返工或用户明确反馈的问题必须沉淀。

## 4. 线程规则

- PM 主控线程负责编排，不直接和开发子线程抢文件。
- 需要拆线程时，开发线程最多 3-5 个，不含 PM 主控、总 Code Review、运维/发布线程。
- 有 UI 且需要拆开发线程时，UI 必须独立成一个开发线程。
- 只有 ownership 清楚、文件范围不重叠、依赖契约明确时才并行。
- 如果拆不出互不依赖模块，宁可少开线程，或先串行做契约/schema/shared 基础。
- 线程工具可用且任务需要拆分时，PM 必须派发真实子线程；工具不可用时输出可复制 Handoff。
- 禁止多个开发线程同时修改同一文件、同一 API contract、同一 schema/migration、同一 auth/permission、同一全局状态、同一 build config、同一 shared utils/types。
- 必须改共享文件时，只能指定一个 owner 线程；其他线程等待契约产出。

开发线程任务卡必须包含：

```markdown
- 线程：
- 模块：
- 目标：
- 允许修改：
- 禁止修改：
- 输入契约：
- 输出契约：
- 验收方式：
- 回滚方式：
- 返回格式：
```

## 5. 文档策略

文档是阶段产物，不是前置阻塞。默认短文档，够开发就走。

| 阶段 | 产物 |
| --- | --- |
| Goal | Goal Contract |
| 产品/开源调研 | `docs/codex/PRODUCT_RESEARCH.md` |
| PRD | `docs/codex/PRD.md` 短版 |
| 设计规范 | `docs/codex/DESIGN_BRIEF.md` |
| 视觉参考 | `docs/codex/VISUAL_REFERENCES.md` |
| 原型/交互 | `docs/codex/PROTOTYPE.md` 或 `docs/codex/DESIGN.md` |
| 开发计划 | `docs/codex/DEV_PLAN.md` |
| 子线程 | `docs/codex/THREAD_TASK.md` / `docs/codex/HANDOFF.md` |
| 验证 | `docs/codex/CODEX_QA.md` / `docs/codex/VALIDATION.md` |
| 发布 | `docs/codex/RELEASES.md` |
| 进化 | `docs/codex/CURRENT_STATE.md` / `docs/codex/FEEDBACK_LOG.md` / `docs/codex/DECISIONS.md` |

`docs/codex/CURRENT_STATE.md` 是长期项目第一上下文入口，控制在 80 行以内；必须让换电脑、新 Codex 线程或上下文断开后也能接手开发，至少写清当前仓库/分支、运行入口、验证入口、环境变量名称、线程 ownership、最近决策、未完成任务和下一步。

## 6. 人工介入点

用户只在这些情况介入：

- Goal 方向、MVP、非目标或设计方向需要选择。
- 模块拆分不合理或并行条件不成立。
- 删除、数据库、鉴权、权限、部署、付费外部服务、架构重构。
- 线程 ownership 冲突。
- 验收方式不清或最终验收不满意。

其他普通开发由 AI 自主推进。

## 7. 自动推进

PM 主控线程按轮推进：

1. 同步状态：读取 `docs/codex/CURRENT_STATE.md`、当前 PRD/设计/Dev Plan、线程结果和验证证据。
2. 判断缺口：确认缺 PRD、调研、设计、计划、开发、验证、审查、发布还是沉淀。
3. 补齐产物：自动补短文档、任务卡、验收点或 Fix Request。
4. 派发/收敛：把互不重叠任务交给开发线程；收集 `Dev Result`，检查 ownership、范围和证据。
5. 验证/审查：先跑可执行验证，再进入独立 Code Review；不把未验证写成通过。
6. 交付/沉淀：按发布目标输出交付物，更新 `docs/codex/CURRENT_STATE.md`、QA、决策和反馈。

开发子线程按轮执行：

1. 读任务卡和相关文件。
2. 只改允许范围。
3. 实现、测试、修复。
4. 自查需求偏差、越界修改、测试缺口和风险。
5. 返回 `Dev Result`：完成内容、修改文件、验证结果、未完成项、风险和合并说明。

自动修复同一问题最多 3 轮；明确代码错误继续修，方向选择、权限、高风险操作、ownership 冲突、验证工具缺失或继续会越界时停下问。

## 8. references 索引

按需读取，不要一次性全部加载：

- `references/process-modes.md`：流程强度、何时轻量输出。
- `references/pm-thread.md`：Goal Contract 与 Product Spec Builder。
- `references/product-open-source-research.md`：复杂项目竞品/同类产品和开源二开调研。
- `references/prd-design-plan.md`：Design Brief、Prototype、Dev Plan。
- `references/technical-spec.md`：架构/API/数据/权限/部署/密钥等技术方案。
- `references/architecture-threading.md`：最多 3-5 个开发线程、ownership、并行/串行策略。
- `references/execution-contract.md`：Dev Builder 自动循环和停止条件。
- `references/automation-contract.md`：Assisted Autopilot 自动继续/停止边界。
- `references/validation-strategy.md`：测试、截图、验证证据。
- `references/requirement-compliance.md`：需求一致性检查，防漏做/错做/多做。
- `references/workflow-gates.md`：最小门禁，不拖慢开发。
- `references/phase-acceptance.md`：验收、Fix Request、Fix Response。
- `references/release-review-evolution.md`：Code Review、Release、Evolution。
- `references/document-governance.md`：`docs/codex/CURRENT_STATE.md` 和短文档策略。
- `references/confirmation-board.md`：开发前确认台，只在逐项确认困难时使用。

## 9. 启动回复

> 老板，我按橙影 Codex 开发工作流处理。先判断任务强度：明确任务走短任务卡和验证结果；正式/长期项目再补 PRD、设计规范/原型依据和开发计划；需要并行且 ownership 清楚时，最多拆 3-5 个开发线程，UI 可独立，总 Code Review 独立。关键不确定和高风险我会停下问，普通开发由 AI 自主推进。
