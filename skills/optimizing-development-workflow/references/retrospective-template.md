# 工作流复盘输出格式

```markdown
# <版本或范围>工作流复盘

**Status:** `NO_CHANGE | PROPOSALS`
**Evidence Window:** <版本、Plan、日期或任务范围>
**Sources:** <只列实际读取的路径和命令>
**Failure Entries:** <读取的FAIL-EVIDENCE数量；没有则写0>

## 事实摘要

- 原计划路径：
- 实际路径：
- 重复次数：
- 可观察成本：返工轮次、等待、Review次数、上下文体量或阻断结果。

## 根因分类

| 现象 | 产品 | 实现 | 环境 | 流程 | 证据 |
|---|---|---|---|---|---|

## 建议

### Proposal 1: <保留、删除或调整什么>

- **Action:** `KEEP | REMOVE | ADJUST`
- **Scope:** `PROJECT_RULE | SKILL | SCRIPT | TEMPLATE`
- **Evidence:** <重复模式或高影响事件>
- **Why Workflow:** <为什么不是产品、实现或环境问题>
- **Benefit:** <可观察收益>
- **Risk:** <可能损失的保护>
- **Context Impact:** <预计增加/删除的规则、自动触发和加载范围>
- **Target:** <准确文件；未知则写需要调查，不猜路径>
- **Behavior Test:** <修改后应触发和不应触发的真实场景>

## 不建议改变

- <一次性问题、证据不足或应在产品/实现/环境层解决的事项>

## 用户决定

- `APPROVE <编号>` / `REJECT <编号>` / `REVISE <编号>: <要求>`
```

规则：

- 最多三条Proposal；
- `NO_CHANGE`时删除Proposal章节，说明为什么现有流程已经足够；
- 不用“更完善”“更智能”等不可验证收益；
- 上下文影响必须包含是否增加自动触发、长期文件或每Task必读内容；
- 用户决定前不修改任何目标文件。
