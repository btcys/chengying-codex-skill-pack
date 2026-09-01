---
name: product-spec-governance
description: 在帧芯开发工作流已启用时，用于从指定PRD建立或维护长期商业项目的产品边界、领域词汇、版本路线、Spec、Plan、Task、截图证据和过期文档归档。
---

# 产品与文档治理

让不同文档只承担一种职责，避免长期项目把产品事实、当前任务和历史状态混在一起。

## 产品来源边界

- 用户明确指定一个PRD时，它是本轮唯一产品输入。
- 不自动搜索、读取或合并其他PRD、旧计划、状态文件或旧工作流文档。
- 只有用户要求补充来源时才读取额外文件；发现冲突要报告，不自行覆盖指定PRD。
- 不自动拆分或迁移现有PRD；先提出拆分建议，由用户确认。
- 已有 `CONTEXT.md`只用于解释项目术语，不是产品输入，不能新增、覆盖或推断PRD需求。
- 使用PRD、Spec或Plan前，按 [document-system.md](references/document-system.md) 的文档现实性规则核对当前版本和相关代码；发现`DOC_STALE`或`CODE_DRIFT`时记录证据，不自动改写任一方。

## 执行顺序

1. 检查指定PRD是否足以确定产品结果；产品事实缺失时先澄清。
2. 出现稳定、项目特有且容易混淆的领域词汇时，按需创建或更新根 `CONTEXT.md`；没有词汇需要记录时不创建。
3. 查看 `docs/ROADMAP.md`，确定当前阶段和唯一 `ACTIVE` 交付单元；不存在时提出第一个版本号。
4. 产品事实变化由PM写回PRD或唯一领域PRD；同步更新`PRD-CHANGELOG.md`，当前单元的实现设计写入Spec，实现步骤写入Plan。
5. Task状态和返工记录只留在当前Plan；真实失败按 [failure-evidence-contract.md](references/failure-evidence-contract.md) 记录，不创建 `docs/tasks/`、`docs/bugs/` 或 `docs/rework/`。
6. 有有效截图时才建立证据目录和索引。
7. Task验收回写和版本关闭归档统一按 [document-system.md](references/document-system.md) 的“文档收尾”处理；文档被正式取代时移动归档，不直接删除。

空项目只创建当前需要的最小骨架：根PRD、`PRD-CHANGELOG.md`、ROADMAP、第一个Spec和随后的一份Plan。`docs/prd/`领域文档、证据、归档和发布目录都按实际需要出现，不预建空目录和未来版本文件。

不影响当前Goal的新增Bug或小功能只记录到ROADMAP Inbox，然后继续当前Plan和当前批次；只有用户明确重新排序，或它被确认是当前Spec必需项时，才建立新版本、Spec或当前Task。

目录职责和模板见 [document-system.md](references/document-system.md)。版本、Task、截图和归档规则见 [version-task-evidence.md](references/version-task-evidence.md)。只读取当前操作所需的reference。

## 写入规则

- 创建文档前先检查仓库已有约定，复用已有等价目录和格式；不要并存两套体系。
- `CONTEXT.md`每个词只写1～2句定义和应避免的近义词；不写需求、版本、Task、接口、Schema、代码路径或开发日志。
- 正式Plan只能在探索代码、依赖、类型和测试方式后写精确路径与命令。
- 一次只允许一个 `ACTIVE` 交付单元，除非用户明确批准并行版本线。
- 已完成版本的回归使用新的补丁交付单元，不重开旧Plan。
- 任何移动、归档或重命名都先更新活动引用；永久删除必须获得用户明确确认。

## 交付

报告本次新增或更新的文档、当前版本、当前Plan、未决产品问题和下一步。没有实际写入时明确说明只给出建议。
