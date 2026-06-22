# 文档治理

文档是 AI 开发闭环的阶段产物，要求短、可执行、可交接。

## 第一上下文

`docs/codex/CURRENT_STATE.md` 是长期项目第一入口，控制在 80 行以内：

- 当前 Goal
- 当前环节
- 接手入口：仓库/分支、运行入口、验证入口、环境变量名称
- 已确认事实
- 线程 ownership
- 最近决策
- 正在进行
- 不要做什么
- 下一步
- 风险/阻塞
- 最近验证

它必须支持换电脑、新 Codex 线程或上下文断开后接手开发。只写必要事实，不写密钥值；外部账号、API Key、部署权限只记录名称、用途和获取方式。

## 候选产物

下表是候选清单，不是默认必填项。每次只创建当前门禁、交接或验收真正需要的最小文档。

| 环节 | 文档 |
| --- | --- |
| Product Research | `docs/codex/PRODUCT_RESEARCH.md` |
| Product Spec | `docs/codex/PRD.md` |
| Design Brief | `docs/codex/DESIGN_BRIEF.md` |
| Visual References | `docs/codex/VISUAL_REFERENCES.md` / `docs/codex/assets/visual-references/` |
| Prototype / Design | `docs/codex/PROTOTYPE.md` / `docs/codex/DESIGN.md` |
| Dev Planner | `docs/codex/DEV_PLAN.md` |
| Dev Threads | `docs/codex/THREAD_TASK.md` / `docs/codex/HANDOFF.md` |
| Review / QA | `docs/codex/CODEX_QA.md` / `docs/codex/ACCEPTANCE.md` |
| Release | `docs/codex/RELEASES.md` |
| Evolution | `docs/codex/CURRENT_STATE.md` / `docs/codex/FEEDBACK_LOG.md` / `docs/codex/DECISIONS.md` |

## 规则

- 不复制大段聊天，写结论和链接。
- 候选产物不是默认产物；普通明确任务优先用短任务卡、验证结果和必要状态更新收口。
- 复杂项目先做竞品/同类产品和开源候选调研；结论写入 `docs/codex/PRODUCT_RESEARCH.md`，再进入 PRD 冻结。
- 用户提供截图、竞品、Figma、旧页面或目标效果图时，使用前先存档或记录不可存档原因。
- 文档未完美不阻塞开发；但 PRD、设计依据、Dev Plan 和线程 ownership 不清时，不要并行开发。
- `docs/codex/CURRENT_STATE.md` 每次重要变更后更新，保证新环境能先运行、再验证、再继续改。
- 活跃任务完成后从 `TASKS.md` 活跃区移除，保留完成摘要和证据。
