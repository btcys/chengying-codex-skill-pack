---
name: writing-plans
description: 在帧芯开发工作流已启用且已有用户批准的Spec时，用于探索代码后编写按版本管理、可由子智能体执行的Implementation Plan。
---

# 编写实施计划

计划必须让不了解当前上下文的开发智能体也能准确实施，同时避免把每条命令拆成一张Task。

## 开始前

1. 确认Spec已批准，范围可形成一个独立可交付单元；没有批准Spec的多步骤需求回到Brainstorming，不得用Plan绕过设计确认；多个独立子系统应拆成多份Spec和Plan。
2. 阅读适用的 `AGENTS.md`。
3. 探索现有目录、相似实现、依赖、类型、测试惯例和运行命令。
4. 确认版本号、阶段目录和ROADMAP中的当前单元。
5. 涉及新页面或重大界面时，确认项目 `Design-Brief.md` 已存在或已确认建立，并确认Visual Companion的布局、交互、Golden和状态矩阵已经进入Spec。
6. 运行 [scan-code-hotspots.py](../../scripts/scan-code-hotspots.py) 扫描一次项目代码行数；只把本次会修改或依赖的热点文件及处理决定写进Plan。项目已有`.codex/quality-gates.json`时，同时读取本次适用的`quality:fast`和Plan收尾`quality:pr`准确命令。

不要根据PRD猜文件名、接口、Schema或命令。无法确定的关键事实先调查，仍无法确定再向用户提问。

## 文件与头部

保存为：

```text
docs/plans/<stage>/<unit>-<feature>.md
```

使用 [plan-template.md](references/plan-template.md) 的格式。

`Goal`是一句话交付结果，推荐填写；它是计划字段，不等于Codex运行时Goal。只有用户明确要求时才创建运行时Goal。

好的 `Goal` 写“完成后能验收什么”，不写步骤、口号或内部实现：

```text
好：用户可以在画布中上传素材，刷新后仍保留，并能看到真实失败原因。
差：完成上传模块开发。
差：修改UploadPanel、API和数据库。
```

需求很小且Plan头部的功能名称和Acceptance已经完全说明结果时，`Goal`可以省略；不要为填字段编造一句重复文本。

`Global Constraints`只写全部Task共同遵守且能验证的约束，例如固定版本、禁止新增依赖、已批准Golden、平台边界和共享命名规则。只影响一个Task的要求留在该Task，不把普通建议堆进全局约束。

代码体量默认规则：普通源文件超过600行预警，新文件或从未超限文件不得增长到1000行以上；测试文件超过1000行预警、1500行硬上限。既有超过对应硬上限的文件执行no-growth，修改其业务域时只渐进拆分相关职责。生成代码、第三方代码、迁移、快照和纯数据文件不计入。不用行数自动升级HIGH_RISK。

确实不适合拆分时，在Plan标记 `APPROVED_EXCEPTION` 并写明原因、适用路径和边界；验证命令对每个准确路径显式追加 `--allow-over-limit <path>`。例外不接受目录、通配符或无记录的临时绕过。

## Task粒度

- 一个Task交付一个可验证的功能结果或工程边界，可以包含多个紧密相关步骤。
- 不把“打开文件、写一行测试、运行一次命令”拆成独立Task。
- 同一功能必须共同理解和修改的文件放在同一Task；能独立开发且不共享文件或状态的Task明确标注可并行。
- 每个Task写清依赖、结果、验收、Files、Interfaces、步骤、定向验证和`Remaining`；Plan获批后，后续需求默认增量合并，新增需求建立新Task，修改或删除原Task先展示差异并确认，再按修订规则保留旧版。
- `Rework`使用 [failure-evidence-contract.md](../product-spec-governance/references/failure-evidence-contract.md)；预期TDD RED和未改变Task状态的临时错误不记录。
- 精确列出新建、修改和测试文件；如果需要改既有接口，写出接口名和调用关系。
- 计划写行为和关键伪代码，不复制大段最终实现。

写每个Task时读取 [task-contract.md](references/task-contract.md)，确保路径、接口、验收和验证足以让无上下文开发代理准确执行。

## TDD与UI验证

- Bug、业务逻辑、状态、API、数据、权限、计费和公共合同标出RED-GREEN-REFACTOR步骤。
- CSS、布局、文案、静态资源、fixture和简单配置不强制失败测试先行，写真实页面、交互和Golden验证。
- 每个Task只运行与改动相关的定向验证；完整test、typecheck、build在Plan全部完成后运行一次。

## 自查

写完后独立检查一次：

- 所有需求是否有Task覆盖；
- 文件和接口是否真实存在或明确标为新建；
- Task依赖和并行标记是否冲突；
- Global Constraints是否包含所有Task共同遵守的版本、依赖、命名、UI、平台和兼容约束；
- 涉及的热点文件是否采用no-growth、局部拆分或有明确例外；
- 是否含占位符、重复Task、未来化抽象或无关重构；
- 验收和验证命令是否足以证明Goal。

直接修复发现的问题，不建立循环Review门禁。

## 执行交接

计划保存后按 [Plan模板的执行启动卡](references/plan-template.md#执行启动卡) 输出范围、非目标、预计交付、Goal执行文案和`1/2`选项，不增加“Goal建议”或第二轮批准。只有用户直接回复当前启动卡的`1`或`2`才开始执行：两者都批准Plan和范围；`1`记录`GOAL`并创建运行时Goal，`2`记录`NORMAL`且不创建Goal。运行时Goal只推进到验收、文档收尾和`READY_FOR_GIT`，不包含Git写操作；其他回复保持`PENDING`。获批后默认交给子智能体执行，无子智能体或用户要求单线程时才使用`executing-plans`。
