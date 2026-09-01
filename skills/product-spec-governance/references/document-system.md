# 项目文档体系

## 推荐目录

```text
项目根目录/
├── PRD.md
├── PRD-CHANGELOG.md                # 仅记录PRD产品事实变更
├── CONTEXT.md                     # 有稳定领域词汇时按需创建
└── docs/
    ├── prd/
    │   ├── README.md                 # 分域索引
    │   └── <domain>.md
    ├── ROADMAP.md
    ├── specs/<stage>/<unit>-<topic>-design.md
    ├── plans/<stage>/<unit>-<feature>.md
    ├── evidence/<stage>/<unit>/
    │   ├── evidence.md
    │   ├── requirements/
    │   ├── issues/
    │   ├── golden/
    │   └── acceptance/
    ├── archive/{prd,specs,plans,evidence}/
    └── releases/<version>/
        ├── release-risk-review.md
        └── release-plan.md
```

## 文档现实性

文档新旧不按文件修改时间判断，而按当前版本链和本次代码核对判断。受控PRD、`PRD-CHANGELOG.md`、Spec、Plan、ROADMAP和CONTEXT头部写最小元数据；每次正文更新都更新`Last Updated`，版本按文档类型递增：PRD及其变更记录使用`Document Version`，其他受控文档使用`Version`。

```markdown
**Status:** `APPROVED | ACTIVE | DONE | SUPERSEDED | ARCHIVED`
**Version:** `0.6.8.1`
**Last Updated:** `YYYY-MM-DD`
**Supersedes:** `NONE | <path>`
```

当前依据只沿着“用户指定PRD → 当前ACTIVE Spec → 当前ACTIVE Plan → 当前Task”读取；`archive/`、旧版本和未被当前链引用的文档默认不读取。版本、路径、接口、状态或验收与代码不一致时，标记`DOC_STALE`或`CODE_DRIFT`并记录证据，不自动改写文档或代码。

变更记录只属于PRD，单独放在根目录`PRD-CHANGELOG.md`（已有项目沿用等价命名，并在PRD头部链接）。PRD产品事实或规则获确认后，递增`Document Version`、更新`Last Updated`，并在变更记录按日期追加一条“稳定结论 + 影响领域 + 链接”；不写实现细节、Task状态、截图或失败日志。Spec、Plan、ROADMAP、CONTEXT、Evidence和执行记录不建立PRD式变更记录，只更新自身版本、日期、状态或记录字段。模板见[PRD变更记录](prd-changelog.md)。

Task验收通过或版本关闭时执行一次“文档收尾”：Task验收先在原Plan中回写实际结果、Evidence、`Remaining`和`Spec Sync`/`Plan Sync`；实现方式变化更新Plan，设计合同变化更新Spec，产品行为或规则变化先取得确认再更新PRD并追加PRD变更记录。无变化写`NO_CHANGE`，不创建文档同步Task。

版本关闭时，在同一次文档收尾中确认该版本全部Plan已完成、没有未处理的`CODE_DRIFT`、`DOC_STALE`或`BLOCKED`，更新`ROADMAP.md`；将已完成且不再被后续版本引用的Spec、Plan和Evidence标记为`SUPERSEDED`并移入`archive/`，仍被后续版本引用的保留原路径。单个Task完成时不归档；根PRD只有在产品基线被新版本正式替代后才归档。

长期项目必须有 `PRD.md`、`docs/ROADMAP.md`、`docs/specs/` 和 `docs/plans/`。`CONTEXT.md`只有出现稳定领域词汇时才创建；只有用户确认将根PRD拆为领域文档时才创建 `docs/prd/`。不创建空目录，其余目录按需创建。

## CONTEXT.md职责

`CONTEXT.md`是人和代理共用的项目领域词汇表，只说明“这个词在本项目中是什么意思、不要叫什么”。它不是产品来源，不能新增或覆盖PRD需求。

只在术语稳定、项目特有且容易混淆时记录；普通编程概念不进入。定义保持1～2句，优先统一一个标准词并列出应避免的近义词。

```markdown
# <项目名称>领域词汇

本项目稳定的产品概念和统一命名。本文件不记录需求与实现。

## Language

**生成任务**：
一次已经提交、可以跟踪状态的模型执行请求。
_Avoid_：生成记录、作业、请求

**生成结果**：
生成任务成功后产生的可使用媒体对象。
_Avoid_：任务、输出任务
```

正文不记录：功能需求、版本、Task、Bug、代码路径、接口签名、Schema、测试步骤或开发日志；文件头仍维护最小`Version`和`Last Updated`。默认只维护根目录一份；不要为了可能出现的未来领域提前建立 `CONTEXT-MAP.md` 或多份词汇表。

Spec、Plan、Task、测试名称和代码命名应使用已确认的标准词。若词汇表与PRD或代码事实冲突，报告冲突并让用户确认，不能自行选择一个来源。

## PRD职责

PRD记录长期产品事实：定位、用户与权限、核心闭环、信息架构、业务规则、数据含义、安全边界、产品验收标准和非目标。

PRD不记录开发版本、Task、Bug、返工、代码路径、接口签名、数据库Schema、测试命令、Commit或开发日志。

根PRD分域后只维护定位、全局边界、事实源优先级和领域索引；稳定产品正文只在`docs/prd/<domain>.md`的一份领域文件中原位维护，`docs/prd/README.md`只负责路由，不复制正文。

### 根PRD模板

```markdown
# 产品需求文档

**Document Version:** `v1.0`
**Status:** `APPROVED`
**Effective Date:** `YYYY-MM-DD`
**Last Updated:** `YYYY-MM-DD`
**Project Type:** `长期商业项目`
**Domain Index:** `docs/prd/README.md`（没有分域时删除）
**Change Log:** `PRD-CHANGELOG.md`

## 产品定位
## 产品目标
## 用户与角色
## 核心用户闭环
## 产品信息架构
## 全局产品规则
## 产品领域索引
## 全局非目标
## 全局验收标准
## 未来能力边界
```

### 领域PRD模板

```markdown
# <领域名称>产品需求

**Document Version:** `v1.0`
**Status:** `APPROVED`
**Parent:** `PRD.md`
**Last Updated:** `YYYY-MM-DD`

## 领域目标
## 使用者与权限
## 产品入口
## 核心用户流程
## 功能需求
## 状态与异常
## 业务规则
## 数据含义
## 安全与权限
## 验收标准
## 非目标
## 依赖领域
```

PRD文档版本和开发版本分开：`PRD v2.1`不等于`0.6.8.1`。

## Spec职责

每个可独立交付单元一份Spec：

```text
docs/specs/0.6.8/0.6.8.1-<topic>-design.md
```

Spec头部至少包含：`Version`、`Status`和`Last Updated`。Spec不建立PRD式变更记录；设计变化直接更新正文并递增`Version`。

至少包含：

```text
Scope
Architecture
Architecture Reuse & Selection（适用时）
Components
UI Compliance：组件复用、设计规范、状态与动效（适用时）
Data Flow
Error Handling
Testing
Out of Scope
PRD Source
```

Spec完成后检查占位符、内部矛盾、范围和歧义，由用户批准后再写Plan。

## Plan职责

一份批准的Spec对应一份Plan：

```text
docs/plans/0.6.8/0.6.8.1-<feature>.md
```

Plan记录准确实现步骤、Task、文件、接口、测试命令、依赖和执行状态。详细格式由 `writing-plans` Skill管理。

## ROADMAP职责

`docs/ROADMAP.md`只记录：当前阶段、当前单元、当前Plan、后续单元和Inbox，不展开任务细节。更新ROADMAP时递增自身`Document Version`并更新`Last Updated`，不建立PRD式变更记录。
