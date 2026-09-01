---
name: using-git-worktrees
description: 在帧芯开发工作流已启用且计划执行需要与当前工作区隔离时，用于优先使用Codex原生worktree能力或安全创建git worktree并验证干净基线。
---

# 使用Git Worktree隔离开发

为较大功能提供隔离工作区，避免污染用户当前checkout。创建worktree是写操作，必须在当前请求范围内且获得必要授权。

## 0. 识别现有隔离

先检查当前环境是否已经是Codex worktree或独立任务目录。已隔离时直接复用，不嵌套创建。

使用以下只读信息区分普通checkout、worktree和submodule：

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git status --short --branch
```

记录当前分支、HEAD和未提交修改。`git-dir`与`git-common-dir`不同通常表示worktree；位于父仓库git目录中的独立git-dir可能是submodule，不能当普通worktree清理。

## 1. 选择方式

优先级：

1. Codex或当前运行时提供的原生worktree/新任务能力；
2. 项目已有 `.worktrees/` 或 `worktrees/` 约定；
3. 用户指定位置；
4. 都没有时，提出建议位置并等待确认。

若使用项目内worktree目录，先确认它已被Git忽略：

```bash
git check-ignore -q .worktrees
git check-ignore -q worktrees
```

未忽略时不要擅自修改仓库；报告并征求如何处理。

## 2. 创建

确认基分支、当前HEAD和目标分支准确存在。detached HEAD、脏工作区或无法确认基分支时先报告。不得发明分支名；只有用户明确要求创建新分支时才创建。

```bash
git worktree add <path> -b <branch>
```

如果分支已经存在：

```bash
git worktree add <path> <branch>
```

任何命令执行前都使用明确路径，禁止以 `$HOME`、`~`、仓库根或未解析通配符作为清理目标。

## 3. 项目准备

根据仓库实际文件识别安装和构建方式，例如 `package.json`、`Cargo.toml`、`pyproject.toml`、`go.mod`。新增或安装依赖前检查现有依赖与lifecycle scripts；没有授权不安装。

## 4. 验证基线

在未修改代码前运行项目最相关的测试或检查：

- 通过：报告worktree路径和基线证据；
- 失败：报告失败并区分既有问题，不在未确认时把它当作本次任务修复；
- 无测试：明确说明并选择最小替代验证。

## 5. 清理

只有分支收尾且用户选择删除工作区后才清理。先用 `git worktree list --porcelain` 确认目标确实属于当前仓库，显示精确路径、分支和未提交状态，再执行 `git worktree remove <exact-path>`；不要使用递归删除替代worktree命令，也不要清理来源不明的工作区。
