# 测试与替代验证方案

## 目标

解决“项目没有现成测试，自动开发怎么验收”的问题。

自动开发前必须先识别验证方式：

- 有测试脚本：使用现有测试脚本。
- 没有测试脚本但可补轻量测试：先补最小测试或检查命令。
- 暂时不能补测试：生成 `VALIDATION.md` 替代验证方案；Lean 快速路径可在轻量工作单中写替代验证清单。
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
- Docker / 部署：`docker compose config`、镜像构建、容器启动、健康检查、关键接口/页面 smoke、日志无启动错误；无法本地跑时使用 CI、远端环境或用户本机验证回执替代，不能仅凭 Docker 文件存在判定通过。

## 阻塞验证与后置验证

每个验证项必须在开发前或提交验收前分级：

- `blocking`：本轮验收必须完成。未运行、失败、无证据、缺工具或缺环境时，阶段状态只能是 `blocked_validation_missing` / `blocked` / `needs-fix`。
- `non-blocking`：可后置。必须在验收前写明原因、风险、owner、后续验证方式和用户/PM 确认。

不得在验收阶段临时把失败或未运行的 `blocking` 验证项改写成“允许后置”。缺 Playwright、Chromium、Chrome 权限、Docker 命令、账号、外部服务或部署环境，只能说明阻塞原因，不能替代通过证据；但在标记阻塞前，必须先按本文件的强制恢复路径尝试补齐，必要时向用户请求一次明确审批。

典型阻塞验证项：

- UI、视觉或浏览器路径在本轮范围内：必须有内置浏览器 / Playwright / 外置 Chrome 的 smoke、截图或可追溯观察证据。
- 生成图片、日报卡、海报或可视资产在本轮范围内：必须有尺寸、格式、关键视觉结果或截图证据。
- Docker、部署、服务器、CI 或发布在本轮范围内：必须有本地、CI、远端或用户本机的启动/健康检查证据。
- 登录、权限、Token、API Key、隐私、安全在本轮范围内：必须有对应负向/正向验证或扫描结果。

## 浏览器验收策略

UI 验收、截图和本地页面检查不要默认使用外置 Chrome。

默认顺序：

1. Codex 内置浏览器：用于 localhost、预览地址、静态页面、普通 UI smoke、截图、响应式检查和视觉回归取证。
2. Playwright 或项目已有 e2e 工具：用于可脚本化的自动冒烟、截图对比、路由巡检和回归路径。
3. 外置 Chrome：只在需要用户本机 Chrome 的登录态、Cookie、浏览器插件、已打开页面、真实账号会话、第三方授权状态，或用户明确要求时使用。

使用外置 Chrome 前必须说明原因。不能因为要截图或看页面就默认外置 Chrome。

### 强制截图恢复路径

涉及 UI、前端、可视化、图片/海报/日报卡、管理后台或用户可见页面时，截图是 `blocking` 验收项。不能因为截图工具第一次失败就进入“验证缺口”。

执行顺序：

1. 先用 Codex Browser Plugin 内置浏览器打开目标页面并调用截图。
2. 如果目标是本地页面、静态文件、构建产物或 `file://` / `data:` 被策略拦截，不得停下；启动项目自己的 dev server / preview，或在只读静态目录上启动临时 `localhost` / `127.0.0.1` 静态服务后再截图。
3. 如果服务未启动、端口占用、需要安装浏览器、需要运行 Docker、需要外置 Chrome 登录态或需要更高权限，先向用户请求一次明确且窄范围的审批；可建议用户批准可复用的命令前缀，例如项目 dev server、`python3 -m http.server`、`npx playwright install` 或 `docker compose up`，但不得请求宽泛脚本权限。
4. 如果项目已有 e2e / visual regression / screenshot 命令，优先复用项目命令；命令失败时记录日志并回到浏览器手动 smoke 截图。
5. 只有在用户拒绝审批、账号/外部服务不可获得、Browser 无法 attach、所有允许路径均失败，或截图会泄露无法脱敏的敏感信息时，才能标记 `blocked_validation_missing`。此时必须写清已尝试路径、失败点、还缺什么审批/环境/账号和下一步补验证方式。

禁止把“Playwright 没装 Chromium”“Chrome headless 被系统杀掉”“本地没有 Docker”“`file://` 被拦截”“当前没有浏览器截图工具”写成通过后的备注。对本轮 UI 交付而言，这些只能触发继续补截图、请求审批或阻塞。

验收证据至少记录：

- 使用的浏览器：内置浏览器 / Playwright / 外置 Chrome。
- 访问地址。
- 视口尺寸。
- 截图或观察证据。
- 不能使用默认内置浏览器的原因。
- 如曾失败：已尝试的恢复路径、请求过的审批和最终失败点。

截图证据必须可追溯：

- 用户/外部提供的参考截图、修改截图、目标效果图、验收目标图，引用 `VISUAL_REFERENCES.md` 中的 ID 或存档路径。
- Codex 执行/验收产生的 before/after、smoke、回归或修复复验截图必须可追溯；Lean 可在对话或轻量验收表中记录截图/观察证据，Standard/Enterprise 存入 `docs/codex/assets/qa/<Work ID>/`，并在 `VALIDATION.md`、`CODEX_QA.md` 或 `PHASE_ACCEPTANCE.md` 中记录。
- UI 修改类任务至少保留可对照的 before/after、参考/实现截图或轻量观察证据；若本轮交付包含用户可见页面、视觉变化或图片产物，截图不得被普通观察证据替代。
- 如果截图、浏览器 smoke 或视觉对照在 Handoff / `VALIDATION.md` / 阶段计划中是 `blocking`，无法截图或缺浏览器工具时不得验收通过；必须先执行强制截图恢复路径并请求必要审批，仍失败才标记 `blocked_validation_missing`。
- 验收或修复期间用户新增的截图先登记为新的 `VISUAL_REFERENCES.md` 依据，再进入 Fix Request 或 Handoff 更新。
- 截图含敏感信息时先脱敏；不能脱敏时记录不可入库原因，不提交原图。

## QA 验证矩阵

创建 `VALIDATION.md` 时必须区分验证类型，不要只写一个笼统测试命令。Lean 快速路径可以不建独立文件，但轻量工作单里的验收方式也必须可执行。

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
- 截图恢复路径：内置浏览器 / localhost dev server / 临时静态服务 / e2e 截图命令 / 外置 Chrome / 不需要
- 已请求审批：
- 参考截图 / 视觉依据：
- 执行/验收截图归档目录：docs/codex/assets/qa/<Work ID>/

## 自动命令

| 命令 | 用途 | 阻塞级别 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
|  |  | blocking / non-blocking | pending / passed / failed / skipped |  |

## 替代验证清单

| 路径/功能 | 操作 | 预期结果 | 阻塞级别 | 结果 | 证据 |
| --- | --- | --- | --- | --- | --- |
|  |  |  | blocking / non-blocking | pending / passed / failed / skipped |  |

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
- 截图恢复路径与审批记录：

## 不能自动验证的部分

| 项目 | 原因 | 阻塞级别 | 替代验证 / 后续 owner | 是否允许后置 |
| --- | --- | --- | --- | --- |
|  |  | blocking / non-blocking |  | yes/no |

## 阻塞项

| 项目 | 原因 | 需要的工具/环境 | 下一步 |
| --- | --- | --- | --- |
|  |  |  |  |
```

## 阻塞规则

- 没有任何测试或替代验证方案：不得进入自动开发。
- 自动命令失败且无法解释：不得进入 Phase Acceptance Thread。
- 替代验证清单没有覆盖当前阶段核心路径：不得标记阶段通过。
- QA 验证矩阵没有覆盖当前流程档位要求：不得进入阶段验收。
- 任一 `blocking` 验证项未运行、失败、无证据或因缺工具无法执行：不得标记阶段通过。
- 浏览器截图、UI smoke、Docker/部署启动验证属于本轮范围且为 `blocking` 时，缺浏览器、缺 Docker 或缺权限不能直接跳过；必须先请求必要审批并尝试可执行恢复路径。全部失败或审批被拒后，只能标记为 `blocked_validation_missing`，不得用“已说明原因”替代通过。
- 涉及安全、权限、支付、上传、隐私时，必须有专门验证项。
