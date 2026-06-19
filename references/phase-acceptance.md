# 阶段验收线程

## 目标

Phase Acceptance Thread 专门检查每轮/每阶段开发计划是否完成。它独立于 Execution Thread。

Execution Thread 只能交付、自测和报告结果，不能给自己判定通过。

Lean 流程可以使用轻量验收表，不强制新开独立线程；Standard 和 Enterprise 必须保留独立 Phase Acceptance Thread 或等价独立验收步骤。

本线程必须形成闭环：`Execution 提交 -> Phase Acceptance 验收 -> passed 进入下一阶段 / needs-fix 生成 Fix Request 打回 / blocked 回 PM Thread`。

## 进入条件

必须已有：

- Work ID 和活跃工作安排登记。
- `PHASE_PLAN.md` 当前阶段。
- `HANDOFF.md` 当前任务边界。
- Execution Thread 输出的修改文件列表、测试结果、自动修复记录。
- `VALIDATION.md` 或等价验证方案。
- QA 验证矩阵及当前阶段验证结果。
- 当前阶段涉及的 PRD / DESIGN / TECH_SPEC 或 ADR / 架构影响面。

缺少任一关键输入，不得验收通过。

## 验收内容

逐条检查：

- 当前阶段计划任务是否全部完成。
- 当前阶段验收标准是否全部满足。
- 自动测试是否运行并通过，或失败原因是否明确。
- 替代验证清单是否覆盖当前阶段核心路径。
- QA 验证矩阵是否覆盖当前流程档位、主链路、回归路径和人工检查项。
- UI 验收如需浏览器，是否默认使用内置浏览器完成截图和 smoke；若使用外置 Chrome，是否说明登录态、Cookie、插件或用户指定等必要原因。
- UI 修改或视觉修复是否提供参考截图 ID、before/after 或验收截图，并归档到 `docs/codex/assets/qa/<Work ID>/`。
- 人工验收点是否有结论。
- 如果本轮来自打回修复，Fix Response 是否逐条回应 Fix Request。
- 修改范围是否符合 Handoff。
- 禁止修改范围是否未被触碰。
- 是否新增未经确认的功能、依赖、接口或数据字段。
- 是否更新对应文档：`TASKS.md`、`CODEX_QA.md`、`PHASE_PLAN.md`、必要时更新 `DECISIONS.md`。
- 验收通过时，是否已要求从 `TASKS.md` 活跃工作安排中移除该 Work ID，并归档摘要。
- 是否存在阻塞风险、未关闭缺陷或跨模块影响。

## 输出格式

```markdown
## Phase Acceptance

### 结论
- 阶段：
- 状态：passed / needs-fix / blocked
- 是否允许进入下一阶段：
- 是否生成 Fix Request：
- 验收轮次：

### 计划对照
| 计划项 | 实现结果 | 测试/证据 | 结论 | 备注 |
| --- | --- | --- | --- | --- |
|  |  |  | passed / missing / failed / drifted |  |

### 浏览器验收证据
- 使用工具：内置浏览器 / Playwright / 外置 Chrome / 不需要
- 使用外置 Chrome 原因：
- 地址：
- 视口：
- 截图/证据：

### 打回项
| ID | 严重级别 | 问题 | 证据 | 期望结果 | 打回对象 |
| --- | --- | --- | --- | --- | --- |
| FX-1 | P0/P1/P2 |  |  |  | Execution / PM |

### 允许后置项
-

### Fix Request
- 修复目标：
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
- 活跃工作安排处理：remove-from-active / keep-blocked / update-and-redispatch
```

## 打回规则

- 有计划项未完成：打回 Execution Thread。
- 有测试失败且未解释清楚：打回 Execution Thread。
- 有越界修改：打回 Execution Thread，并更新影响面。
- 有需求矛盾或验收标准不清：回 PM Thread。
- 有 P0 风险：当前阶段状态为 `blocked`。
- 打回 Execution Thread 时，必须生成 Fix Request；不能只写“继续修复”。
- Execution Thread 只能修 Fix Request 中列出的事项；不得借修复新增功能或扩大范围。
- 同一阶段最多自动修复并重新验收 3 轮；仍未通过时状态为 `blocked`，回 PM Thread 重新确认计划、范围或验收标准。
- 每次重新提交验收必须带上修复轮次、修复项对照、测试结果和仍未解决的问题。

只有 Phase Acceptance Thread 输出 `passed`，当前阶段才可标记为 `verified`。通过后必须把对应 Work ID 从活跃工作安排中移除，并在验收/QA/完成记录中留下摘要，避免活跃上下文堆积。
