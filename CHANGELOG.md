# CHANGELOG.md

## Unreleased

### Added

- 初始化橙影 Codex 企业级工作流技能包。

### Changed

- 多线程规则调整为长期线程优先。
- 临时线程必须在任务完成后合并、放弃或归档，并更新 THREADS.md / MERGE_PLAN.md。
- 技能定位从偏特定工具类场景扩展为适用于小程序、网站、App、SaaS、后台系统、企业系统与通用工具软件。
- 明确 PM Thread 与执行线程分离：PM Thread 只负责需求、范围、风险、验收与交接，不负责代码修改；开发必须切换到新的执行线程。
- 架构示例改为通用软件项目结构，移除工具型 Editor / Engine 示例命名。
- README 改为 GitHub 友好的详细使用说明，并加入 Mermaid 工作流图。
- 新增项目目录策略：PM Thread 只创建 docs/codex/ 项目管理文档区，源码目录需在技术栈确认并进入执行线程后创建。

### Fixed

- 暂无。

### Notes

- 每次 Codex 完成任务后必须更新此文件。
