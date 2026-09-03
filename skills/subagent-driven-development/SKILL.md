---
name: subagent-driven-development
description: 在帧芯开发工作流已有批准Plan且当前环境支持子智能体时，用于由主任务按功能批次派发开发、整合结果，并在Plan结束后集中完成一次独立Review。
---

# 子智能体驱动开发

主任务负责全局判断，子智能体负责边界清晰的功能实现。目标是减少上下文污染和等待时间，不是把每个微步骤都变成一个代理任务。

## 适用条件

- 已有用户批准的Spec和最新可执行Plan修订，且`Execution Route`已由用户选择为`GOAL`或`NORMAL`；
- Task可以组成职责清晰的功能批次；
- 主任务可以持续统筹同一个工作区；
- 当前运行时支持子智能体。

没有子智能体能力或用户要求单线程时，改用 `$zhenxin-development-workflow:executing-plans`。

## 不变原则

- 主任务不把整个Plan丢给一个代理后失去控制。
- 子智能体只执行任务简报，不重新规划产品范围，也不得继续派发子智能体。
- 代理报告不能替代主任务对diff、测试证据和集成状态的检查。
- 不为每个Task安排独立Reviewer；整个Plan完成后做一次独立Review。
- 不自动commit、push、merge、创建worktree或安装依赖；只禁止生产写入和超出`Execution Mode`授权范围的外部副作用。

## 1. 准备

1. 确认工作区已隔离或用户接受在当前checkout工作；需要worktree时先使用 `$zhenxin-development-workflow:using-git-worktrees`。
2. 读取最新Plan修订、关联Spec、Global Constraints和适用项目指令；确认`Approval=APPROVED`且`Execution Route`不是`PENDING`。
3. 记录开始commit、当前未提交改动和用户已有改动；空仓库没有commit时准确记录 `UNBORN`，不得为了流程自动创建baseline commit；不得覆盖或归入用户成果。
4. 检查Plan中的文件、接口、依赖和命令是否仍准确；关键缺陷先展示增量差异并让用户确认，未经确认不得修订已批准内容。
5. 按依赖关系把Task组成少量功能批次。
6. 运行 `scripts/execution-workspace.sh <plan>` 创建或恢复 `.codex/execution/<plan>/`；目录只保存简洁进度、brief、report和review。
7. 已有 `progress.md` 时先核对当前Git状态、报告路径和Plan，再从第一个未完成批次继续；不能仅凭旧记录跳过工作。

进度格式见 [progress-ledger.md](references/progress-ledger.md)。不要把完整Plan、对话或每次命令复制进账本。

## 2. 决定并行或顺序

批次只有同时满足以下条件才可并行：

- 不修改相同文件或共享核心接口；
- 不依赖另一批次尚未产生的类型、Schema、迁移或行为；
- 不共用会互相干扰的数据库、服务、端口或生成目录；
- 可以用独立测试证明结果。

满足时使用 `$zhenxin-development-workflow:dispatching-parallel-agents`。任何一项不满足就顺序派发。不要为了并行把一个内聚功能硬拆开。

## 3. 派发开发批次

使用 [implementer-prompt.md](references/implementer-prompt.md)。每个简报必须包含：

- Plan路径、与本批次直接相关的Spec章节和证据路径；完整Spec只在跨多个合同或出现歧义时读取；
- Task编号与完整文本；
- 绑定的Global Constraints；
- 允许修改的功能范围和已知相邻改动；
- 需要运行的定向验证；
- 报告文件路径；
- `Execution Mode`及必要的费用/数据范围；禁止继续派发、生产写入和超出该模式授权范围的副作用。

优先让代理直接读取简报文件，避免在主任务上下文重复粘贴大段Plan。可用 `scripts/task-brief.sh <plan> <task-number> [output]` 提取Task。

## 4. 接收与整合

每个开发代理返回后，主任务必须：

1. 读取报告和实际diff，不只看摘要；
2. 确认没有越界修改、覆盖用户改动或增加未批准依赖；
3. 检查报告包含测试文件、命令、结果和剩余风险；
4. 根据代理状态处理：`NEEDS_CONTEXT`先补最小上下文，`BLOCKED`由主任务裁定，`DONE_WITH_CONCERNS`不能直接视为完成；
5. 运行必要的整合定向测试；
6. 更新Plan中的Task状态、Acceptance和Remaining；子智能体报告`DONE`只表示实现批次完成，用户可见Task在产品验收前保持未完成状态。
7. 在 `progress.md` 更新批次、Task状态、返工轮次、报告路径、证据路径、Blocker和重要裁定，不复述实现结果。

基础批次若定义了多个后续批次依赖的公共接口、Schema或状态合同，进入后续批次前由主任务检查其diff和定向证据；证据不完整时停止，不默认增加独立Reviewer。

实现或定向验证失败时，优先把明确失败和证据发回原代理修复。每轮都要记录结果和根因；同一Task连续三轮仍未通过时转 `BLOCKED`，停止继续补丁，使用系统化调试并复查Spec、Architecture或Task边界。

不要让多个代理同时修同一问题，也不要在主任务中悄悄代替代理修复后跳过记录。

## 5. Plan级独立Review

所有Task达到可集成状态后：

1. 运行 `scripts/prepare-review.sh <base-ref-or-UNBORN> <output>` 生成状态、提交、受控tracked diff和未跟踪文件diff；二进制或超大文件只记录大小、blob hash和变更统计，Reviewer按需读取相关区段。脚本无法覆盖特殊仓库时直接提供准确diff范围和文件内容。
2. 使用 `$zhenxin-development-workflow:requesting-code-review` 派一个未参与实现的独立Reviewer；它是唯一Plan级Review入口和模板来源。
3. Reviewer针对整个Spec和Plan给出一次结论，不为每个Task重复Review，也不重复执行已有的新鲜可信测试；不得再从本Skill额外派第二个Reviewer。
4. `BLOCKER`或`IMPORTANT`问题由一个修复代理统一处理，避免每个问题重新建立上下文。
5. 修复后只做一次针对原问题和修复diff的定向复审，使用 [re-reviewer-prompt.md](references/re-reviewer-prompt.md)。
6. 仍有影响交付的真实问题时将Plan标记 `BLOCKED` 并报告用户；不进入第二轮修复波次或五轮Review循环。

## 6. 完成

独立Review通过后：

1. 使用 `$zhenxin-development-workflow:verification-before-completion` 运行完整验证；
2. 若Plan含用户可见Acceptance，使用 `$zhenxin-development-workflow:product-acceptance`；纯API、内部数据或基础设施Plan记录`Product Acceptance: N/A`并完成技术验收。
3. 汇总 `progress.md` 中主任务做出的范围裁定及其风险；
4. 完成文档收尾并标记`READY_FOR_GIT`；运行时Goal在此结束，再使用 `$zhenxin-development-workflow:finishing-a-development-branch` 等待用户选择，选择前不执行Git写操作；
5. 临时执行目录可在结果已被Plan、Git和验收证据承接后清理，清理必须使用解析后的精确目录。
