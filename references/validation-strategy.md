# 测试与替代验证方案

## 目标

解决“项目没有现成测试，自动开发怎么验收”的问题。

自动开发前必须先识别验证方式：

- 有测试脚本：使用现有测试脚本。
- 没有测试脚本但可补轻量测试：先补最小测试或检查命令。
- 暂时不能补测试：生成 `VALIDATION.md` 替代验证方案。
- 连替代验证都无法定义：不得进入自动开发。

## 测试识别顺序

优先查找：

- `package.json`：`test`、`typecheck`、`lint`、`build`、`e2e`、`preview`。
- `Makefile`、`justfile`、`taskfile`。
- 框架命令：Next/Vite/Vue/Svelte、Expo、Flutter、Tauri、Electron、小程序 CLI。
- 后端命令：unit、integration、migration、seed、API smoke。
- CI 配置：GitHub Actions、GitLab CI、Vercel、Netlify。

## 替代验证方式

按项目类型选择：

- Web / SaaS：typecheck、lint、build、内置浏览器或 Playwright 冒烟、关键页面截图、核心路径手动清单。
- 小程序：构建/预览、页面路径检查、登录/授权/支付/表单手动清单。
- App：构建、模拟器冒烟、核心页面导航、权限弹窗、崩溃检查。
- 后台系统：列表/筛选/表单/权限/批量操作主链路。
- API：健康检查、核心接口请求、错误码、权限、schema 兼容。
- 数据库：迁移 dry-run、回滚计划、数据兼容检查。
- AI 功能：输入输出样例、失败兜底、敏感数据检查、费用/速率限制。

## 浏览器验收策略

UI 验收、截图和本地页面检查不要默认使用外置 Chrome。

默认顺序：

1. Codex 内置浏览器：用于 localhost、预览地址、静态页面、普通 UI smoke、截图、响应式检查和视觉回归取证。
2. Playwright 或项目已有 e2e 工具：用于可脚本化的自动冒烟、截图对比、路由巡检和回归路径。
3. 外置 Chrome：只在需要用户本机 Chrome 的登录态、Cookie、浏览器插件、已打开页面、真实账号会话、第三方授权状态，或用户明确要求时使用。

使用外置 Chrome 前必须说明原因。不能因为要截图或看页面就默认外置 Chrome。

验收证据至少记录：

- 使用的浏览器：内置浏览器 / Playwright / 外置 Chrome。
- 访问地址。
- 视口尺寸。
- 截图或观察证据。
- 不能使用默认内置浏览器的原因。

截图证据必须可追溯：

- 用户/外部提供的参考截图、修改截图、目标效果图、验收目标图，引用 `VISUAL_REFERENCES.md` 中的 ID 或存档路径。
- Codex 执行/验收产生的 before/after、smoke、回归或修复复验截图存入 `docs/codex/assets/qa/<Work ID>/`，并在 `VALIDATION.md`、`CODEX_QA.md` 或 `PHASE_ACCEPTANCE.md` 中记录。
- UI 修改类任务至少保留可对照的 before/after 或参考/实现截图；无法截图时必须写明原因和替代观察证据。
- 验收或修复期间用户新增的截图先登记为新的 `VISUAL_REFERENCES.md` 依据，再进入 Fix Request 或 Handoff 更新。
- 截图含敏感信息时先脱敏；不能脱敏时记录不可入库原因，不提交原图。

## QA 验证矩阵

`VALIDATION.md` 必须区分验证类型，不要只写一个笼统测试命令。

最小矩阵：

- 自动测试：typecheck、lint、unit、integration、build、e2e。
- 人工主链路：用户最核心路径、关键表单、关键页面、权限入口。
- 回归检查：本次修改可能影响的旧功能。
- 发布后 smoke：上线或构建后必须快速确认的路径。
- 不可自动验证项：需要人工、外部系统、真实账号或生产环境才能确认的项目。

Lean 可以只保留自动测试和人工主链路；Standard 必须包含回归检查；Enterprise 必须包含发布后 smoke、隐私/安全专项和不可自动验证项。

## VALIDATION.md 最小模板

```markdown
# VALIDATION.md

## 验证策略

- 项目类型：
- 流程档位：
- 当前阶段：
- 是否有现成测试：
- 使用的验证方式：
- 浏览器验收工具：内置浏览器 / Playwright / 外置 Chrome / 不需要
- 使用外置 Chrome 原因：
- 参考截图 / 视觉依据：
- 执行/验收截图归档目录：docs/codex/assets/qa/<Work ID>/

## 自动命令

| 命令 | 用途 | 是否阻塞 |
| --- | --- | --- |
|  |  | yes/no |

## 替代验证清单

| 路径/功能 | 操作 | 预期结果 | 结果 |
| --- | --- | --- | --- |
|  |  |  | pending |

## QA 验证矩阵

| 类型 | 覆盖范围 | 方法 | 是否阻塞 | 结果 |
| --- | --- | --- | --- | --- |
| 自动测试 |  |  | yes/no | pending |
| 人工主链路 |  |  | yes/no | pending |
| 回归检查 |  |  | yes/no | pending |
| 发布后 smoke |  |  | yes/no | pending |
| 不可自动验证项 |  |  | yes/no | pending |

## 浏览器验收证据

- 使用工具：内置浏览器 / Playwright / 外置 Chrome / 不需要
- 地址：
- 视口：
- 参考截图 ID：
- before 截图：
- after 截图：
- 截图/观察证据：
- 使用外置 Chrome 原因：

## 不能自动验证的部分

-

## 阻塞项

-
```

## 阻塞规则

- 没有任何测试或替代验证方案：不得进入自动开发。
- 自动命令失败且无法解释：不得进入 Phase Acceptance Thread。
- 替代验证清单没有覆盖当前阶段核心路径：不得标记阶段通过。
- QA 验证矩阵没有覆盖当前流程档位要求：不得进入阶段验收。
- 涉及安全、权限、支付、上传、隐私时，必须有专门验证项。
