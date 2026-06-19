# 全流程门禁表

## 目标

用一张门禁表把“从项目想法或已有需求到发布复盘”的流程串起来。它用于关键边界检查，不是要求每个小任务都把全表机械跑一遍。

关键边界必须检查本文件：进入开发前、阶段验收前、需求一致性审核/Code Review/发布前、需求变更、验收打回或流程卡住时。Lean 小任务可只检查相关门禁，并说明等价产物在哪里。

## 总规则

- 没有输入，不进入下一阶段。
- 没有明确产物，不进入下一阶段。
- 未判断项目等级和 Lean / Standard / Enterprise 流程档位，不进入 PRD；Lean 快速路径可明确跳过 PRD 文档，直接进入轻量工作单。
- 流程可以按档位压缩，但门禁判断不能消失；压缩时必须说明等价产物在哪里。
- “需求稍微完整”“用户发了 PRD”“用户让整理 Goal”都不等于可执行完整需求。可执行完整需求必须满足当前档位和本轮目标的全部开发前提：项目判断、PRD、调研依据、产品原型、设计规范或无界面说明、技术上下文、阶段计划、执行前线程方案、验证方案、风险/回滚、开发前对齐包、Goal Prompt 和 Handoff 字段都能完整落地；缺任一会影响目标、范围、产品路径、技术方案、验收、验证、风险或回滚判断的字段，仍停留在 PM 对齐。
- Lean 快速路径的“完整落地”可以是聊天内轻量工作单，不要求完整文档集合；但必须明确目标、非目标、允许修改、禁止修改、验收方式和回滚方式。触碰登录、后台账号、权限、数据、API、API Key、Token、上传、支付、部署、自动化任务、外部抓取、外部数据源、新增依赖或公共架构时，必须退出 Lean 快速路径。
- `TECH_SPEC` / `PHASE_PLAN` / `VALIDATION` / Handoff 或 Lean 等价工作单未形成前，禁止输出完整 Goal Prompt；只能输出“当前还不能生成最终 Goal”的阶段状态、缺口和下一步。
- 用户需求涉及 UI、后台、登录、API Key、Token、部署、自动化、外部抓取或外部数据源时，必须先输出全流程状态表和开发前对齐包，再允许生成最终 Goal Prompt。
- PM 对齐超过两轮，或用户质疑“还缺什么 / 为什么还不能开始 / 现在到哪一步”，必须输出最小全流程状态表。Standard/Enterprise 对齐达到三轮后，必须输出可复制的 `PRD v0.x`、`TECH_SPEC v0.x`、`PHASE_PLAN v0.x`、`VALIDATION v0.x` 和 Handoff 草案，未知项标为待确认。`v0.x` 是未冻结草案，必须标注不可执行缺口；最终 Goal Prompt / Work ID / Execution 派发前必须使用 `v1.0`、本轮冻结版或 Lean 等价冻结工作单。
- `PHASE_PLAN` 没有计划版本号、每阶段三段式阶段版本号、执行顺序、前后依赖、每阶段修改边界、独立审计点、独立验收标准、阻塞验证项和进入下一阶段条件时，不进入 Goal Prompt / Execution / Phase Acceptance。不得用 `P0` / `P1` / `P2` 等优先级标签替代阶段版本。
- PM 输出 PRD 或范围变更时，必须分为“已确认 / 我的建议 / 待确认”；没有被用户确认的推断不得写成事实。
- Level 2/3 项目没有 PRD 前期竞品/同类产品/开源方案方向校准，不冻结 PRD。
- 新软件、产品、网站、App、小程序、SaaS、后台或内部系统没有产品原型/交互草图，也没有明确跳过原因和替代依据时，不进入实现。
- 涉及视觉界面时，没有参考产品、截图、Figma、原型、草图、品牌素材、现有页面、竞品 URL、已选视觉方向，或用户明确确认跳过视觉探索，不进入 UI 实现。Product Design 或其他视觉探索出图后，必须产出 `DESIGN_DECISION`：选中方案、采用点、不采用点、待改点、是否冻结；未冻结前不进入 UI 实现。用户/外部截图作为实现依据时，没有在 `VISUAL_REFERENCES.md` 登记存档路径/来源、页面/模块、对照点和确认状态，不进入 UI 实现。
- 每个参考资料必须登记用途：`可借鉴` / `不照搬` / `不采用` / `待验证`，并说明它影响 PRD、设计、技术、数据源还是架构；用途未定时不得让参考项目改变范围。
- 没有验收标准，不进入开发。
- 没有测试命令或替代验证方案，不进入自动开发。
- 没有测试结果，不进入阶段验收。
- Handoff / `VALIDATION.md` / 阶段计划 / Goal 中列为阻塞或必需的验证项，未运行、无证据、失败或因缺工具无法执行时，不得标记 `passed` / `verified`；只能标记 `needs-fix` / `blocked`，并生成阻塞验证缺口或 Fix Request。
- 说明“浏览器截图没完成 / Docker 没有跑 / Playwright 缺浏览器 / Chrome 被系统权限杀掉 / 本地没有 docker 命令”等原因，只能解释阻塞来源，不能替代验收通过证据；在形成最终阻塞结论前，必须先尝试内置浏览器、localhost / preview、临时静态服务、项目 e2e 截图命令、必要外置 Chrome 或 Docker/浏览器安装等恢复路径，并在需要时向用户请求一次明确且窄范围审批。
- UI、前端、可视化、图片/海报/日报卡、管理后台或用户可见页面的交付，截图是强制验收门禁。缺截图时优先生成 Fix Request 或补验证任务；只有用户拒绝审批、账号/外部服务不可获得、工具无法 attach、全部允许路径失败或敏感信息无法脱敏时，才允许 `blocked_validation_missing`，并必须列出已尝试路径、审批记录、失败点和下一步。
- 允许后置项必须在验收前明确为非阻塞，写明风险、owner、后续验证方式和用户/PM 确认；阻塞验证项不得被放入“允许后置项”绕过验收。
- 阶段验收未通过，不进入下一阶段。
- 审查或验收打回时，必须生成 Fix Request；Execution Thread 只能按 Fix Request 定向修复后重新提交验收。
- 执行、验收或打回期间用户补充修改截图、标注截图或目标效果图时，先归档/登记为新的实现依据；若改变范围、交互、视觉目标或验收标准，回到 PM Thread 更新 Handoff / Fix Request，不得直接扩大执行范围。
- 同一阶段或同一审核问题自动修复最多 3 轮；仍失败则回 PM Thread 或技术方案重新确认。
- 全部阶段验收未通过，不进入需求一致性审核。
- 需求一致性审核未通过，不进入代码审查。
- 有 P0 / 阻塞风险，不进入发布。
- 用户未确认 Goal，不进入 Execution Thread；但 PM Thread 必须继续按阶段开发计划沟通缺口、风险、建议和下一步选择。
- Goal Draft / Goal Prompt 不是执行授权。只有用户明确说“按这个 Goal 执行 / 开始开发 / 进入 Execution”等，才进入执行授权。
- 默认当前对话是 PM Thread。Level 2 / Standard 和 Level 3 / Enterprise 在执行授权后，也不得由 PM Thread 自行改代码，且不得把当前 PM Thread 降级为执行线程；必须实际派发到 Execution Thread 或明确指向已有执行线程。线程工具不可用时，PM Thread 只能输出可复制的 Execution Thread 任务包并停止，状态记为 `blocked_waiting_for_execution_thread`。
- 多线程不能拖到 Goal 执行时临时决定。PM 早期只能预判；技术方案/架构影响面阶段只做可拆性分析；阶段计划与验证方案完成后、Goal Prompt / Execution 前，必须输出执行前线程方案并确定 single-thread / N threads / defer，缺线程责任、数据/API 契约、验证矩阵、合并顺序或回滚方式时不得并行开发。
- PM 未登记 PM 台账 / 活跃工作安排、未生成 Work ID 或 Handoff 未引用 Work ID，不进入 Execution Thread。Lean 快速路径可使用聊天内轻量 Work ID 和 6 字段工作单作为等价登记；Standard/Enterprise 必须写入 `TASKS.md` 或等价项目文档。PM 台账只保留未完成活跃任务；Phase Acceptance 通过后必须从活跃区删除该 Work ID 条目并归档摘要。
- 未明确自动化模式时，不进入 Execution Thread；如用户未指定，PM Thread 可在 Goal 中建议 Assisted Autopilot，并取得用户确认。高风险任务必须使用 Manual。
- 发现风险、矛盾或不可实现点时，必须直接指出，不得迎合式推进。
- 用户反馈流程或执行问题时，不等版本结束，必须先记录到 `FEEDBACK_LOG.md`；重复、高影响或导致返工的问题必须升级到相关文档或检查清单。

## 门禁表

| 阶段 | 输入 | 必须产出 | 通过条件 | 不通过时 |
| --- | --- | --- | --- | --- |
| 0. 启动 | 粗略想法、半成型需求或可执行完整需求材料 | 输入成熟度判断、必要 PM 问题、项目等级、流程档位 | 已识别项目类型、复杂度、流程重量、现有材料和升级风险；已有材料不重复逼问 | 继续 PM 追问、整理材料或要求用户补充关键输入 |
| 1. PRD 前期竞品/同类产品方向校准 | 项目定位、MVP 初稿、现有基础、项目等级 | `PRODUCT_RESEARCH.md` 或 PM Handoff 调研结论 | Level 1 已明确跳过或轻量参考；Level 2 已轻量联网扫描；Level 3 已做竞品边界和可商用二开评估；无法联网时假设已标明 | 补调研，或明确跳过/从零实现原因 |
| 2. PRD | 项目定位、MVP、现有基础、调研结论 | `PRD.md` 或 PM Handoff 中的完整 PRD | 功能、角色、流程、数据、权限、验收可实现；已写明调研对需求/MVP/非目标的影响 | 继续追问或给方案选择 |
| 3. 产品原型与设计规范 | PRD、调研结论、参考产品、用户偏好、用户/外部提供的截图/Figma/原型/品牌素材或明确跳过原因 | `DESIGN.md` / `VISUAL_REFERENCES.md` / Product Design brief / `DESIGN_DECISION` / 产品原型或交互草图结论 | 新软件/产品/网站/App/小程序/SaaS/后台/内部系统已有产品原型或交互草图；已询问参考产品、截图、Figma、原型、草图、品牌素材或竞品 URL；作为实现依据的截图已归档或登记来源、页面/模块、对照点、禁止点和确认状态；design brief 已确认；Product Design 出图后已记录选中方案、采用点、不采用点、待改点和是否冻结；页面、组件、状态、响应式、可访问性、动效原则、图标风格明确；必要的 Product Design / ui-ux-design-advisor / motion-quality / better-icons / 生图 / Figma 调用已完成或明确跳过原因；需要视觉目标时用户已选定方向且已冻结或明确未冻结 | 继续追问参考材料，调用 Product Design:get-context -> ideate，给 2 到 3 个方案或生成草图再确认 |
| 4. 技术方案与架构 | PRD、产品原型、设计规范、调研结论、现有代码、流程档位 | `TECH_SPEC.md` 或 Handoff 技术方案、模块清单、依赖关系、影响面表、多线程可拆性分析 | Lean 已在 Handoff 写明技术边界；Standard/Enterprise 涉及 API/数据/权限/部署/依赖时已有技术方案；修改范围、禁止范围、共享资源、风险模块和候选拆分点明确 | 回到技术方案或架构梳理 |
| 5. 阶段计划与验证方案 | PRD、产品原型、设计、调研结论、技术方案、架构影响面 | `PHASE_PLAN.md` / `VALIDATION.md` / 执行前线程方案 / 开发前对齐包 / Handoff 草案 / Goal 就绪判断 | `PHASE_PLAN` 有计划版本号和本轮状态；每阶段有三段式阶段版本号、执行顺序、前置/后续依赖、目标、任务、修改范围、禁止范围、输入、输出、独立审计点、独立验收标准、阻塞验证项、回滚方式和进入下一阶段条件；QA 验证矩阵可执行；已确定 single-thread / N threads / defer；如需多线程，线程责任矩阵、数据/API 契约、合并顺序、回滚策略和跨模块验证矩阵明确；Handoff 草案可支持执行；若前置产物缺失，只能输出 Goal 未就绪说明 | 重拆计划、补验证方案，或回架构阶段重做可拆性分析 |
| 6. Goal Prompt / 执行授权 | Goal 就绪判断、开发前对齐包、Handoff 草案、执行前线程方案、技术方案/ADR、阶段计划、当前 Task、自动化模式、QA 验证矩阵 | 一段式 Goal Prompt、用户明确执行授权记录、执行线程安排、派发证据 | `TECH_SPEC` / `PHASE_PLAN` / `VALIDATION` / Handoff 或 Lean 等价工作单已形成；`PHASE_PLAN` 已冻结到本轮版本，当前阶段有三段式阶段版本号，且可独立审计验收；Goal Prompt 只承载授权目标，不替代 Handoff；用户明确同意按最终 Goal Prompt 正式进入开发，自动化模式明确，QA 验证矩阵可执行；Level 2/3 已实际创建/派发独立 Execution Thread 或已明确已有执行线程 ID/链接；多线程时每个线程的 Goal 字段写入 Handoff，而不是把 Goal Prompt 写成长文档 | 不进入 Execution；如线程工具不可用，输出 Execution Thread 任务包并标记 `blocked_waiting_for_execution_thread`；否则继续按阶段计划沟通缺口、建议和下一步选择 |
| 7. Execution Thread | Work ID、PM Handoff、当前 Task、或 Fix Request | 代码修改、测试结果、自动修复记录、Fix Response | 当前阶段测试通过或阻塞原因明确；被打回时已逐条回应 Fix Request | 自动修复，最多 3 轮；仍失败则停止 |
| 8. Phase Acceptance Thread | Work ID、阶段计划、Handoff、执行结果、测试结果、验证证据 | `PHASE_ACCEPTANCE.md` 或等价验收表；不通过时输出 Fix Request；通过时从 PM 台账活跃区删除该 Work ID 条目并归档摘要 | 当前阶段计划项全部完成；全部阻塞验证项已运行且有可追溯证据；未运行、失败、缺工具或无证据的验证项均已判定为非阻塞并有确认记录；Lean 可用轻量验收表 | 生成 Fix Request 打回 Execution Thread；缺验证工具或环境时标记 `blocked` 并给出补验证路径；验收标准问题回 PM Thread 重新确认 |
| 9. 需求一致性审核 | PRD、产品原型、设计规范、Goal、阶段计划、Handoff、全部阶段验收结果 | `ACCEPTANCE.md` 或等价审核表；不通过时输出 Fix Request | 无漏做、错做、多做、越界修改；偏差已确认 | 生成 Fix Request 回 Execution Thread，或回 PM Thread 重新确认 |
| 10. Code Review Thread | 已完成代码、测试结果、影响面、需求一致性审核 | 审查发现清单；P0/P1 输出 Fix Request | 无 P0；P1 有处理计划 | 生成 Fix Request 回 Execution Thread 修复 |
| 11. Release Thread | 审查结果、构建结果 | 隐私审计、版本文档、回滚方案 | 隐私、构建、发布后主链路验证通过 | 阻塞发布 |
| 12. Version Close | 发布结果、版本文档、验收记录 | 当前版本关闭记录 | 当前版本目标完成或明确终止 | 不回 PM，除非有新需求/变更/返工 |
| 13. Feedback Evolution | 用户反馈、发布/审查/返工记录 | `FEEDBACK_LOG.md`、决策、上下文、检查清单或项目规则更新 | 可复用规则已记录；重复或高影响问题已升级 | 补写文档，或回到相关阶段修正 |

## Lean 快速路径最小输出

低风险小任务可输出下面的轻量门禁，不必展开全流程表：

```markdown
## Lean 快速路径

- Work ID：
- 目标：
- 非目标：
- 允许修改：
- 禁止修改：
- 验收方式：
- 回滚方式：
- 流程判断：Lean / single-thread / 不触碰高风险项
- Goal 确认：等待确认 / 已确认
```

只要出现登录、后台账号、权限、数据、API、API Key、Token、上传、支付、部署、自动化任务、外部抓取、外部数据源、新增依赖、公共组件重构、生产风险或验收不清，立即升级到 Standard 或回 PM Thread 补齐完整门禁。

## 阶段状态

每个阶段只能处于一种状态：

- `blocked`：缺关键输入或存在 P0 风险。
- `blocked_waiting_for_execution_thread`：Level 2/3 已有执行授权和任务包，但没有可用线程工具或尚未完成执行线程派发；PM Thread 必须停止，不得改代码。
- `blocked_validation_missing`：阻塞验证项未运行、无证据、失败或缺工具无法执行；对截图、浏览器 smoke、Docker/部署启动等强制验证项，必须先尝试可执行恢复路径并请求必要审批后仍失败，才允许使用本状态。不得进入下一阶段、需求一致性审核、Code Review 或 Release。
- `ready`：输入完整，等待用户确认。
- `in_progress`：正在执行。
- `verified`：产物和验收通过。
- `deferred`：明确后置，并写入非目标或后续计划。

不得把 `blocked` 写成 `ready`。

## 最小全流程输出

当用户要求“对齐全部流程”、PM 对齐超过两轮、用户质疑“还缺什么 / 为什么还不能开始 / 现在到哪一步”，或需求涉及 UI、后台、API Key、Token、部署、自动化、外部抓取、外部数据源时，输出：

```markdown
## 全流程对齐

| 阶段 | 当前状态 | 已有产物 | 缺口 | 下一步 |
| --- | --- | --- | --- | --- |
| 启动 |  |  |  |  |
| 项目等级 / 流程档位 |  |  |  |  |
| PRD 前期竞品 / 同类产品方向校准 |  |  |  |  |
| PRD |  |  |  |  |
| 产品原型 / 设计规范 |  |  |  |  |
| 技术方案 / 架构影响面 |  |  |  |  |
| 阶段计划 / 验证方案 |  |  |  |  |
| 开发前对齐包 / Handoff 草案 |  |  |  |  |
| Goal Prompt / 执行授权 |  |  |  |  |
| Execution |  |  |  |  |
| 阶段验收 |  |  |  |  |
| 需求一致性审核 |  |  |  |  |
| Code Review |  |  |  |  |
| Release |  |  |  |  |
| Version Close |  |  |  |  |
| Feedback Evolution |  |  |  |  |
```

## 回退规则

- PRD 变更：回到 PRD 阶段，并重新检查设计、架构、阶段计划。
- 产品原型或设计规范变更：回到产品原型/设计阶段，并重新检查前端任务、交互路径和验收。
- 数据模型/API/权限变更：回到架构阶段，并重新检查多线程边界。
- 测试失败：留在 Execution Thread，自动修复，不能进入阶段验收。
- 阶段验收失败或阻塞验证缺失：打回 Execution Thread；缺工具或环境时补齐验证路径，无法补齐则状态为 `blocked_validation_missing`；如果是计划或验收标准问题，回 PM Thread。
- 需求一致性审核失败：回 Execution Thread 修复；如果是需求矛盾，回 PM Thread。
- 审查 P0：回 Execution Thread 修复。
- 隐私或发布 P0：阻塞发布。
- 用户改变目标：回 PM Thread 重写 Goal。
- 当前版本关闭后，不自动回 PM；只有新需求、变更、返工或下一版本才重新进入 PM Thread。
