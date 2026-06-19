# Execution Thread 执行、验收与回滚

## 目录

- 执行线程启动条件
- 开发前声明模板
- 执行前确认
- 执行中规则
- 自动开发、测试、修复闭环
- 任务拆解契约
- 执行后输出
- 打回修复输入
- 回滚机制

## 执行线程启动条件

Execution Thread 必须在用户确认后由 PM Thread 派发启动，并且必须基于 PM Handoff 或 Lean 等价工作单。Level 2 / Standard 和 Level 3 / Enterprise 必须使用独立 Execution Thread 或已有执行线程；PM Thread 不得自行改代码，也不得把当前 PM Thread 降级为执行线程。如果当前环境没有线程工具，PM Thread 只能输出可复制的 Execution Thread 任务包并停止在 `blocked_waiting_for_execution_thread`，等待用户新开或指定执行线程。

启动前必须具备：

Lean 快速路径可以使用聊天内轻量 Work ID 和 6 字段工作单作为等价输入；只要目标、非目标、允许修改、禁止修改、验收方式、回滚方式清楚，且明确不触碰高风险项，就不要求完整 PRD、独立 DESIGN、TECH_SPEC、PHASE_PLAN 或完整 Handoff。

- Work ID 和活跃工作安排登记
- 项目类型与复杂度等级
- Lean / Standard / Enterprise 流程档位
- 完整 PRD 或当前版本 PRD 切片
- 产品原型或交互草图，或明确说明当前任务无需原型
- 设计规范，或明确说明当前任务没有用户可见界面
- UI/视觉任务的参考截图 ID、视觉依据存档路径或明确无截图依据
- MVP 与非目标
- 已确认技术路线
- 技术方案 / ADR 结论，或明确说明当前任务不需要单独技术方案
- Goal 和用户确认结果
- 阶段开发计划
- 自动化模式
- 测试命令或 `VALIDATION.md` 替代验证方案
- QA 验证矩阵
- 当前 Task 目标与边界
- 验收标准
- 风险点
- 准备修改文件范围
- 禁止修改范围
- 架构影响面
- 上下游依赖
- 回滚方式

如果缺少关键字段，先补问或回到 PM Thread，不要直接开发。

Execution Thread 的执行依据是 Work ID、PM Handoff 或 Lean 等价工作单、阶段计划或轻量任务单、验证矩阵或替代验证清单和验收标准。Goal 只证明用户授权了这轮开发，不能替代具体工作单。

如果拿到的是完整 Goal Prompt，但缺少 `TECH_SPEC`、`PHASE_PLAN`、`VALIDATION`、Handoff 或 Lean 等价工作单中的任一当前档位必需项，Execution Thread 必须退回 PM Thread 输出阶段状态表和缺口；不得自行补全范围、技术方案、阶段计划或验证方式。

如果当前上下文只有需求描述、PRD、Goal Draft 或 Goal Prompt，而没有开发前对齐包 / Handoff 草案 / Lean 等价工作单，Execution Thread 必须退回 PM Thread 补齐上下文，不得自行推断修改范围、验收或验证方式。若已有 Handoff 或等价工作单但没有用户明确“按这个 Goal 执行 / 开始开发 / 进入 Execution”的确认记录，也必须退回 PM Thread 补齐授权，不得自行开始改代码。

进入 Execution Thread 前，必须对照 `references/workflow-gates.md` 检查 0 到 6 阶段的相关门禁。Lean 小任务可使用等价轻量产物，但缺 Goal、范围、验收标准或验证方式时仍不得进入执行。

自动开发必须遵守 `references/automation-contract.md`。未确认自动化模式时不得开始；如用户未指定，PM Thread 可以在 Goal 中建议 Assisted Autopilot，并取得用户确认。

开始自动开发前必须读取或生成 `VALIDATION.md`，或在 Lean 快速路径中写明可执行替代验证清单，并确认 QA 验证矩阵或轻量验收方式覆盖当前阶段。如果没有测试脚本，也没有可执行替代验证清单，不得开始自动开发。

## 开发前声明模板

此模板只能由实际 Execution Thread 使用。Level 1 / Lean 快速路径可在当前线程显式切换执行后使用；Level 2 / Standard 和 Level 3 / Enterprise 不得在 PM Thread 中使用本模板来启动开发。

```markdown
当前已切换到执行阶段。

## 执行前确认

1. 当前任务理解：
2. 关键假设：
3. 需求歧义与取舍：
4. 成功标准：
5. 涉及模块：
6. 准备修改文件：
7. 禁止修改文件：
8. 架构影响面：
9. 上下游依赖：
10. 风险点：
11. 验收标准：
12. 流程档位：
13. 技术方案 / ADR：
14. 自动化模式：
15. QA 验证矩阵：
16. Work ID：
17. 工作安排状态：
18. 是否需要用户确认：
```

如果存在多种合理解读，必须列出解读和取舍，不得静默选择。影响目标、范围、数据、安全、用户体验或不可逆操作的不明确点，必须停止并回 PM Thread 或询问用户；低风险实现细节可以声明假设后继续。

如果任务影响公共组件、数据模型、API 契约、权限、状态管理、构建配置、部署、API Key、Token、外部数据源、外部抓取、自动化任务或新增依赖，必须先确认技术方案；Lean 必须升级到 Standard。

开发前声明必须说明当前对应 `PHASE_PLAN.md` 的哪个阶段；Lean 快速路径说明对应轻量任务单即可。

## 执行中规则

- 一次只做一个任务。
- 严格按阶段开发计划执行，不得跳阶段。
- 用最简单能满足当前验收标准的实现；不添加未请求功能、未来扩展点、备用配置或推测性抽象。
- 不允许顺手重构。
- 不允许修改无关模块。
- 不允许越过线程责任边界修改其他线程模块。
- 不允许未评估影响面就修改公共组件、数据模型、API 契约或全局配置。
- 不允许引入新依赖，除非说明原因并获得确认。
- 不允许删除旧功能，除非明确要求。
- 不允许破坏数据结构。
- 不允许格式化、重排或清理与本任务无关的旧代码；只清理本次修改造成的无用导入、变量和临时代码。
- 不允许跳过测试和总结。
- UI 验收、截图、localhost 页面检查默认使用 Codex 内置浏览器；只有需要用户 Chrome 登录态、Cookie、插件、已打开页面状态或用户明确要求时，才切外置 Chrome，并在执行结果中说明原因。
- UI 修改或视觉修复任务必须引用 Handoff / `VISUAL_REFERENCES.md` 中的参考截图 ID，或 Lean 等价视觉依据；执行产生的 before/after、浏览器 smoke 或修复复验截图必须可追溯，Lean 可在对话或轻量验收表中记录，Standard/Enterprise 归档到 `docs/codex/assets/qa/<Work ID>/` 并在执行结果或 QA 记录中写明路径。
- 执行中用户补充修改截图、标注截图、目标效果图或新的验收目标图时，先停止扩大实现范围；将图片作为新的实现依据归档/登记到 `VISUAL_REFERENCES.md`，并要求 PM Thread 更新 Handoff 或 Fix Request。只有不改变范围、交互、视觉目标和验收标准的低风险澄清，才可在记录 ID 后继续。

## 自动开发、测试、修复闭环

Execution Thread 默认执行闭环：

1. 开发当前阶段最小可交付任务。
2. 运行约定测试：typecheck、lint、unit、integration、build、端到端或手动验证。
3. 如果失败，定位原因并自动修复。
4. 修复后再次运行相关测试。
5. 最多连续修复 3 轮；仍失败时，停止并输出阻塞原因、失败日志摘要、建议方案。

不能为了“看起来完成”而跳过失败测试。

如果测试命令不存在，必须说明缺失，并建议补齐测试脚本或使用可替代的验证方式。

测试未通过时，当前阶段状态只能是 `blocked` 或 `in_progress`，不得标记为 `verified`。

Execution Thread 完成后只能标记为 `ready_for_acceptance`，不得自我标记为 `verified`。只有 Phase Acceptance Thread 通过后，当前阶段才能标记为 `verified`。

## 打回修复输入

当 Phase Acceptance、Requirement Compliance 或 Code Review 打回时，Execution Thread 不得重新自由发挥，必须只读取打回包并做定向修复。

打回包必须包含：

- 来源：Phase Acceptance / Requirement Compliance / Code Review / Release。
- Fix Request ID。
- 严重级别：P0 / P1 / P2。
- 问题和证据。
- 期望结果。
- 涉及 UI/视觉时的参考截图 ID 或新增参考截图归档路径。
- 必须修改范围。
- 禁止修改范围。
- 必须重新运行的验证。
- 回归检查。
- 当前修复轮次。

修复规则：

1. 只修 Fix Request 指定问题。
2. 不新增需求、不顺手重构、不扩大修改范围。
3. 修复后重新运行指定验证和相关回归。
4. 输出 Fix Response，对照每个 Fix Request ID 说明处理结果。
5. 重新提交 Phase Acceptance 或对应审核线程。
6. 同一阶段自动修复最多 3 轮；仍失败则停止并回 PM Thread。

## 任务拆解契约

Standard / Enterprise 或非平凡开发前必须把需求拆成：

1. Epic：大模块。
2. Feature：功能。
3. Task：可执行任务。
4. Subtask：具体代码修改。

每个 Task 必须包含：

- 任务目标
- 修改范围
- 禁止修改范围
- 架构影响面
- 上下游依赖
- 输入输出
- 验收标准
- 风险点
- 回滚方法

一个 Task 应该能在一次 Codex 任务中完成。

不允许一个 Task 同时包含大范围重构、新功能、UI 改造、数据结构调整、后端接口调整。

Lean 快速路径可以只保留一个 Task，不要求拆 Epic / Feature / Subtask；但仍必须写清目标、范围、验收和回滚。

## 执行后输出

任务完成后必须输出：

- 修改文件列表
- 完成内容
- 测试结果
- 浏览器验收工具和截图/证据；若使用外置 Chrome，说明原因
- 自动修复轮次
- 阶段状态：`ready_for_acceptance` / `blocked` / `deferred`
- Work ID 状态建议：`ready_for_acceptance` / `blocked`
- 风险点
- 未完成事项
- 下一步建议

被打回后必须额外输出：

- Fix Request ID 对照
- 修复轮次
- 修复证据
- 重新运行的验证
- 未解决项
- 是否重新提交验收

如果没有运行测试，必须说明原因。

## 回滚机制

每个任务必须可回滚。

如果出现：

- 构建失败
- 类型错误
- 核心功能损坏
- 数据风险
- 线程冲突
- 修改范围失控
- 架构影响面判断错误

必须：

1. 停止当前任务。
2. 标记失败原因。
3. 回滚到稳定状态或请求用户确认回滚方案。
4. 重新拆分任务。
5. 按档位更新记录：Lean 可在对话中记录，Standard/Enterprise 更新 `CHANGELOG.md` / `TASKS.md` / `DECISIONS.md`。

不要为了完成任务而掩盖失败。
