# TASKS.md

## PM 台账：活跃工作安排登记

本区是 PM Thread 的临时调度台账，只保留当前未完成、未验收通过、仍需跟踪或可能打断的活跃任务。PM Thread 派发任何执行、验收、审查或发布任务前，必须先登记到这里。

验收通过后，必须从本区删除该 Work ID 条目，避免活跃上下文堆积；删除前先在下方完成记录或 `CODEX_QA.md` / `PHASE_ACCEPTANCE.md` 中归档摘要、验收结论和证据路径。这里的删除只针对活跃行，不删除验收证据、截图、测试结果或历史记录。

| Work ID | 阶段 | 目标线程 | 执行线程 ID / 链接 | 派发方式 | 工作内容 | 状态 | 派发时间 | 是否已产生代码修改 | 是否允许打断 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W-001 |  | Execution |  | created_thread / handoff_thread / send_message_to_thread / existing_thread / task_package_only |  | planned / dispatched / in_progress / ready_for_acceptance / accepted / blocked / blocked_waiting_for_execution_thread / cancelled |  | yes/no | yes/no |  |

## 当前任务池

### P0

- [ ] 启动 PM 访谈
- [ ] 确认项目复杂度
- [ ] 确认 MVP
- [ ] 确认视觉方向
- [ ] 确认是否需要开源扫描
- [ ] 确认是否商用/对外
- [ ] 生成第一阶段任务

### P1

- [ ] 待 PM 访谈后补充

### P2

- [ ] 待 PM 访谈后补充

## 任务模板

```md
### Task：任务名

目标：
允许修改：
禁止修改：
验收标准：
风险：
回滚：
```

## 完成记录

| Work ID | 阶段 | 完成摘要 | 验收结论 | 归档位置 | 删除活跃项时间 |
| --- | --- | --- | --- | --- | --- |
|  |  |  | passed / cancelled / superseded | CODEX_QA / PHASE_ACCEPTANCE / RELEASES |  |
