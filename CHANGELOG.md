# CHANGELOG.md

## Unreleased

### Added

- 初始化橙影 Codex 企业级工作流技能包。

### Changed

- 新增截图与视觉证据存档规则：用户提供的参考截图、修改截图、旧系统/设计稿/验收截图需归档到 `docs/codex/assets/visual-references/` 或记录来源；执行和验收截图归档到 `docs/codex/assets/qa/<Work ID>/`，并在 `VISUAL_REFERENCES.md`、Handoff、Validation、QA 和 Phase Acceptance 中引用。
- 重新审视上下文后统一 Goal / Handoff / 执行线程关系：开发前先形成对齐包和 Handoff 草案，再输出一段式 Goal；Goal 只承载授权目标，不替代执行上下文；复制给其他 Codex 时必须同时提供对齐包或 Handoff。
- 放松 `AGENTS.md` 中过硬的执行规则：Execution Thread 优先新开但允许无线程工具时在当前线程显式切换；Lean 小任务可压缩任务前后输出；主分支限制改为受保护/生产/发布分支需确认。
- 明确多线程判断时机：PM 第一轮只做预判；技术方案/架构影响面阶段只做可拆性分析；阶段计划与验证方案完成后，在 Goal Prompt / Execution 前输出执行前线程方案并确定 single-thread / N threads / defer，缺线程责任、数据/API 契约、验证矩阵、合并顺序或回滚策略时不得并行开发。
- 明确 `可执行完整需求` 判定标准：必须满足当前流程档位和本轮目标下进入开发前的全部必需前提，能支撑 Handoff、阶段计划、Goal Prompt、验证和回滚；资料完整仍不等于执行授权。
- 将“原型”从 UI 视觉门禁中拆出为项目级产品原型门禁：新软件、产品、网站、App、小程序、SaaS、后台和内部系统默认需要产品原型/交互草图；Lean 可用文本流程或低保真草图，Standard/Enterprise 必须覆盖核心路径、页面/模块结构、关键交互和状态；纯后端、脚本、库、局部 bugfix 等可说明原因后跳过。
- 收紧需求到执行的边界：将“完整需求”改为“可执行完整需求”，明确“稍微完整的需求 / PRD / 目标描述 / 整理 Goal 请求”不等于执行授权；新增 Goal Draft、Goal Prompt、Execution Authorization 三层定义，要求项目在产品原型、设计依据、视觉方向或明确跳过原因确认前不得进入代码。
- 新增工程执行四准则：Think Before Coding、Simplicity First、Surgical Changes、Goal-Driven Execution；同步到 `SKILL.md`、`AGENTS.md` 和 `references/execution-contract.md`，要求开发前说明假设/歧义/取舍/成功标准，执行中保持最小实现、手术式修改和目标驱动验证。
- 将 `SKILL.md` 从“一句话启动开发”的重流程入口调整为“对话式项目想法/已有需求收敛”的轻量路由内核：新增粗略想法、半成型需求、完整材料三类输入分流；统一每轮提问数量、默认 3 个视觉方向、关键边界检查 workflow gates；允许在线程工具不可用时在当前线程显式切换执行阶段，避免 Lean 小任务被 Enterprise 流程拖重。
- 多线程规则调整为长期线程优先。
- 临时线程必须在任务完成后合并、放弃或归档，并更新 THREADS.md / MERGE_PLAN.md。
- 技能定位从偏特定工具类场景扩展为适用于小程序、网站、App、SaaS、后台系统、企业系统与通用工具软件。
- 明确 PM Thread 与执行线程分离：PM Thread 只负责需求、范围、风险、验收与交接，不负责代码修改；开发必须切换到新的执行线程。
- 架构示例改为通用软件项目结构，移除工具型 Editor / Engine 示例命名。
- README 改为 GitHub 友好的详细使用说明，并加入 Mermaid 工作流图。
- 新增项目目录策略：PM Thread 只创建 docs/codex/ 项目管理文档区，源码目录需在技术栈确认并进入执行线程后创建。
- 扩展 GitHub 首页说明，补充安装、更新、PM Thread、Execution Thread、真实项目目录、多线程治理与调用模板。
- 新增 `agents/openai.yaml`，把 Skill 内部名称规范化为 slug，并保留中文展示名与默认调用提示。
- 新增架构梳理与影响面控制规则：多线程分工前必须明确模块依赖、共享资源、影响面表、线程责任矩阵、合并顺序与跨模块验证路径。
- 将 `SKILL.md` 瘦身为核心入口规则，并把 PM 访谈、架构多线程、文档治理、执行回滚细则拆入 `references/`，降低触发 Skill 时的上下文负担。
- 强化 PM Thread：必须逼问出完整、可实现、可测试、可验收的 PRD，设计规范不完整时继续追问或给方案选择。
- 新增原型图/交互草图规则：需要视觉确认时调用可用生图或设计工具生成草图，并等待用户确认。
- 调整 Goal Prompt 门槛：Goal Draft 可在 PM 后段形成，但最终 Goal Prompt 必须在阶段计划、验证方案和自动化模式明确后输出，并等待用户明确执行授权。
- 新增阶段开发计划规则：每阶段必须可实现、可测试、可验收、可回滚。
- 新增自动开发、自动测试、自动修复闭环，以及失败阻塞输出规则。
- 新增隐私审计、打包发布、版本文档、独立 Code Review Thread 和自进化记录规则。
- 整理 Skill 包目录：项目文档模板移动到 `assets/templates/docs-codex/`，项目根模板移动到 `assets/templates/project-root/`。
- 新增反阿谀奉承规则：禁止迎合式确认和无依据乐观承诺，发现风险、矛盾或不可实现点时必须直接指出并给出替代方案。
- 新增 `references/workflow-gates.md` 全流程门禁表，串联 PM、PRD、设计、架构、Goal、Execution、Review、Release、Evolution。
- 新增一段式 Goal 指令规则、`PHASE_PLAN.md`、`HANDOFF.md` 模板，明确开发前 Goal、阶段计划和 PM 交接产物。
- 强化阶段推进规则：门禁不通过不得进入下一阶段，测试未通过不得进入 Code Review，存在 P0 不得进入 Release。
- 新增需求一致性审核环节和 `ACCEPTANCE.md` 模板：Code Review 前必须逐条对照 PRD、设计规范、Goal、阶段计划和 Handoff，确认没有漏做、错做、多做或越界修改。
- 调整版本闭环：当前版本发布和复盘后进入 Version Close，不自动回 PM；只有新需求、变更、返工或下一版本才重新进入 PM Thread。
- 新增独立 `Phase Acceptance Thread` 与 `PHASE_ACCEPTANCE.md` 模板：每轮/每阶段计划完成后必须单独验收，不合格打回 Execution Thread，Execution Thread 不得自我验收。
- 新增 `references/automation-contract.md` 受控自动开发契约，明确 Manual、Assisted Autopilot、Long-run Autopilot 三种模式，以及自动开发停止条件。
- 新增 `references/validation-strategy.md` 和 `VALIDATION.md` 模板：自动开发前必须识别测试命令；无测试时生成替代验证方案；无验证方式不得自动开发。
- 新增 `FEEDBACK_LOG.md` 模板和用户反馈驱动自进化规则：反馈先记录，重复、高影响或导致返工的问题再升级到检查项、决策、上下文或项目硬规则。
- 明确设计规范阶段的 Skill 调用链：Product Design:get-context / ideate、ui-ux-design-advisor、motion-quality、better-icons、ImageGen、Figma 与设计审查类 Skill 按需调用；实现型 image-to-code 必须等到 Execution Thread。
- 新增同类产品与开源方案分级调研规则和 `PRODUCT_RESEARCH.md` 模板：Level 2 轻量扫描同类产品/开源候选，Level 3 评估可商用二开底座、License、二开成本和提速价值。
- 前置竞品/同类产品调研到 PRD 冻结前：Level 2/3 必须用当前调研结论指导 PM 追问、MVP、非目标、设计规范、技术路线和阶段计划。
- 新增 Lean / Standard / Enterprise 流程档位：小项目可压缩 PM、文档和验收；标准项目保留核心门禁；长期商业项目启用完整治理。
- 新增轻量技术方案 / ADR 门禁和 `TECH_SPEC.md` 模板：涉及核心技术选型、API、数据、权限、部署或新增依赖时先确认实现契约。
- 强化 `VALIDATION.md` 为 QA 验证矩阵：区分自动测试、人工主链路、回归检查、发布后 smoke 和不可自动验证项。
- 打通审查验收自动打回闭环：Phase Acceptance、Requirement Compliance、Code Review 不通过时必须生成 Fix Request，Execution Thread 定向修复后输出 Fix Response 并重新提交验收。
- 补齐 PM、Execution、Phase Acceptance 与自动开发契约之间的 TECH_SPEC/ADR、QA 验证矩阵、Fix Request/Fix Response 闭环要求，避免流程文档互相断链。
- 同步 `HANDOFF.md`、`PHASE_PLAN.md` 模板字段，确保正式开发前能记录自动化模式、QA 验证矩阵、验收打回和修复轮次上限。
- 调整 Goal 定位：Goal 不再作为必备独立文档，而是正式开发前发给用户确认、并可复制到 Codex Execution Thread 的一段式目标指令；确认结果记录在 Handoff 或 QA 记录中。
- 强化设计规范闸门：UI 项目必须询问参考产品、截图、Figma、原型、草图、品牌素材或竞品 URL；没有明确视觉目标时必须确认是否调用 Product Design:get-context -> ideate，并在用户选择方向前禁止进入 UI 实现。
- 调整 PM Handoff 定位：Handoff 改为面向其他线程的工作单；Goal 只作为用户授权依据。新增 Work ID 与活跃工作安排登记规则，要求派发前登记、执行后避免随意打断、验收通过后从活跃登记移除并归档摘要。
- 新增浏览器验收策略：UI 验收、localhost 检查、截图和视觉 smoke 默认使用 Codex 内置浏览器；只有需要 Chrome 登录态、Cookie、插件、已打开页面状态或用户明确要求时才使用外置 Chrome，并必须记录原因。
- 调整 Goal 未确认后的处理：用户暂不确认或不选择使用 Goal 时，不进入 Execution Thread，但 PM Thread 必须继续按阶段开发计划沟通缺口、风险、建议和下一步选择。

### Fixed

- 修正验收顺序描述：需求一致性审核必须在全部阶段验收通过后执行，避免绕过 Phase Acceptance Thread。

### Notes

- 每次 Codex 完成任务后必须更新此文件。
