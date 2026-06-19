# 阶段验收线程

## 目标

Phase Acceptance Thread 专门检查每轮/每阶段开发计划是否完成。它独立于 Execution Thread。

Execution Thread 只能交付、自测和报告结果，不能给自己判定通过。

Lean 流程可以使用轻量验收表，不强制新开独立线程；Standard 和 Enterprise 必须保留独立 Phase Acceptance Thread 或等价独立验收步骤。

本线程必须形成闭环：`Execution 提交 -> Phase Acceptance 验收 -> passed 进入下一阶段 / needs-fix 生成 Fix Request 打回 / blocked 回 PM Thread`。

## 进入条件

必须按当前流程档位已有。Lean 可使用轻量验收表，不要求完整文档集合；Standard/Enterprise 使用完整输入。

- Work ID 和活跃工作安排登记。
- `PHASE_PLAN.md` 当前阶段，或 Lean 轻量任务单。
- `HANDOFF.md` 当前任务边界，或 Lean 等价工作单。
- Execution Thread 输出的修改文件列表、测试结果、自动修复记录。
- `VALIDATION.md` 或等价验证方案。
- QA 验证矩阵及当前阶段验证结果。
- 当前阶段涉及的 PRD / DESIGN / TECH_SPEC 或 ADR / 架构影响面；Lean 可使用轻量任务单中的风险判断和修改范围。

缺少当前档位的关键输入，不得验收通过。

## 结论判定

Phase Acceptance 不能把“执行线程如实说明了缺口”当作验收通过。结论必须按证据判定：

- 全部计划项完成，全部 `blocking` 验证项运行并有证据，且无阻塞风险：`passed`。
- 实现基本完成，但存在可由 Execution Thread 补齐的缺陷、测试失败、缺证据或阻塞验证未跑：`needs-fix`。
- 缺工具、缺环境、缺账号、缺部署条件、验收标准冲突或需要用户/PM 决策才能补验证：`blocked` 或 `blocked_validation_missing`。

只有验收前已明确为 `non-blocking`、写明风险、owner、后续验证方式并获得用户/PM 确认的项目，才允许进入“允许后置项”。任何 Handoff / `VALIDATION.md` / 阶段计划 / Goal 中列为 `blocking` 或必需的验证项，不得在验收时临时后置。

## 验收内容

逐条检查：

- 当前阶段计划任务是否全部完成。
- 当前阶段验收标准是否全部满足。
- 自动测试是否运行并通过，或失败原因是否明确。
- 替代验证清单是否覆盖当前阶段核心路径。
- QA 验证矩阵是否覆盖当前流程档位、主链路、回归路径和人工检查项。
- UI 验收如需浏览器，是否默认使用内置浏览器完成截图和 smoke；若使用外置 Chrome，是否说明登录态、Cookie、插件或用户指定等必要原因。
- UI 修改或视觉修复是否提供 `VISUAL_REFERENCES.md` 中的参考截图 ID 或 Lean 等价视觉依据；Execution 产生的 before/after、smoke、回归或修复复验截图是否已按档位记录，Lean 可在对话/轻量验收表中记录，Standard/Enterprise 归档到 `docs/codex/assets/qa/<Work ID>/`。
- 浏览器截图、UI smoke、视觉对照、Docker/部署启动、外部服务、权限或安全扫描如果是本轮 `blocking` 验证项，是否已经实际运行并有证据；缺 Playwright/Chromium、Chrome 权限、Docker 命令、账号或环境时，是否先尝试内置浏览器、localhost / preview、临时静态服务、项目 e2e 截图命令、外置 Chrome 或必要审批后仍失败。没有补验证尝试和审批记录时，不能直接判为阻塞结论，必须打回 Execution Thread 补齐。
- 如果用户在验收期间补充新的修改截图、标注截图或目标效果图，是否已作为新的实现依据归档/登记，并生成 Fix Request 或回 PM Thread 更新范围与验收标准。
- 人工验收点是否有结论。
- 如果本轮来自打回修复，Fix Response 是否逐条回应 Fix Request。
- 修改范围是否符合 Handoff。
- 禁止修改范围是否未被触碰。
- 是否新增未经确认的功能、依赖、接口或数据字段。
- 是否更新对应文档：Lean 可在对话中归档摘要；Standard/Enterprise 更新 `TASKS.md`、`CODEX_QA.md`、`PHASE_PLAN.md`、必要时更新 `DECISIONS.md`。
- 验收通过时，是否已要求从 PM 台账 / 活跃工作安排中删除该 Work ID 条目，并归档摘要；Lean 可在对话中标记完成，Standard/Enterprise 更新 `TASKS.md`。
- 是否存在阻塞风险、未关闭缺陷或跨模块影响。

## 输出格式

```markdown
## Phase Acceptance

### 结论
- 阶段：
- 状态：passed / needs-fix / blocked / blocked_validation_missing
- 是否允许进入下一阶段：
- 是否生成 Fix Request：
- 验收轮次：

### 计划对照
| 计划项 | 实现结果 | 测试/证据 | 结论 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  | passed / missing / failed / drifted |  |

### 阻塞验证缺口
| 验证项 | 阻塞级别 | 未完成原因 | 缺少工具/环境 | 必须补的证据 | 处理结论 |
| --- | --- | --- | --- | --- | --- |
|  | blocking / non-blocking |  |  |  | needs-fix / blocked / allowed-deferred |

### 浏览器验收证据
- 使用工具：内置浏览器 / Playwright / 外置 Chrome / 不需要
- 使用外置 Chrome 原因：
- 地址：
- 视口：
- 参考截图 ID：
- before 截图：
- after 截图：
- 截图/证据：
- 截图恢复路径与审批记录：

### 打回项
| ID | 严重级别 | 问题 | 证据 | 期望结果 | 打回对象 |
| --- | --- | --- | --- | --- | --- |
| FX-1 | P0/P1/P2 |  |  |  | Execution / PM |

### 允许后置项
| 项目 | 为什么非阻塞 | 风险 | owner | 后续验证方式 | 用户/PM 确认 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | yes/no |

### Fix Request
- 修复目标：
- 参考截图 ID / 新增参考截图路径：
- 必须修改范围：
- 禁止修改范围：
- 必须重新运行的验证：
- 回归检查：
- 返回验收需要提供的证据：
- 最多修复轮次：

### 下一步
- 回 Execution Thread 修复：
- 进入下一阶段：
- 回 PM Thread 重新确认：
- PM 台账处理：delete-active-entry / keep-blocked / update-and-redispatch
```

## 打回规则

- 有计划项未完成：打回 Execution Thread。
- 有测试失败且未解释清楚：打回 Execution Thread。
- 有 `blocking` 验证项未运行、失败、无证据或因缺工具/环境无法执行：状态为 `needs-fix` 或 `blocked_validation_missing`，不得通过。
- 浏览器截图、UI smoke、Docker/部署启动验证属于本轮范围且缺证据：不得通过；先检查 Execution 是否已经尝试强制恢复路径并请求必要审批。能由执行线程补齐时打回 Execution Thread；缺环境、工具或权限但尚未请求审批时，也打回要求补审批和补验证；用户拒绝审批或全部路径失败后，才标记 `blocked_validation_missing` 并给出下一步补验证路径。
- 允许后置项没有风险、owner、后续验证方式和用户/PM 确认：不得作为后置，按阻塞验证缺口处理。
- 有越界修改：打回 Execution Thread，并更新影响面。
- 有需求矛盾或验收标准不清：回 PM Thread。
- 有 P0 风险：当前阶段状态为 `blocked`。
- 打回 Execution Thread 时，必须生成 Fix Request；不能只写“继续修复”。
- Execution Thread 只能修 Fix Request 中列出的事项；不得借修复新增功能或扩大范围。
- 同一阶段最多自动修复并重新验收 3 轮；仍未通过时状态为 `blocked`，回 PM Thread 重新确认计划、范围或验收标准。
- 每次重新提交验收必须带上修复轮次、修复项对照、测试结果和仍未解决的问题。

只有 Phase Acceptance Thread 输出 `passed`，当前阶段才可标记为 `verified`。通过后必须把对应 Work ID 从 PM 台账 / 活跃工作安排中删除，并在验收/QA/完成记录中留下摘要，避免活跃上下文堆积。
