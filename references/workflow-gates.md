# 最小门禁

门禁用于保护质量，不用于拖慢开发。

## Product Spec 前

- 已形成 Goal Contract。
- 多种理解已列出并确认或写明假设。
- 用户参考资料已登记用途。

## Design / Prototype 前

- 有 UI 时必须有 Design Brief。
- 涉及 UI 时必须写明主目标端、是否支持手机 / 平板、最小与目标视口、比例参考；未明确时默认桌面 Web 优先，不承诺完整移动适配。
- 复杂 UI 必须有原型/交互依据。
- 没有 UI 时写明跳过原因。

## Dev Threads 前

- 已有 Dev Plan。
- 只有需要并行且 ownership 清楚时才拆开发线程。
- 开发线程最多 3-5 个。
- 有 UI 且拆开发线程时，UI 独立线程。
- 每个线程 ownership 不重叠。
- 共享契约已有唯一 owner。
- 不能并行时先串行做 contract/schema/shared 基础。

## Merge / Review 前

- 每个 Dev Thread 返回 Dev Result。
- 已运行相关验证或说明未验证原因。
- 总 Code Review 独立，不写业务代码。
- Code Review 轻量触发：auth / permission、data / migration、API contract / schema、shared types / utils、build / deploy config、跨线程合并、发布前必须独立 review；低风险单文件文案 / 样式 / 局部修复可自查。
- Code Review 输出 Fix Request 后必须派回 owner Dev Thread；收到 Fix Response 后重新验证。

## Release 前

- 验证证据、未验证项、风险、回滚方式明确。
- 运维/发布交给外部线程或明确 Handoff。
- 非商用、内测、阶段验收、技术预览或普通迭代不执行完整商业检查，只记录适用的风险和待补项。
- 正式商用发布前必须完成商业发布检查：权限、密钥、数据备份/迁移/回滚、构建/测试、关键路径验证、日志/监控、已知风险和发布说明。

## 高风险确认

删除、数据库、鉴权、权限、部署、生产配置、付费服务、架构重构必须先确认。
