# Code Review、Release 与 Evolution

## 总 Code Review

独立线程，不算开发线程。

- 不写业务代码。
- 不改文件。
- 审查需求偏差、越界修改、测试缺口、安全/密钥/权限风险。
- 输出 Fix Request。
- Fix Request 必须回到对应 owner Dev Thread；owner 修复后返回 Fix Response；PM 再重新验证并决定是否再次 Code Review。

```markdown
## Fix Request
- Owner：
- 未通过项：
- 证据：
- 期望结果：
- 禁止扩大范围：
- 必须重新验证：

## Fix Response
- Owner：
- 修复内容：
- 修改文件：
- 重新验证：
- 剩余风险：
```

## Release Builder

按发布目标输出，不是所有任务都需要版本号。

普通任务输出：

- 修改摘要
- 验证结果
- 未验证项
- 风险 / 回滚

阶段验收、预览或发布任务输出：

- 可发布版本号
- 交付物 / 构建产物
- 修改摘要
- 验证证据
- 未验证项
- 风险
- 回滚方式
- 发布说明或 Release Handoff

阶段或发布任务必须形成可交付版本，而不只是“代码已改完”。发布版本至少包括版本号、范围、构建/测试结果、已知问题、回滚方式和是否允许发布。不能实际发布时，也要输出可交给运维/发布线程执行的 Release Handoff。

## 正式商用发布检查

完整商业项目检查只在明确 `commercial` 或正式商用发布前执行。非商用、阶段验收、内测、技术预览或普通迭代不因完整商业检查阻塞开发，只记录适用的风险和待补项。

正式商用发布前至少检查：

- 鉴权 / 权限 / 账号边界。
- 密钥 / Token / 环境变量 / secret scan。
- 数据迁移 / 备份 / 回滚。
- 构建 / lint / test / 关键 smoke。
- UI 关键路径截图或等价验证。
- 日志 / 监控 / 错误追踪 / 告警入口。
- 已知问题、未验证项、发布说明和回滚方案。

运维/发布线程是外部线程，不占开发线程名额。

## Evolution Runner

每次交付后判断是否更新：

- `docs/codex/CURRENT_STATE.md`
- `docs/codex/TASKS.md`
- `docs/codex/CODEX_QA.md`
- `docs/codex/DECISIONS.md`
- `docs/codex/FEEDBACK_LOG.md`
- `docs/codex/REVIEW_CHECKLIST.md`

重复踩坑、导致返工或用户明确反馈的问题必须沉淀。
