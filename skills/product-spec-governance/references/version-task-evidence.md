# 版本、Task、证据与归档

## 版本规则

```text
0.6.8       当前阶段
0.6.8.1     第1个独立交付单元
0.6.8.2     第2个独立交付单元
```

编号一旦使用不重排、不复用。状态只使用：`PLANNED`、`ACTIVE`、`BLOCKED`、`DONE`、`CANCELLED`。

## 已批准基线与修订

开发版本和文档修订分开：`0.6.8.1`是交付单元，`R1`、`R2`是同一交付单元内的Spec/Plan修订。未批准的Plan草稿可按用户意见原位调整；一旦Spec或Plan获批，其范围、结果、Acceptance、接口和Task定义即成为受保护基线。

后续返工、补充需求和新指令默认是增量输入。先比较当前基线，只报告`保留 / 新增 / 修改 / 删除 / 影响Task`；不得把新指令解释为覆盖旧计划。新增内容在用户确认后加入下一Plan修订；修改或删除只有在用户明确要求替换、取消、删除或以新规则为准，并确认差异后才能进行。新旧内容冲突且取舍不明确时，受影响部分标为`BLOCKED`并等待决定。

修订获确认后，先把旧Spec或Plan保存为`docs/archive/<type>/<stage>/<unit>-<topic>-rN.md`，再让活动文件递增`Revision`、更新日期并通过`Supersedes`指向旧修订。新修订必须逐字保留未变化的已批准内容；Task不建立独立文件，旧Task随旧Plan修订归档。

状态、`Actual Result`、Evidence、`Remaining`、`Rework`和同步结果属于执行事实，可以据实追加或更新，不触发新修订。若改变Task的Result、Acceptance、范围、接口或依赖，必须先确认并递增该Task的`Task Revision`；新增需求建立新Task。已开始执行时，仅受影响Task及其真实下游转`REWORK`或`TODO`，相关旧证据标为`SUPERSEDED`，不受影响Task和证据保持有效。已关闭交付单元不再修订，统一建立新的补丁交付单元。

## Task管理

Task直接写在Plan中，状态只使用：`TODO`、`IN_PROGRESS`、`REWORK`、`BLOCKED`、`DONE`。

每张Task卡至少保留：`Task Revision`、`Supersedes`、结果、验收、Files、Interfaces、步骤、Remaining和精简Rework记录。

子智能体报告`DONE`只代表实现批次完成，不等于Plan Task完成。用户可见Task只有在所有阻断性Acceptance项通过真实页面验收后才标`DONE`；明确标记为`Advisory`的非阻断项可以未完成，不阻塞`DONE`。纯API、内部数据或基础设施Task记录`Product Acceptance: N/A`并完成技术验收后才可`DONE`。Plan或交付单元只有在全部Task完成、Review覆盖最新diff、新鲜完整验证和适用的产品验收完成后才可`DONE`。

- 阻断当前Goal或由当前改动引起的Bug：留在当前版本，原Task转 `REWORK` 或新增当前Plan Task。
- 不影响当前Goal的Bug或小功能：只进入ROADMAP Inbox，继续当前Plan；用户明确重新排序或它成为当前Spec必需项时再晋升。
- 当前Spec必需的补充：未批准Plan可在确认后新增Task；已批准Plan生成下一修订，不覆盖旧Task。
- 改变产品或设计：先更新PRD或Spec并取得批准。
- 已完成版本的回归：创建新的 `0.6.8.n`，不重开旧Plan。
- 部分完成：保持 `IN_PROGRESS`，用checkbox和 `Remaining` 记录；未满足任何阻断性Acceptance不得 `DONE`，明确标记为`Advisory`的事项可以未完成且不阻塞 `DONE`。
- 返工：只有原实现未满足原Acceptance时才使用原Task；新增需求建立新Task，改变原Task定义走确认和修订。每轮按 [failure-evidence-contract.md](failure-evidence-contract.md) 记录一行 `FAIL-EVIDENCE`，修复后原地更新Resolution。
- 重复失败或连续三轮仍未通过：按 [返工与停止条件](../../systematic-debugging/SKILL.md#返工与停止条件) 重新调查；有证据推进的原范围修复继续`REWORK`，真实阻塞才标记`BLOCKED`。

## 截图证据

```text
docs/evidence/0.6.8/0.6.8.1/
├── evidence.md
├── requirements/
├── issues/
├── golden/
└── acceptance/
```

命名示例：

```text
REQ-001-asset-panel-layout.png
ISSUE-001-upload-error-state.png
GOLDEN-default-1440x900.png
ACCEPT-001-upload-success.png
```

`evidence.md`是唯一索引：

```markdown
# 0.6.8.1 截图证据

| ID | 类型 | 文件 | 适用范围 | 要求或实际问题 | 期望结果 | 状态 | 关联 |
|---|---|---|---|---|---|---|---|
| REQ-001 | REFERENCE | requirements/REQ-001-layout.png | 素材面板 | 参考分栏和密度 | 不复制品牌与文案 | ACTIVE | Spec UI章节 |
| ISSUE-001 | ISSUE | issues/ISSUE-001-error.png | 上传失败 | 错误信息不准确 | 显示真实失败类型 | OPEN | Task 3 |
| GOLDEN-001 | GOLDEN | golden/GOLDEN-default.png | 默认态 | 用户确认布局 | 接线后保持 | APPROVED | Global Constraints |
```

类型含义：`EXACT`精确实现；`REFERENCE`只参考结构或交互方向；`ISSUE`记录当前错误；`GOLDEN`是用户确认的UI基线。

问题截图必须同时记录复现入口、步骤、实际结果、期望结果和关联Task。截图去除Secret、个人信息和生产敏感数据；大量媒体使用Git LFS或外部持久化存储。被替换的证据标记 `SUPERSEDED` 并指向新ID。

## 归档

被新文档正式取代的PRD或Spec、已取消且不会执行的Plan、重复错误证据，以及版本关闭时已完成且不再被后续版本引用的Spec、Plan和Evidence进入 `docs/archive/`。仍被后续版本引用的已完成文档继续按版本保留在原目录。

归档前：

1. 确认不是活动引用；
2. 更新有效链接；
3. 增加以下头部；
4. 移到对应归档目录；
5. 不保留两份正文；
6. 不自动永久删除。

```markdown
**Status:** `ARCHIVED`
**Archived At:** `YYYY-MM-DD`
**Last Applicable Version:** `0.6.8.1`
**Replaced By:** `相对路径或NONE`
**Reason:** 一句话归档原因
```
