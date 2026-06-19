# 需求一致性审核

## 目标

需求一致性审核只回答一个问题：开发结果是否严格符合已确认需求。

它不同于 Code Review：

- 需求一致性审核：检查有没有按 PRD、设计规范、Goal 授权、阶段计划、Work ID 和 Handoff 工作单做。
- Code Review：检查代码正确性、安全、性能、可维护性和测试缺口。

## 输入

进入本审核前必须已有：

- `PRD.md` 或 PM Handoff 中的完整 PRD。
- `DESIGN.md` / `VISUAL_REFERENCES.md` 或明确的非 UI 说明。
- 已确认的一段式 Goal 指令和用户确认记录。
- Work ID、活跃工作安排归档或阶段验收记录。
- `PHASE_PLAN.md`。
- 全部阶段的 `PHASE_ACCEPTANCE.md` 或等价验收结论。
- `HANDOFF.md`。
- `VALIDATION.md` / QA 验证矩阵结果。
- Execution Thread 的修改文件列表、测试结果、自动修复记录。

缺任一关键输入，不得进入需求一致性审核或 Code Review。

任一阶段验收未通过，不得进入需求一致性审核。

## 审核清单

逐条检查：

- PRD 功能是否全部覆盖。
- 非目标是否没有被偷做。
- 设计规范是否被遵守。
- 原型图/草图已确认的结构是否被实现。
- Goal 成功标准是否满足。
- Work ID 对应工作单是否完成，且没有把其他工作混进来。
- 阶段计划中当前阶段任务是否全部完成。
- Handoff 的修改范围是否被遵守。
- 禁止修改范围是否没有被触碰。
- 验收标准是否逐条通过。
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
- 有 PRD 与实现矛盾：回 PM Thread 重新确认。
- 打回 Execution Thread 时必须生成 Fix Request，列明需求来源、偏差证据、期望结果、禁止扩大范围和必须重新验证的路径。
- 同一需求一致性问题最多自动修复 3 轮；仍不通过时回 PM Thread 重新确认需求或验收标准。

需求一致性审核通过后，才进入 Code Review Thread。
