# 帧芯开发工作流 5.8

帧芯开发工作流是一个面向长期、多模块商业软件项目的 Codex Skill Pack。它把产品需求、UI 设计、架构选型、版本计划、代码实现、验收和发布治理串成一条可追踪的开发链路，同时保持简单任务的开发速度。

## 解决什么问题

- 让长期项目按版本和交付单元推进，不再依赖聊天记录记忆阶段。
- 新页面或重大 UI 改动先确认真实交互，再进入实现，减少“功能完成后才返工 UI”。
- 用 Spec、Plan、Task 和证据记录明确边界，避免 AI 顺手增加未批准功能或过度工程化。
- 让子智能体按功能批次并行开发，控制共享文件、状态、接口和 worktree 冲突。
- 在真实入口完成产品验收，并在代码再次变化时自动使旧 PASS 证据失效。
- 区分本地开发、测试环境和正式发布的授权边界：本地测试以效率为主，生产发布才严格收口。

## 核心流程

```text
指定 PRD
  → 适度需求访谈
  → 必要时架构复用调研
  → 必要时 Visual Companion UI 确认
  → Spec 批准
  → Implementation Plan 批准
  → 子智能体按功能批次开发
  → 一次独立 Review
  → 最新完整验证
  → 真实产品验收
  → 分支收尾
  → 正式发布风险审查与发布治理
```

单文件修改、确定性小 Bug、文案和样式微调不会强制走完整流程。

## Skill 组成

包内共有 20 个 Skill：

- 产品与设计：`brainstorming`、`product-spec-governance`
- 计划与执行：`writing-plans`、`executing-plans`、`subagent-driven-development`
- 并行与隔离：`dispatching-parallel-agents`、`using-git-worktrees`
- 工程质量：`test-driven-development`、`systematic-debugging`、`requesting-code-review`、`receiving-code-review`、`verification-before-completion`
- 验收与交付：`product-acceptance`、`finishing-a-development-branch`
- 正式发布：`release-risk-review`、`release-governance`
- 工作流维护：`writing-skills`、`optimizing-development-workflow`、`uninstall-development-workflow`

其中 18 个常用 Skill 默认允许隐式调用；工作流复盘和卸载是显式调用 Skill，避免误触发。

## 使用方式

在 Codex 中明确启动：

```text
使用帧芯开发工作流，基于我指定的 PRD 推进当前版本。
```

也可以直接调用某个阶段：

```text
$zhenxin-development-workflow:brainstorming
$zhenxin-development-workflow:writing-plans
$zhenxin-development-workflow:subagent-driven-development
$zhenxin-development-workflow:product-acceptance
```

复盘和卸载必须明确调用：

```text
$zhenxin-development-workflow:optimizing-development-workflow
$zhenxin-development-workflow:uninstall-development-workflow
```

## 包结构

```text
.
├── .codex-plugin/plugin.json   # 插件名称、版本和界面信息
├── skills/                     # 20 个运行时 Skill
├── scripts/                    # 包校验、上下文审计、代码热点扫描
├── tests/                      # 路由场景和脚本烟测
├── NOTICE.md                   # 上游来源、许可和版本记录
├── LICENSE                     # MIT 许可
└── README.md
```

业务项目的 PRD、Spec、Plan、Task、截图和发布记录应保存在业务项目自己的 `docs/` 目录，不放入本仓库。

## 维护与验证

修改 Skill 前先检查相邻 Skill、reference、脚本和测试。完成后运行：

```bash
python3 scripts/validate-package.py
bash tests/workflow-scripts-smoke.sh
python3 scripts/audit-context.py
```

主 Skill 只保留路由、边界和关键门禁；详细模板和例外放在对应的 `references/`，避免上下文膨胀。

## 版本

当前版本：`5.8.0`

- `5.6`：PRD 唯一事实源、领域索引、变更记录和文档归档。
- `5.7`：代码或合同变化后旧 PASS 证据自动失效并重新验证。
- `5.8`：最小实现边界、本地/测试/生产执行模式、Task 继承、返工证据和完成状态统一。

## 来源与许可

通用开发方法基于 MIT 许可的 [obra/superpowers](https://github.com/obra/superpowers)，并参考 [oil-oil/oil-frontend](https://github.com/oil-oil/oil-frontend) 的前端实施规则。本项目的适配范围和许可说明见 [NOTICE.md](NOTICE.md)。
