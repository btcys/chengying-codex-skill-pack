# 定向复审提示模板

```markdown
你只复审上一轮独立Review中的阻断和重要问题，以及修复diff引入的新回归；不重新进行全量风格Review，不修改代码，不派发子智能体。

## 输入

- 原问题清单：<findings>
- 修复diff或材料：<path>
- 修复验证证据：<paths>

逐项给出 `ADDRESSED` 或 `NOT_ADDRESSED`，引用证据。只报告修复diff中新引入的 `BLOCKER` 或 `IMPORTANT` 回归。最后给出 `PASS` 或 `CHANGES_REQUIRED`；是否继续修复或将Task/Plan标为`BLOCKED`由主任务依据根因、进展和授权裁定。
```
