---
name: writing-skills
description: 在维护帧芯开发工作流自身或创建配套Codex Skill时，用于按真实触发条件编写、测试和验证Skill，避免把一次性问题堆成通用流程规则。
---

# 编写与维护Skill

Skill是给另一个Codex实例使用的决策指导，不是面向人的长篇说明书。

## 何时创建

- 同一种非显然方法会反复使用；
- 特定风险需要稳定门禁；
- 工具、格式或领域规则需要准确路由；
- 已有Skill无法通过小修改合理覆盖。

一次性经验、项目私有细节、已有官方文档和普通常识不应新建Skill。优先修正现有Skill，避免重复和冲突。

## 结构

```text
skill-name/
├── SKILL.md
├── agents/openai.yaml       # 可选
├── references/              # 按需
├── scripts/                 # 可重复、确定性的操作
└── assets/                  # 交付素材，不作为指令
```

`SKILL.md` frontmatter必须包含 `name` 和能准确说明“何时使用”的 `description`。名称使用英文小写短横线；正文和面向用户的输出使用中文，代码、命令和接口名保留原文。

## 渐进披露

- description只负责发现和边界；
- SKILL.md保留共同流程、关键约束和reference路由；
- 大型模板、模式、API和条件分支放到references；
- 确定性重复操作才写脚本；
- 不创建空目录、README、重复速查表或无调用方资源。

## Skill的RED-GREEN-REFACTOR

### RED

先写真实压力场景或观察当前Skill的失败行为：误触发、漏触发、越权、跳步骤、过度流程或输出错误。没有失败案例不要凭感觉叠规则。

### GREEN

加入能修正该失败的最小指令、边界或脚本。不要为假设中的未来问题写万能流程。

### REFACTOR

删除重复、模糊和可由模型常识完成的内容；把条件细节下沉到references；确认没有与用户或项目指令冲突。

## 验证

1. 运行Skill结构验证器；
2. 检查所有相对链接和脚本路径；
3. 运行新增或修改脚本；
4. 检查description不会吸引不相关任务；
5. 对复杂或高风险Skill用独立上下文做前向测试；
6. 未经用户确认不安装到全局Skill目录。

复杂行为Skill还要读取 [behavior-tests.md](references/behavior-tests.md)，至少验证应触发、不应触发和压力场景。不要恢复长篇Skill教程或为每条历史问题增加规则。

针对帧芯工作流的修改，还必须：

- 运行包根目录 `scripts/validate-package.py`；
- 使用 `tests/workflow-routing-cases.md` 做独立上下文前向测试；
- 检查简单任务不会触发总工作流；
- 检查未授权操作、UI确认和Review频率没有回退。
