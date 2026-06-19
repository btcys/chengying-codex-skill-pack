# 流程档位

## 目标

用流程档位控制工作量。项目等级判断复杂度，流程档位判断本次要走多重的治理流程。

PM Thread 第一轮后必须同时给出：

- 项目等级：Level 1 / Level 2 / Level 3。
- 流程档位：Lean / Standard / Enterprise。
- 升级或降级理由。

## 三种档位

| 档位 | 适用 | PM 与 PRD | 调研 | 文档 | 验收与审查 |
| --- | --- | --- | --- | --- | --- |
| Lean | 小工具、Demo、单页、小改动、内部临时脚本 | 1 到 2 轮 PM；PRD 和产品原型可写成 Handoff 切片 | 0 到 15 分钟，可跳过 | `README.md`、`AGENTS.md`，必要时写 `HANDOFF.md` / `VALIDATION.md` | 轻量验收表；不强制独立 Code Review / Release |
| Standard | 正式小程序、网站、App、后台、中小型 SaaS | 完整 PRD、产品原型/交互草图、设计规范、技术方案、阶段计划和一段式 Goal 指令 | 20 到 45 分钟轻量竞品/开源扫描 | 核心 `docs/codex/` 文档 | Phase Acceptance 必须有；Code Review 按风险启用 |
| Enterprise | 长期商业项目、用户数据、权限、上传、计费、发布、多模块、多线程 | 完整 PRD、产品原型、设计规范、TECH_SPEC/ADR、架构影响面、版本规划 | 1 到 3 小时；必要时独立 Research Thread | 完整 `docs/codex/` 文档体系 | Phase Acceptance、Requirement Compliance、Code Review、Privacy Audit、Release 必须有 |

默认当前对话是 PM Thread。Lean 快速路径可在授权后由当前线程显式切换执行；Standard 和 Enterprise 必须由 PM Thread 派发给独立 Execution Thread 或已有执行线程修改代码。

## 选择规则

- 默认不要用 Enterprise；只有项目风险和生命周期需要时才升级。
- Level 1 默认 Lean。
- Level 2 默认 Standard。
- Level 3 默认 Enterprise，但如果只是低风险局部维护，可降为 Standard。
- 用户要求快速验证时，优先 Lean；但不能绕过安全、隐私、数据和发布风险。
- 多线程按档位升降级：Lean 默认单线程并写明不拆原因；Standard 在技术方案和架构影响面明确后只做候选拆分；Enterprise 必须在 Goal Prompt / Execution 前输出执行前线程方案，但不代表默认并行开发。

## 必须升级的情况

遇到以下任一情况，不得使用 Lean：

- 登录、权限、团队协作、支付、上传、AI Key、客户数据、个人信息。
- 数据库 schema、API 契约、权限模型、构建配置或部署发布变更。
- 长期维护、商用交付、多人协作、多线程开发。
- 用户明确要求高可靠、可发布、可审计或可回滚。
- 失败会影响生产、客户数据、品牌或收入。

## 可降级的情况

满足以下条件可以降级：

- 本次只做视觉微调、文案、静态页面、Demo 或局部非核心功能。
- 不触碰权限、数据、上传、支付、发布、API 契约和公共架构。
- 有清晰验收方式，且失败代价低。

## 压缩规则

Lean 可以合并阶段，但不能省略判断：

- PRD、产品原型、设计规范、阶段计划、验证方案和执行前线程方案可合并为一个轻量开发前对齐包 / Handoff；产品原型可以是文本流程、页面清单或低保真草图。
- 技术方案可合并到 Handoff；触碰 API、数据、权限、部署或新增依赖时升级到 Standard。
- 竞品调研可跳过，但要写明原因。
- Phase Acceptance 可用轻量验收表，不强制新线程。
- Goal 仍必须在开发前确认，但它只是用户授权目标；执行线程必须读取开发前对齐包 / PM Handoff / Work ID 工作单。
- 多线程判断可压缩为一句结论，通常为 single-thread；不得因为想加速而拆线程。

### Lean 快速路径

适用：

- 低风险 bugfix、文案、静态内容、视觉微调、一次性脚本、单页 Demo。
- 不触碰登录、权限、客户数据、上传、支付、AI Key、数据库 schema、API 契约、部署发布、新增依赖或公共架构。
- 验收方式清楚，失败代价低，可用一次任务完成和回滚。

Lean 快速路径只需要 6 个最小字段：

```markdown
目标：
非目标：
允许修改：
禁止修改：
验收方式：
回滚方式：
```

Lean 的 Work ID 可以是聊天内轻量编号，例如 `L-20260619-001`。除非项目需要长期维护或用户要求沉淀，否则不强制创建 `docs/codex/`、`TASKS.md`、完整 `HANDOFF.md`、独立 `PHASE_PLAN.md`、独立 `DESIGN.md` 或独立 `TECH_SPEC.md`。

Lean UI Fix 可以按已有页面、明确截图或文字验收目标执行；只要求记录视觉依据来源、必须对照点、禁止偏离点和 before/after 或替代观察证据。不需要重新走完整产品原型或视觉探索。

Standard 保留完整主线，但允许文档后置生成：

- PM 阶段先形成 PRD、PRODUCT_RESEARCH、产品原型、DESIGN、TECH_SPEC、PHASE_PLAN、VALIDATION、执行前线程方案、开发前对齐包、GOAL、HANDOFF 的等价内容。
- 用户确认 Goal 后，PM Thread 只负责登记 Work ID、冻结 Handoff 和派发 Execution Thread；不得自己改业务代码。
- Execution 后再补齐 PHASE_ACCEPTANCE、ACCEPTANCE、CODEX_QA。
- 如需多线程，必须先在技术方案/架构影响面阶段完成可拆性分析，再在 Goal Prompt / Execution 前的执行前线程方案中确定线程数量，并写清线程责任、契约、合并顺序和验证矩阵。

Enterprise 不压缩关键门禁：

- 不压缩架构影响面、多线程边界、需求一致性审核、代码审查、隐私审计、发布和回滚。
