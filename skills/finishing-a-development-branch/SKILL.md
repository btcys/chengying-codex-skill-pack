---
name: finishing-a-development-branch
description: 在帧芯开发工作流的实现、Review、完整验证和产品验收完成后，用于让用户选择本地合并、创建PR、保留分支或丢弃工作，并安全处理worktree。
---

# 收尾开发分支

先验证，再让用户决定集成方式；不要根据“完成”自动push或merge。

## 1. 确认完成证据

运行并检查项目要求的完整test、typecheck、build和其他门禁；确认独立Review和定向复审（如有）覆盖最新diff。若Plan含用户可见Acceptance，确认产品验收已完成；纯API、内部数据或基础设施Plan记录`Product Acceptance: N/A`并确认技术验收完成。失败时停止，不提供合并选项。

## 2. 确定环境

记录：

- 当前仓库和工作区绝对路径；
- 当前分支、HEAD和未提交改动；
- 基分支及其确定依据；
- 是否为worktree；
- 是否为detached HEAD或submodule；
- 与本次任务无关的用户改动。

无法可靠确定基分支时询问用户，不发明。存在用户未提交修改时，不把它们自动归入、暂存、丢弃或覆盖。

## 3. 提供四个选项

正常分支只向用户提供：

1. 本地合并到基分支；
2. push并创建PR；
3. 保留当前分支和工作区；
4. 丢弃本次工作。

说明当前验证和未决风险。等待用户明确选择，不把询问当成授权。

若当前是detached HEAD，不直接提供本地合并或push/PR。先报告准确commit，并只让用户选择：保留当前状态、用用户指定的准确名称创建分支后再进入正常菜单、或确认丢弃。不得发明分支名，也不得在detached状态下假装存在可集成功能分支。

若当前位于submodule，必须分别报告submodule commit和superproject指针变化；只处理用户明确纳入本次交付的层级。

## 4. 执行选择

### 本地合并

检查工作区干净和基分支状态，切换基分支、合并功能分支，再在合并结果上重新运行关键验证。任何冲突或失败都停止并报告。

### push和PR

只有用户明确选择后才push。创建PR时概括交付结果、验证、风险和关联Spec/Plan，不泄漏Secret或内部敏感信息。

### 保留

不清理worktree，报告准确分支和路径。

### 丢弃

这是破坏性操作。再次显示将删除的精确分支、worktree、未合并commit和未提交文件，取得针对这些目标的明确确认后才执行。存在归属不明的文件时停止。优先使用Git的安全删除和worktree命令，不使用 `--force` 或广泛递归删除。

## 5. 清理

仅在成功合并或用户确认丢弃后清理本次任务拥有的worktree。先用 `git worktree list --porcelain` 核对所有权和路径，离开目标目录，再运行 `git worktree remove <exact-path>` 并验证结果。不要删除兄弟worktree、submodule或用户文件。
