# Design Brief、Prototype 与 Dev Plan

## Design Brief Builder

有 UI 或用户路径时，AI 自动生成：

```markdown
# DESIGN_BRIEF

## 页面结构
## 核心路径
## 状态 / 空态 / 错误态
## 视觉方向
## 参考依据
## 禁止点
```

用户提供截图、竞品、Figma、旧页面、目标效果图时，先存档到 `docs/codex/assets/visual-references/`，再写入 `docs/codex/VISUAL_REFERENCES.md`。不能入库时写明来源、原因和可引用范围。

设计规范必须把主观感觉翻译成可执行设计决策：

- “高级/专业/轻量/年轻/稳重”等感觉，要落到布局、色彩、字体、间距、密度、组件、动效和状态。
- 每条设计决策都要能被开发和验收对照。
- 不确定的视觉方向给 2-3 个可选方向，等用户选择后再冻结。

## Design Maker

复杂 UI 需要可对照设计依据：

- `docs/codex/PROTOTYPE.md`：低保真页面结构、交互路径、状态说明。
- `docs/codex/DESIGN.md`：视觉规范、组件、响应式、动效。
- 需要出图时再调用设计/生图工具；不强制每次出图。

## Dev Planner

开发前输出 `docs/codex/DEV_PLAN.md`：

```markdown
# DEV_PLAN

## 阶段 / 模块版本
## 模块拆分
## 子线程分工
## 执行顺序
## 依赖关系
## Ownership 表
## 验证方式
## 合并策略
```

Dev Plan 必须写清先后顺序。可以按阶段拆，也可以按模块拆；每个阶段/模块都要有版本号、目标、允许修改、禁止修改、依赖、验收证据和回滚方式。不能独立验收的拆分，不允许交给不同线程并行。

阶段计划要标明发布目标，不默认按商用发布处理。发布目标可为 `none / internal / staging / technical-preview / commercial`。非商用或内部项目不执行完整商业检查；只有明确 `commercial` 或用户要求正式商用发布时，才记录登录/权限/支付/客户数据/部署/监控/回滚等商用发布待补项，并在发布前执行完整检查。

不能并行时，先串行定契约/schema/shared 基础，再并行开发。
