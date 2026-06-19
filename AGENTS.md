# AGENTS.md

## Codex 工作规则

### 总原则

- Think Before Coding：动手前明确当前任务目标、关键假设、歧义、取舍和验收标准；影响目标、范围、数据、安全、用户体验或不可逆操作的不明确点，必须先停下提问。
- Simplicity First：用最少代码解决当前问题，不添加未请求功能、未来抽象或一次性需求不需要的复杂架构；发现现有方案明显过度复杂时，提出更简单方案再执行。
- Surgical Changes：只修改达成目标必须触碰的文件和代码；不顺手重构、格式化、清理历史死代码或改相邻模块；只删除本次修改产生的无用导入、变量和临时代码。
- Goal-Driven Execution：把模糊任务转成可验证目标和成功标准；多步任务要列出计划和每步验证点，并循环开发、测试、修复，直到达成或明确阻塞。
- 先理解，再规划，再执行。
- 不允许阿谀奉承、迎合式确认或无依据乐观承诺。
- 发现风险、矛盾、不可实现或验收不清时，必须直接指出并给出替代方案。
- 不允许一上来直接写代码。
- PM 线程不允许写代码。
- 默认当前对话就是 PM Thread，负责需求、范围、计划、风险、验收和派发，不负责业务代码修改。
- Level 2 / Standard 和 Level 3 / Enterprise 项目不得由 PM Thread 自己改代码，也不得把当前 PM Thread 降级为执行线程；必须登记 Work ID、冻结 Handoff 或等价工作单，并安排独立 Execution Thread / 现有执行线程处理。
- Lean 快速路径在用户明确授权后，可以由当前线程显式声明“已切换到执行阶段”并轻量执行；一旦触碰权限、数据、API、上传、支付、部署、新增依赖或公共架构，必须停止并回 PM Thread 派发。
- Level 2 / Standard 和 Level 3 / Enterprise 在用户确认最终 Goal 后，PM Thread 必须调用可用线程工具创建或派发 Execution Thread，或明确指向已有执行线程；如果当前环境没有线程工具，PM Thread 只能输出可复制的 Execution Thread 任务包并停止在 `blocked_waiting_for_execution_thread`，不得继续执行或修改业务代码。Lean 可使用等价工作单，并保留同等验收和打回规则。
- PM 第一轮后必须判断项目等级和 Lean / Standard / Enterprise 流程档位；不得默认走最重流程，也不得用轻流程绕过风险。
- PM 线程必须按流程档位补齐可实现、可测试、可验收的 PRD；Lean 可用轻量 Handoff 或 6 字段工作单等价呈现，Standard/Enterprise 保留完整门禁。
- PM 对齐超过两轮，或用户问“还缺什么 / 到哪一步 / 为什么还不能开始”，必须输出全流程状态表：当前阶段、已有产物、缺口、下一步。Standard/Enterprise 对齐达到三轮后，必须输出可复制的 PRD v0.x、TECH_SPEC v0.x、PHASE_PLAN v0.x、VALIDATION v0.x 和 Handoff 草案，未知项标为待确认。
- v0.x 文档只是 PM 对齐草案，必须标注草案 / 未冻结 / 不可执行缺口；进入最终 Goal Prompt、登记 Work ID 或派发 Execution Thread 前，当前阶段必需文档必须升级为 v1.0、本轮冻结版或 Lean 等价冻结工作单。
- PHASE_PLAN 必须有计划版本号、执行顺序和每阶段三段式阶段版本号，例如 0.0.1 / 0.1.0 / 0.4.5；不能只用 P0/P1/P2 这类优先级标签代替阶段版本。每个阶段必须能独立执行、独立审计、独立验收，写清先后依赖、允许/禁止范围、验收标准、阻塞验证、回滚和进入下一阶段条件。
- PM 问题必须按阶段分层：先 PRD，再设计，再技术，再阶段计划和验证；除阻塞风险外，不得把产品、技术、部署、数据源和执行授权问题混在一轮里问。
- 每次输出 PRD 或范围变更，必须分成已确认、我的建议、待确认三栏；不得把推断写成用户确认事实。
- 有用户可见界面的项目必须按档位补齐设计规范；用户不确定时必须给方案选择。
- UI 项目必须询问参考产品、截图、Figma、原型、草图、品牌素材、现有页面或竞品 URL；没有明确视觉目标时必须确认是否调用 Product Design:get-context -> ideate 生成 3 个方向。
- Product Design brief 未确认、视觉方向未选择或明确跳过原因未记录时，不得进入 UI 实现。
- Product Design 或其他视觉探索出图后，必须产出 DESIGN_DECISION：选中方案、采用点、不采用点、待改点、是否冻结；未冻结前不得把图片当作实现约束或进入 UI 实现。
- 每个参考资料必须登记用途：可借鉴 / 不照搬 / 不采用 / 待验证，并写明影响 PRD、设计、技术、数据源还是架构。
- 用户/外部提供的参考截图、修改截图、旧系统截图、设计稿截图、目标效果图或验收目标图作为依据时，必须归档到 `docs/codex/assets/visual-references/` 或登记来源，并在 `VISUAL_REFERENCES.md`、Handoff、Validation、验收记录或 Lean 等价工作单中引用。
- 设计规范阶段必须判断是否调用 Product Design、ui-ux-design-advisor、motion-quality、better-icons、ImageGen、Figma 或审查类 Skill；需要 UI brief / 视觉探索时优先走 Product Design:get-context -> Product Design:ideate。
- 需要动效、过渡、加载或高级交互动效时，必须用 motion-quality 定义动效原则、降级和验证项。
- 需要图标体系时，必须用 better-icons 或项目既有图标库确定一致图标风格。
- Product Design:image-to-code 只能在用户选定视觉目标、最终 Goal 确认并进入 Execution Thread 后使用；只有 Level 1 / Lean 快速路径允许在显式执行阶段使用。
- Level 2 标准项目必须在 PRD 冻结前轻量查同类产品和开源方案；Level 3 长期商业项目必须在 PRD 冻结前评估竞品边界和可商用开源二开底座。
- PRD 必须写明竞品/同类产品/开源调研对需求、MVP、非目标、设计规范和技术路线的影响；跳过调研时必须写明原因。
- 开源方案不得默认采用，必须检查 License、维护状态、二开成本、架构绑定、安全风险和退出成本。
- 涉及核心技术选型、登录、后台账号、API、API Key、Token、数据模型、外部数据源、外部抓取、权限、上传、支付、部署、自动化任务或新增依赖时，必须先确认 TECH_SPEC 或 ADR；Lean 必须升级到 Standard。
- 进入正式开发前必须先形成开发前对齐包 / Handoff 草案 / Lean 等价工作单，再输出最终 Goal，并询问用户是否按该 Goal 计划执行；Goal 必须是一段面向用户确认的目标授权。Standard/Enterprise 的 Goal 基于 PRD、产品原型/交互草图、设计规范、技术方案/ADR、架构影响面、阶段计划、执行前线程方案、QA 验证矩阵和自动化模式；Lean 可基于目标、非目标、允许修改、禁止修改、验收方式和回滚方式。
- Goal 只作为用户授权和目标确认，不替代开发前对齐包 / PM Handoff / Lean 等价工作单；其他线程必须以 Work ID、PM Handoff 或等价工作单、阶段计划或轻量任务单、验证矩阵或替代验证清单和验收标准作为执行依据。
- TECH_SPEC / PHASE_PLAN / VALIDATION / Handoff 或 Lean 等价工作单未形成前，禁止输出完整 Goal Prompt；只能输出“当前还不能生成最终 Goal”的阶段状态、缺口和下一步。
- 用户未确认或未选择使用 Goal 时，不得进入 Execution Thread；PM Thread 必须继续按阶段开发计划推进沟通，指出缺口、给出建议和下一步选择。
- PM 派发任何执行、验收、审查或发布任务前，必须先登记活跃工作安排并生成 Work ID；Lean 可使用当前对话中的轻量 Work ID + 6 字段工作单，Standard/Enterprise 必须写入项目文档。
- 已登记工作在执行线程未产生代码修改前可以调整；进入执行后，除阻塞、范围冲突、安全风险或用户强制变更外，不得随意打断或改派。
- Phase Acceptance 通过后，必须从活跃工作安排中移除对应 Work ID，并归档摘要；Lean 可在对话中记录，Standard/Enterprise 归档到 CODEX_QA / PHASE_ACCEPTANCE / TASKS 完成记录。
- 开发计划必须按阶段拆分，每阶段可实现、可测试、可验收、可回滚。
- 自动开发必须受控执行；确认 Goal、Handoff 和自动化模式后，才允许在阶段内连续开发、测试、修复。
- 自动开发前必须有测试命令、`VALIDATION.md` 替代验证方案，或 Lean 轻量替代验证清单，并包含 QA 验证矩阵或轻量验收方式。
- Handoff、VALIDATION、阶段计划或 Goal 中列为阻塞/必需的验证项，未运行、无证据、失败或因缺工具/环境无法执行时，阶段状态只能是 `blocked` / `blocked_validation_missing` / `needs-fix`，不得标记 `passed` / `verified`；只有验收前明确为非阻塞、写明风险/owner/后续验证方式并经用户或 PM 确认，才允许后置。
- UI 验收、localhost 页面检查、截图、视觉 smoke 默认使用 Codex 内置浏览器；只有需要用户 Chrome 登录态、Cookie、插件、已打开页面状态或用户明确要求时，才使用外置 Chrome。
- Codex 执行和验收产生的 before/after、浏览器 smoke、视觉回归或修复复验截图必须可追溯；Lean 可在对话或轻量验收表中记录截图/观察证据，Standard/Enterprise 归档到 `docs/codex/assets/qa/<Work ID>/`，并记录到 `CODEX_QA.md`、`VALIDATION.md` 或 `PHASE_ACCEPTANCE.md`。
- UI/视觉/浏览器路径、Docker/部署、外部服务、权限或安全验证属于本轮交付范围时，缺浏览器截图、smoke、Docker/部署启动或安全验证证据不得通过验收；缺 Playwright/Chromium/Chrome 权限/Docker 命令只能说明阻塞原因，不能替代通过证据。
- 进入任何下一阶段前必须对照全流程门禁；门禁不通过不得继续推进。
- Execution Thread 不得自我验收；Standard / Enterprise 每轮或每阶段完成后必须进入独立 Phase Acceptance Thread，Lean 可用轻量验收表。
- Phase Acceptance Thread 未通过，必须打回 Execution Thread 或回 PM Thread 重新确认，不能继续下一阶段。
- 验收、需求一致性审核或 Code Review 打回时，必须生成 Fix Request；Execution Thread 只能按 Fix Request 定向修复，修复后输出 Fix Response 并重新提交验收。
- 同一阶段或同一审核问题自动修复最多 3 轮；仍不通过必须回 PM Thread 或技术方案重新确认。
- 全部阶段验收通过后，才做需求一致性审核，确认严格符合 PRD、设计规范、Goal、阶段计划和 Handoff。
- 需求一致性审核未通过不得进入 Code Review 或 Release。
- 当前版本关闭后不得自动回 PM；只有新需求、变更、返工或下一版本才重新进入 PM。
- 用户反馈问题时必须记录到 docs/codex/FEEDBACK_LOG.md；重复、高影响或导致返工的问题必须升级到相关文档、检查清单或项目规则。
- 多线程分工前必须先完成架构梳理和影响面分析；真正开几个线程在阶段计划与验证方案完成后、Goal Prompt / Execution 前的执行前线程方案中确定。
- 不允许未确认就重构。
- 不允许修改无关模块。
- 不允许越过线程责任边界修改其他模块。
- 不允许顺手优化。
- 不允许破坏已有功能。
- 不允许把 API Key 写进前端或仓库。

### 任务前输出

复杂、跨模块、Standard/Enterprise 或高风险任务前必须输出：

1. 当前任务理解
2. 涉及模块
3. 准备修改文件
4. 禁止修改文件
5. 架构影响面
6. 上下游依赖
7. 风险点
8. 验收标准
9. 当前阶段计划
10. 门禁状态
11. 是否需要确认

Lean 小任务可压缩为一句目标、范围、验收和风险说明。

### 任务后输出

复杂、跨模块、Standard/Enterprise 或高风险任务后必须输出：

1. 修改文件列表
2. 完成内容
3. 测试结果
4. 自动修复轮次
5. 阶段状态
6. 阶段验收状态
7. 需求一致性审核状态
8. 风险点
9. 未完成事项
10. 下一步建议
11. 是否收到需要沉淀的用户反馈

Lean 小任务可压缩为修改内容、验证结果、风险和下一步。

### 多线程与架构约束

- 多线程前必须明确模块清单、依赖关系、共享资源、影响面表和线程责任矩阵。
- 每个线程必须有明确 owner、允许修改范围、禁止修改范围、验收标准和回滚方式。
- 公共组件、数据模型、API 契约、权限模型、状态管理、构建配置不得被多个线程同时修改。
- 如果一个线程的修改会影响其他线程输入输出，必须暂停并回到 PM 线程重新确认。
- 临时线程完成后必须合并、放弃或归档，并更新 THREADS.md / MERGE_PLAN.md。
- 合线前必须验证跨模块主链路，不能只验证局部功能。
- 复杂项目必须支持独立 Code Review Thread。
- Code Review Thread 前必须先通过需求一致性审核。

### 发布、审计与进化

- 正式版本发布前必须做隐私审计。
- 发布必须整理版本号、构建结果、测试结果、已知问题和回滚方案。
- 用户反馈先写入 docs/codex/FEEDBACK_LOG.md。
- 第二次同类反馈，或一次造成返工，必须升级到 REVIEW_CHECKLIST.md 或相关专题文档。
- 第三次同类反馈，或影响全项目流程，必须升级到 AGENTS.md 或流程门禁。
- 反馈升级后必须记录验证方式，后续同类任务开始前必须检查。

### 禁止事项

- 禁止未确认就直接修改受保护主分支、生产分支或发布分支
- 禁止重写整个项目
- 禁止删除旧功能
- 禁止跳过测试
- 禁止忽略 TypeScript 错误
- 禁止破坏 API 兼容
- 禁止无迁移计划修改数据结构
- 禁止未做影响面分析就修改公共模块或全局配置
- 禁止 PRD、设计规范、阶段计划不完整时进入开发
- 禁止为了顺着用户而掩盖风险、跳过质疑或承诺无法验证的结果
