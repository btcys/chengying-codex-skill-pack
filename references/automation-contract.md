# 受控自动开发契约

## 目标

本 Skill 支持受控自动开发，不支持无边界无人值守开发。

意思是：用户确认 Goal 前，PM 先形成开发前对齐包 / Handoff 草案 / Lean 等价工作单；用户确认 Goal 后，PM 登记 Work ID 并冻结或补齐 PM Handoff 工作单或 Lean 等价工作单。Level 2 / Standard 和 Level 3 / Enterprise 必须由 PM 实际派发给 Execution Thread 或已有执行线程，不能由 PM Thread 自己改代码，也不能把当前 PM Thread 降级为执行线程；线程工具不可用时只能输出 Execution Thread 任务包并停止。Codex 只能在该 Work ID、Handoff 或等价工作单、阶段计划或轻量任务单、修改范围和自动化模式内连续完成开发、自测、修复和文档更新；遇到门禁、风险、越界或需要产品判断时必须停止。

Goal Prompt 不能替代自动开发前置条件。`TECH_SPEC` / `PHASE_PLAN` / `VALIDATION` / Handoff 或 Lean 等价工作单未形成前，即使用户要求“先给 Goal”，也只能输出“当前还不能生成最终 Goal”的阶段状态、缺口和下一步。

## 自动化模式

自动化模式不同于流程档位：流程档位决定治理重量，自动化模式决定 Codex 执行时能连续做多少步。两者都必须在开发前确认。

### Manual

- 每个关键动作前都询问用户。
- 适合高风险、需求不清、生产系统、数据迁移。

### Assisted Autopilot

- 默认推荐。
- 用户确认 Goal、PM 派发 Work ID 且 Handoff 明确后，Codex 在当前阶段内自动开发、测试、修复。
- 阶段结束必须停在 Phase Acceptance Thread。

### Long-run Autopilot

- 只适合低风险、边界清晰、测试完整的项目。
- Codex 可以连续执行多个已确认阶段。
- 每个阶段仍必须经过 Phase Acceptance Thread；不合格立即打回。
- 遇到新依赖、schema/API/权限/支付/上传/发布、API Key、Token、外部数据源、外部抓取、自动化任务或部署风险必须停。

## 自动开发前置条件

必须按当前流程档位具备。Lean 快速路径可以用 6 字段工作单和替代验证清单满足等价前置条件；Standard/Enterprise 使用完整文档。

- Lean / Standard / Enterprise 流程档位已确认。
- 完整 PRD、当前版本 PRD 切片或 Lean 轻量目标/非目标。
- 产品原型/交互草图或明确无需原型。
- 设计规范或明确没有用户可见界面。
- 技术方案 / ADR 已确认，或明确当前任务不需要单独技术方案。
- Goal Prompt 已获得执行授权。
- 开发前对齐包 / Handoff 草案 / Lean 等价工作单已形成。
- Work ID 已登记，PM Handoff 工作单或 Lean 等价工作单已明确目标线程或 single-thread、修改范围、禁止范围、参考依据、验收标准和派发条件。
- Standard/Enterprise 已记录执行线程 ID/链接或派发证据；若状态为 `blocked_waiting_for_execution_thread`，不得开始自动开发。
- `PHASE_PLAN.md` 或 Lean 轻量任务单已明确阶段、验收、测试、回滚。
- `HANDOFF.md` 或 Lean 等价工作单已明确修改范围和禁止范围。
- 架构影响面已确认。
- 自动化模式已确认。
- 已识别测试命令，或已生成 `VALIDATION.md` / Lean 替代验证方案。
- QA 验证矩阵或 Lean 轻量验收方式已覆盖当前流程档位要求。

缺少当前档位的必需项，不得开始自动开发。

## 自动执行循环

```markdown
1. 读取 Work ID、当前阶段计划和 Handoff；Lean 读取轻量任务单。
2. 输出当前阶段理解、修改范围、禁止范围、风险。
3. 实现当前阶段最小可交付任务。
4. 运行测试。
5. 失败则自动修复，最多 3 轮。
6. 更新必要文档。
7. 输出执行结果。
8. 停在 Phase Acceptance Thread；Lean 可停在轻量验收表。
```

## 打回自动修复循环

Phase Acceptance、Requirement Compliance 或 Code Review 打回后，自动修复循环只能基于 Fix Request 执行：

```markdown
1. 读取 Fix Request。
2. 确认必须修改范围、禁止修改范围和重新验证要求。
3. 只修复 Fix Request 指定问题。
4. 运行指定验证和相关回归。
5. 输出 Fix Response。
6. 重新提交对应验收线程。
7. 同一阶段或同一审核问题最多 3 轮；仍失败则停止并回 PM Thread 或技术方案重新确认。
```

## 必须停止的情况

- 用户未确认 Goal 或自动化模式。
- 缺少开发前对齐包、Work ID、活跃工作安排登记、PM Handoff 工作单或 Lean 等价工作单。
- 缺少当前档位所需的 `TECH_SPEC`、`PHASE_PLAN`、`VALIDATION` 或 Goal 就绪判断。
- 需求、设计或验收标准不清。
- 修改范围需要扩大。
- 触碰禁止修改范围。
- 需要新增依赖。
- 需要改 API 契约、数据库 schema、权限模型、状态管理、构建配置。
- 涉及支付、上传、隐私、密钥、API Key、Token、外部数据源、外部抓取、自动化任务、服务器部署或生产发布，但还没有技术方案和验证/回滚方案。
- 自动修复 3 轮仍失败。
- Fix Request 要求扩大范围、改需求或改技术方案。
- 测试缺失且无法建立替代验证。
- Phase Acceptance Thread 打回。

## 不能承诺的事

- 不能承诺一次性完整开发复杂项目。
- 不能跳过 PM、设计、架构、验收和审查。
- 不能把“测试通过”当成“需求满足”。
- 不能用自动开发替代用户对产品方向和发布风险的确认。
