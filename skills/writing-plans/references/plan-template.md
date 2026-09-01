# Implementation Plan格式

```markdown
# <功能名称> Implementation Plan

**Version:** `0.6.8.1`
**Status:** `ACTIVE`
**Approval:** `PENDING | APPROVED`
**Execution Mode:** `LOCAL_DEV | STAGING_QA | PRODUCTION_RELEASE`
**Authorized Test Scope:** `<费用、账号和数据范围或NONE>`
**Last Updated:** `YYYY-MM-DD`

**Goal:** 一句话说明最终可验收结果（可选；不需要时删除本行）
**Architecture:** 2～3句话说明实现方式和关键边界
**Tech Stack:** 使用的主要技术与已有依赖
**Spec:** `docs/specs/0.6.8/0.6.8.1-<topic>-design.md`

## Global Constraints

- 全部Task共同遵守的准确版本、依赖、命名、UI、平台、安全和兼容约束。
- 已批准Golden或证据ID写在这里。
- UI Task写 `UI Compliance: COMPONENT_REUSE=PASS, DESIGN_SPEC=PASS, STATE_MOTION=PASS`，已批准例外紧随对应项说明；没有UI Task时省略。
- UI Task按需写 `Frontend Focus: TASK_OBJECT | CONTENT_MINIMAL | DATA_SCOPE | STRUCTURE_OWNERSHIP | VISUAL_MOTION | SOURCE_MIGRATION` 中的相关项，不要求六点全部填写。
- 只列本次涉及的热点文件及 `NO_GROWTH | SPLIT_IN_TASK_N | APPROVED_EXCEPTION`；没有则写 `NONE`。
- 本地服务优先使用项目已有的动态端口能力或先探测空闲端口；确需固定端口时写明冲突检查和替代端口，并在验收证据中记录实际URL。

---

### Task 1: <可验证功能结果>

**Status:** `TODO`
**Depends On:** `NONE | Task N`
**Parallel:** `YES | NO`
**Execution Mode:** `INHERIT | LOCAL_DEV | STAGING_QA | PRODUCTION_RELEASE`
**Authorized Test Scope:** `INHERIT | <费用、账号和数据范围>`

**Result:** 完成后用户或系统可以得到什么。

**Acceptance:**

- [ ] 可观察的验收结果1
- [ ] 可观察的验收结果2

Acceptance下每一项默认都是阻断项；只有明确写`Advisory`的事项不参与完成门禁。

**Files:**

- Create: `exact/path/new-file.ts`
- Modify: `exact/path/existing.ts`
- Test: `exact/path/existing.test.ts`

**Interfaces:**

- `functionName(input): Output`：职责和调用方
- `ComponentName`：props、状态或事件合同

**Steps:**

1. 写入或更新覆盖目标行为的失败测试；不适用TDD时写明验证方式。
2. 运行定向测试并确认失败原因与预期一致。
3. 实现满足行为的最小完整改动。
4. 运行定向测试、类型检查或真实页面验证。
5. 自查范围、错误处理和对现有调用方的影响。

**Verification:**

```bash
<准确的定向命令>
```

**Expected:** RED阶段为何失败；GREEN阶段应通过什么。非TDD任务写可观察结果。

**Actual Result:** `PENDING`（验收 `PASS` 后回写实际结果和Evidence）
**Product Acceptance:** `PENDING | PASS | N/A`
**Spec Sync:** `NO_CHANGE | UPDATED | NEEDS_CONFIRMATION`
**Plan Sync:** `PENDING | UPDATED`

**Remaining:** `NONE`

**Rework:**

- `NONE`
- 真实失败时替换为：`FAIL-EVIDENCE | YYYY-MM-DD | Stage=DEVELOPMENT | Round=1 | Expected=<短句> | Observed=<短句> | Evidence=<ID、报告或命令> | RootCause=UNKNOWN | Resolution=OPEN`
```

Task状态只使用 `TODO`、`IN_PROGRESS`、`REWORK`、`BLOCKED`、`DONE`。Acceptance下每项默认都是阻断项；明确标记为`Advisory`的事项不参与完成门禁。子智能体报告`DONE`不等于Plan Task完成，未满足任何阻断性Acceptance不得标记`DONE`。
