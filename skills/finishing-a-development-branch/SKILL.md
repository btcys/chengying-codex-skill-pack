---
name: finishing-a-development-branch
description: 在帧芯开发工作流的实现、Review、完整验证和产品验收完成后，用于停在READY_FOR_GIT并让用户选择本地commit、保留、合并或创建PR。
---

# Git集成收尾

先核对证据，再把交付标为`READY_FOR_GIT`。AI生成的“可以提交”“准备提交”或“作为下一版本基线”只是状态结论，不是授权；没有用户明确的对应Git授权，不得运行`git add`、`git commit`、`merge`或`push`。

## 1. 确认完成证据

按 [完成前验证](../verification-before-completion/SKILL.md#复用证据) 核对项目要求的完整test、typecheck、build和门禁证据，补跑缺失或失效部分，不因进入Git阶段重复全量验证；确认独立Review及必要复审覆盖最新diff。用户可见Acceptance须完成产品验收，纯内部Plan记录`Product Acceptance: N/A`并完成技术验收。证据未通过时不得执行Git收尾；全部满足后标记`READY_FOR_GIT`，运行时Goal在此结束。

## 2. 确定环境

记录：

- 当前仓库和工作区绝对路径；
- 当前分支、HEAD和未提交改动；
- 基分支及其确定依据；
- 是否为worktree；
- 是否为detached HEAD或submodule；
- 与本次任务无关的用户改动。

无法可靠确定基分支时询问用户，不发明。存在用户未提交修改时，不把它们自动归入、暂存、丢弃或覆盖。

## 3. 提供Git选项

正常分支只向用户提供：

1. 创建本地`commit`（把本次成果保存成可回退的本机版本），不上传GitHub；
2. 暂不`commit`（不保存新版本），保留现在的修改；
3. 创建`commit`后合并到本地主开发分支，不上传GitHub；
4. 创建`commit`，`push`（上传）到GitHub，并创建`PR`（发起合并审核）。

同时展示拟提交文件、排除的用户改动、建议commit message、当前验证和未决风险。接受数字或明确自然语言授权；已有针对本次交付且仍适用的Git授权时沿用，不重复询问。没有明确授权时只做只读检查；目标或范围有歧义、扩大或授权被撤回时先确认。

自然语言按实际动作执行，不强行套菜单组合：“提交并推送”只授权本次commit和push，不自动创建PR或合并；“做完了”“自行推进”不授权Git写操作。获批Plan执行或Goal本身也不授权Git。

若当前是detached HEAD，先报告准确commit；除选项2外，必须先由用户提供准确分支名，不得发明分支，也不得假装存在可集成功能分支。

若当前位于submodule，必须分别报告submodule commit和superproject指针变化；只处理用户明确纳入本次交付的层级。丢弃不放在默认菜单；只有用户主动要求时才显示准确目标并再次确认。

## 4. 执行选择

### 1. 创建本地commit

只暂存当前Plan范围内的文件，检查`git diff --cached`没有用户改动后创建commit并报告hash；无法可靠区分范围时停止，不猜测暂存。

### 2. 保留工作区

不修改Git状态，报告当前分支、工作区和恢复入口。

### 3. commit并本地合并

先按选项1创建commit，再检查基分支和工作区状态、切换并合并，最后在合并结果上重新运行关键验证；冲突或失败立即停止。

### 4. commit、push并创建PR

先按选项1创建commit；push和创建PR分别须有用户明确授权，数字4同时授权两者。PR概括交付结果、验证、风险和关联Spec/Plan，不泄漏Secret或内部敏感信息。

## 5. 清理

仅在成功合并或用户另行确认丢弃后清理本次任务拥有的worktree。先用 `git worktree list --porcelain` 核对所有权和路径，离开目标目录，再运行 `git worktree remove <exact-path>` 并验证结果。不要删除兄弟worktree、submodule或用户文件。
