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

## 选择规则

- 默认不要用 Enterprise；只有项目风险和生命周期需要时才升级。
- Level 1 默认 Lean。
- Level 2 默认 Standard。
- Level 3 默认 Enterprise，但如果只是低风险局部维护，可降为 Standard。
- 用户要求快速验证时，优先 Lean；但不能绕过安全、隐私、数据和发布风险。

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

- PRD、产品原型、设计规范、阶段计划可合并为一个轻量 Handoff；产品原型可以是文本流程、页面清单或低保真草图。
- 技术方案可合并到 Handoff；触碰 API、数据、权限、部署或新增依赖时升级到 Standard。
- 竞品调研可跳过，但要写明原因。
- Phase Acceptance 可用轻量验收表，不强制新线程。
- Goal 仍必须在开发前确认，但它只是用户授权目标；执行线程必须读取 PM Handoff / Work ID 工作单。

Standard 保留完整主线，但允许文档后置生成：

- PM 阶段先形成 PRD、PRODUCT_RESEARCH、产品原型、DESIGN、TECH_SPEC、PHASE_PLAN、VALIDATION、GOAL、HANDOFF 的等价内容。
- Execution 后再补齐 PHASE_ACCEPTANCE、ACCEPTANCE、CODEX_QA。

Enterprise 不压缩关键门禁：

- 不压缩架构影响面、多线程边界、需求一致性审核、代码审查、隐私审计、发布和回滚。
