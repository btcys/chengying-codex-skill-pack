# 失败证据合同

用于让返工、阻断和工作流复盘有稳定证据，同时不建立新的Bug目录、信号队列或开发日志。

## 何时记录

只有真实失败导致Task进入 `REWORK`、`BLOCKED`，或Plan级Review、完成验证、产品验收判定失败时记录。以下情况不记录：

- TDD中预期发生的RED；
- 开发中立即修正、没有改变Task状态的普通编译错误；
- 相同命令和相同根因的重复输出；
- 没有证据的推测或情绪判断。

## 写在哪里

写入当前Plan中受影响原Task的 `Rework`。截图、长日志和报告继续放在既有Evidence或执行目录，只在记录中引用路径或Evidence ID。`progress.md`只保存Task、Round、状态和同一证据指针，不复制正文。

## 固定格式

每个改变Task状态的失败轮次一行：

```markdown
- FAIL-EVIDENCE | 2026-08-31 | Stage=ACCEPTANCE | Round=2 | Expected=深色主题下按钮文字可读 | Observed=禁用态文字与背景对比不足 | Evidence=ACCEPT-021 | RootCause=IMPLEMENTATION | Resolution=OPEN
```

枚举：

- `Stage`：`DEVELOPMENT | REVIEW | VERIFICATION | ACCEPTANCE`
- `RootCause`：`PRODUCT | IMPLEMENTATION | ENVIRONMENT | WORKFLOW | UNKNOWN`
- `Resolution`：`OPEN | FIXED | DEFERRED | BLOCKED`

`Expected`和`Observed`各写一个可验证短句；值中不要使用 `|`。`Evidence`写准确命令、报告路径或Evidence ID，不粘贴长输出。根因未证明时必须写 `UNKNOWN`；调查完成后原地更新同一行，不能为了完整而猜测。

修复或裁定后更新同一行的 `RootCause` 和 `Resolution`。相同根因在新返工轮次再次导致失败时新增一行，以保留重复次数；同轮重复运行只更新Evidence，不复制记录。

## 安全和上下文

- 不记录Secret、个人信息、生产敏感数据或完整日志；
- 不因为记录失败自动触发工作流复盘；
- 不从失败数量直接判断流程有问题；仍需区分产品、实现、环境和流程根因；
- 复盘时先在选定版本Plan中搜索 `FAIL-EVIDENCE`，只跟进相关证据指针，不预读全部Plan和archive。
