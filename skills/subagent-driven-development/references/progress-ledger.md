# 最小执行进度

`progress.md`只用于任务中断、上下文压缩和恢复，不是开发日志。

```markdown
# 执行进度

**Plan:** `docs/plans/0.6.8/0.6.8.1-feature.md`
**Plan Identity:** `<由绝对Plan路径生成的稳定hash>`
**Initial Plan Contract Digest:** `<首次启动时忽略状态、勾选和Rework记录的合同hash>`
**Last Seen Plan Contract Digest:** `<最近一次已提示核对的合同hash>`
**Base:** `<commit或UNBORN>`
**Current Batch:** `Batch 2`

## Completed

- Batch 1：DONE；报告路径；验证证据路径。

## Current

- Batch 2：IN_PROGRESS；报告路径；Remaining位置。

## Tasks

| Task | Status | Round | Report | Evidence |
|---|---|---:|---|---|
| T-03 | REWORK | 2 | `reports/T-03.md` | `E-014` |

## Blockers

- NONE

## Rulings

- 不新增Provider抽象；本版本复用现有接口。风险：后续模型差异需新版本处理。
```

Task状态与Plan一致，只使用 `TODO`、`IN_PROGRESS`、`REWORK`、`BLOCKED`、`DONE`。`Round`记录当前返工轮次；恢复时从第一个非 `DONE` Task继续，不能仅凭批次摘要跳过。

空Git仓库尚无commit时，`Base`使用 `UNBORN`；工作流不得为了获得基准而自动commit。合同摘要忽略Plan/Task状态、Acceptance勾选、Remaining和Rework日志，普通推进不会触发变化警告；Files、Interfaces、Acceptance正文、Steps或Verification变化时才提示核对。

只记录：批次和Task状态、返工轮次、验证或报告路径、对应 `FAIL-EVIDENCE` 指针、Blocker和主任务的重要裁定。不复述失败正文；完成后由Plan、Git和验收证据承接，不长期累积。
