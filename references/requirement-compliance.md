# 需求一致性审核

## 目标

需求一致性审核只回答一个问题：开发结果是否严格符合已确认需求。

它不同于 Code Review：

- 需求一致性审核：检查有没有按 PRD、产品原型、设计规范、Goal 授权、阶段计划、Work ID 和 Handoff 工作单做。
- Code Review：检查代码正确性、安全、性能、可维护性和测试缺口。

## 输入

进入本审核前必须按当前流程档位已有。Lean 小任务通常不强制进入需求一致性审核；如果因风险或用户要求启用，可使用 Lean 等价工作单和轻量验收结果作为输入。

- `PRD.md`、PM Handoff 中的完整 PRD，或 Lean 等价工作单。
- 产品原型 / 交互草图结论，或明确的无需原型说明。
- `DESIGN.md` / `VISUAL_REFERENCES.md` 或明确的无用户可见界面说明。
- 涉及截图对照时，用户/外部参考截图、修改截图、目标效果图或验收目标图的 `VISUAL_REFERENCES.md` ID、存档路径、来源或不可入库原因，以及 Codex 执行/验收截图的可追溯证据；Lean 可引用对话/轻量验收表，Standard/Enterprise 引用 `docs/codex/assets/qa/<Work ID>/` 路径。
- 已确认的一段式 Goal 指令和用户确认记录。
- Work ID、活跃工作安排归档或阶段验收记录。
- `PHASE_PLAN.md` 或 Lean 轻量任务单。
- 全部阶段的 `PHASE_ACCEPTANCE.md` 或等价验收结论。
- `HANDOFF.md` 或 Lean 等价工作单。
- `VALIDATION.md` / QA 验证矩阵结果 / Lean 替代验证结果。
- Execution Thread 的修改文件列表、测试结果、自动修复记录。

缺少当前档位的关键输入，不得进入需求一致性审核或 Code Review。

任一阶段验收未通过，不得进入需求一致性审核。

任一阻塞验证项未运行、失败、无证据或状态为 `blocked_validation_missing`，不得进入需求一致性审核或 Code Review。说明缺工具或缺环境只能解释阻塞原因，不能替代验证证据；涉及截图、浏览器 smoke、Docker/部署启动等强制验证项时，必须已经尝试恢复路径并请求必要审批，不能把“尚未申请权限 / 尚未启动 localhost / 尚未尝试内置浏览器”当作最终缺口。

## 审核清单

逐条检查：

- PRD 功能是否全部覆盖。
- 非目标是否没有被偷做。
- 设计规范是否被遵守。
- 用户/外部参考截图、修改截图、设计稿截图、目标效果图是否已按 `VISUAL_REFERENCES.md` 和 Handoff 对照实现。
- Codex 产生的 before/after、smoke、回归或修复复验截图是否已按档位记录；Lean 可引用对话/轻量验收表，Standard/Enterprise 归档到 `docs/codex/assets/qa/<Work ID>/` 并在 QA/验收记录中引用。
- 产品原型/交互草图已确认的结构、路径和状态是否被实现。
- Goal 成功标准是否满足。
- Work ID 对应工作单是否完成，且没有把其他工作混进来。
- 阶段计划中当前阶段任务是否全部完成。
- Handoff 的修改范围是否被遵守。
- 禁止修改范围是否没有被触碰。
- 验收标准是否逐条通过。
- Handoff / `VALIDATION.md` / 阶段计划中所有 `blocking` 验证项是否均有通过证据；浏览器截图、UI smoke、Docker/部署启动、安全/权限验证如在本轮范围内，是否已实际验证。
- 是否新增了未经确认的功能、依赖、接口、数据字段或权限逻辑。
- 是否遗漏边界状态：loading、empty、error、disabled、权限不足、数据为空。
- 是否存在“代码做了但文档没更新”的情况。

## 输出格式

```markdown
## 需求一致性审核

### 结论
- 状态：passed / blocked / needs-fix
- 是否允许进入 Code Review：

### 对照表
| 需求项 | 来源 | 实现位置 | 结果 | 备注 |
| --- | --- | --- | --- | --- |
|  | PRD / DESIGN / GOAL / HANDOFF |  | passed / missing / drifted / extra |  |

### 范围漂移
- 漏做：
- 错做：
- 多做：
- 越界修改：

### 阻塞项
-

### Fix Request
| ID | 严重级别 | 类型 | 问题 | 证据 | 期望结果 | 打回对象 |
| --- | --- | --- | --- | --- | --- | --- |
| FX-REQ-1 | P0/P1/P2 | missing/drifted/extra/scope |  |  |  | Execution / PM |

### 后续处理
- 回 Execution Thread 修复：
- 回 PM Thread 重新确认：
- 可后置并记录：
```

## 阻塞规则

- 有漏做核心需求：不得进入 Code Review。
- 有未经确认的新增功能：不得进入 Release。
- 有越界修改：不得进入 Code Review。
- 有设计规范明显不一致：不得进入 Release，除非用户确认接受偏差。
- 有阻塞验证缺口：不得进入 Code Review 或 Release。
- 有 PRD 与实现矛盾：回 PM Thread 重新确认。
- 打回 Execution Thread 时必须生成 Fix Request，列明需求来源、偏差证据、期望结果、禁止扩大范围和必须重新验证的路径。
- 同一需求一致性问题最多自动修复 3 轮；仍不通过时回 PM Thread 重新确认需求或验收标准。

需求一致性审核通过后，才进入 Code Review Thread。
