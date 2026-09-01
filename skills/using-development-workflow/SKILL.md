---
name: using-development-workflow
description: 用于长期、多模块、按版本推进的商业软件项目，从指定PRD、UI可视化确认、Spec与Plan到子智能体开发、产品验收和正式发布治理；单文件修改、确定性小Bug和短任务不使用。
---

# 帧芯开发工作流 5.8

把产品事实、当前版本设计、实施任务和发布治理分开，让长期项目持续推进而不被流程拖慢。

## 适用边界

进入总入口的条件：

- 用户明确调用本工作流；
- 项目需要持续数月、跨多个模块或按版本交付；
- 当前工作同时涉及产品、UI、工程和商业验收。

用户明确调用时先做最小路由判断；单文件修改、确定性小Bug、文案或样式微调、短时一次性任务仍按普通Codex开发处理，不创建PRD、Spec、Plan或完整治理记录。

若你是被主任务派发的子智能体，只执行任务简报，不重新启动总工作流，也不得继续派发子智能体。

## 上下文控制

- 每次只加载当前阶段的主Skill和当前问题需要的reference，不预读全部Skill；
- PRD、Visual Companion确认、Spec、Plan和brief逐级承接结论，下一阶段以文件合同为准，不重复粘贴历史对话；
- `CONTEXT.md`存在时只作为领域词汇表使用，不作为需求来源；
- 开发子智能体只读取Task brief、必要Spec片段、Global Constraints、相关词条和证据，不读取完整PRD、完整词汇表与其他批次报告；
- 开发和验收按 [执行模式](references/execution-modes.md) 处理；`LOCAL_DEV`/`STAGING_QA`允许范围内的正常测试操作，`PRODUCTION_RELEASE`仍需严格授权；
- UI证据只交给相关UI Task，后端Task只接收其必须遵守的接口和状态合同；
- Review读取Spec、Plan、受控变更材料和验证证据，不重放开发过程；
- 一个阶段完成后先落文档和状态，再进入下一个Skill；Bounded任务不创建Spec/Plan，只有Architectural任务走Spec→Plan，避免在同一轮并行启动设计、计划、开发和验收。

## 先确认本轮输入

1. 读取仓库中的 `AGENTS.md` 和适用的项目指令。
2. 用户明确指定PRD时，只把该文件当作本轮产品来源；不要自动读取其他PRD、旧计划、状态文件或旧工作流文档。根 `CONTEXT.md`存在时可读取相关词条解释术语，但不能从中增加需求。
3. 先检查现有代码、依赖、类型、测试和相似实现；使用PRD、Spec或Plan前，按文档现实性规则核对本次任务的版本、路径、接口、状态和验收，不做全库审计。
4. 发现文档与代码冲突时标记`DOC_STALE`或`CODE_DRIFT`，列出期望、实际和证据，停止受影响范围；不得自动判断应该改文档还是改代码。
5. 没有仓库或代码为空时，从产品边界和第一个可交付单元开始，不提前设计完整企业架构。

需要建立或整理产品文档、版本和证据目录时，使用 `$zhenxin-development-workflow:product-spec-governance`。

### 空项目起步

项目没有代码时按以下顺序开始：

1. 只读取用户指定的PRD，确认产品目标、首批用户、核心闭环、非目标和首个可验收结果；
2. 用产品治理Skill建立最小文档骨架和ROADMAP，不一次创建所有未来领域文档；
3. 把第一个结果编号为独立交付单元；
4. 首次决定项目骨架或昂贵底层能力前，调研仓库现有能力和成熟开源方案，明确采用、薄适配、参考或自研；
5. 涉及新页面或重大界面时，在需求讨论中用Visual Companion确认组件复用、设计规范、布局、交互、关键状态与动效；
6. 将确认结果、架构、依赖和最小项目骨架写入Spec并批准，再写Plan；项目骨架不增加单独审批门禁；
7. 从第一个端到端可运行的功能批次开始开发，后续版本按ROADMAP继续。

在空项目中也不要仅凭长篇PRD提前生成全部服务、模块、Schema和抽象层。

## 标准路线

```text
指定PRD
→ 需求澄清与版本范围
→ 必要时架构复用调研或Spike
→ 必要时Visual Companion确认UI方案
→ 可交付Spec并由用户批准
→ Implementation Plan（用户批准后）
→ 子智能体按功能批次开发
→ 一次独立Review
→ 完整验证
→ 产品验收
→ 分支收尾
→ 发布风险审查与发布治理（仅正式发布时）
```

### 1. 需求与设计

- 新项目、新子系统、接口结构变化或需求仍有歧义：使用 `$zhenxin-development-workflow:brainstorming`。
- 新增功能先按复杂度进行适度需求访谈；每个关键问题给推荐方案、备选和取舍，达到停止条件后立即进入设计，不持续追问。
- 空项目骨架、新子系统和昂贵底层能力先调查项目现有能力与成熟开源方案；结论写入Spec，不单建调研流程。
- 先把大型需求拆成可独立验收的交付单元；每个交付单元一份Spec和一份Plan。
- 产品事实变化先由PM更新PRD或唯一领域PRD并让用户确认，再同步`PRD-CHANGELOG.md`；实现细节只进入Spec或Plan。

### 2. UI可视化确认

新页面、新入口、布局大改、复杂交互或跨页面规范变化时，在 `$zhenxin-development-workflow:brainstorming` 中使用Visual Companion：

- 展示浏览器mockup、布局比较、架构图、关键状态和必要动效；
- 让用户直接选择或提出修改；
- 请求确认前检查组件复用、设计规范、状态与动效，并把结果、状态矩阵和必要Golden写入Spec与Plan；
- 不再创建独立UI线程、第二套Preview项目或额外UI预览阶段。

开发任务随后直接实现真实UI和功能；完成后由产品验收对照已确认设计检查实际页面。

### 3. 写Spec和Plan

- Spec经用户确认后，使用 `$zhenxin-development-workflow:writing-plans`。
- Plan必须写准确文件路径、接口、验证命令和Task依赖。
- Plan前扫描一次项目代码行数，识别与本次交付有关的热点文件；不把全仓统计长期复制进文档。
- `Goal`是Plan中的一句话交付结果，推荐写但不强制使用Codex运行时Goal；不要为了流程自动创建运行时Goal。

### 4. 默认开发执行

默认使用 `$zhenxin-development-workflow:subagent-driven-development`：

- 主任务保持全局上下文并负责整合；
- 按功能批次派开发子智能体，不为每个微小步骤派一个；
- 只有依赖、文件和共享状态互不冲突的批次才并行，使用 `$zhenxin-development-workflow:dispatching-parallel-agents`；
- 有前后依赖或共享核心文件的批次顺序执行；
- 当前环境无子智能体能力，或用户明确要求单线程时，才使用 `$zhenxin-development-workflow:executing-plans`。

### 5. 开发纪律

- Bug、业务逻辑、状态、API、数据、权限、计费和公共合同使用 `$zhenxin-development-workflow:test-driven-development`。
- CSS、布局、文案、静态资源、fixture和简单配置不强制先写失败测试；用真实页面、交互和Golden验证。
- 前端/UI Task按需读取 [前端六点实施规则](references/frontend-six-rules.md)；只检查相关条目，不新增UI线程、Preview阶段或Task级Review。
- 遇到Bug、测试失败或反复返工，先使用 `$zhenxin-development-workflow:systematic-debugging` 找根因，再修复。
- 普通源文件600行预警、1000行硬上限，测试文件1000行预警、1500行硬上限；既有超限文件执行no-growth，当前Task只渐进拆分相关职责，不做无关大重写。Plan批准的准确路径例外可显式放行。
- 开发中运行定向测试；整个Plan完成后使用 `$zhenxin-development-workflow:requesting-code-review` 做一次独立Review。
- 处理Review意见时使用 `$zhenxin-development-workflow:receiving-code-review`，先验证再修改，不盲从。
- 只做当前Task的Acceptance；额外想法记入`Remaining`或ROADMAP Inbox，不顺手实现。宣称完成前必须使用 `$zhenxin-development-workflow:verification-before-completion` 获取新鲜证据。
- 任何代码、接口、状态或数据结构发生改动后，之前的`PASS`证据自动失效，相关Task必须重新验证；未完成真实页面验收时，只能报告“开发完成，待真页验收”，不能报告“已修复”或“已完成”。

### 6. 验收与发布

- 用户可见功能通过技术验证后，使用 `$zhenxin-development-workflow:product-acceptance` 从真实入口验收。
- 产品验收通过后，先使用 `$zhenxin-development-workflow:finishing-a-development-branch` 由用户选择集成方式并形成准确候选commit。
- `$zhenxin-development-workflow:release-risk-review` 只在正式首发、正式版本更新或生产hotfix发布前使用，不进入日常开发循环。
- 正式候选确定后再执行发布风险审查；通过后使用 `$zhenxin-development-workflow:release-governance`，生产执行仍需单独授权。

### 7. 工作流复盘（仅手动）

- 只有用户明确要求复盘、优化或精简工作流时，才使用 `$zhenxin-development-workflow:optimizing-development-workflow`；它不属于标准开发或发布路线。
- 只基于真实版本证据提出最多三条改进，优先删减或收窄现有规则；未经用户批准不修改工作流。
- 不自动采集纠正语句、不在新会话扫描、不维护信号队列，也不创建自动优化Hooks。

## 权限与停止条件

- 未经明确授权，不安装Skill、不写全局目录、不创建worktree、不commit、不push、不merge、不deploy、不release，也不执行生产写入；`LOCAL_DEV`/`STAGING_QA`按执行模式允许范围操作。
- 计划、Spec或Visual Companion确认的UI发生冲突时停止开发并报告冲突。
- 同一Task连续三轮返工仍未通过时转为 `BLOCKED`，停止继续打补丁，重新检查根因、Spec、Architecture和Task边界。
- 不维护巨型状态JSON、长期角色绑定、每Task独立文档或五轮Review循环。
