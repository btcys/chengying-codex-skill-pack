# 架构与开发线程

## 线程数量

- 只有需要并行且 ownership 清楚时才拆开发线程。
- 开发线程最多 3-5 个，不含 PM、总 Code Review、运维/发布线程。
- 有 UI 且拆开发线程时，UI 必须独立开发线程。
- 拆不出互不依赖模块时，宁可少开线程。
- 线程工具可用且任务需要拆分时，PM 派发真实子线程；工具不可用时输出可复制 Handoff。

## 推荐拆分

有 UI：

- UI / Frontend
- Backend / API
- Data / Integration
- Admin / Internal Tools（可选）
- Quality / Test Harness（可选）

无 UI：

- Core Logic
- API / Integration
- Data / Jobs / Scripts
- Tests / Tooling（可选）

## Ownership 表

```markdown
| 线程 | 负责模块 | 允许修改 | 禁止修改 | 依赖 | 被依赖 | 验收 |
| --- | --- | --- | --- | --- | --- | --- |
```

## 禁止并行修改

- 同一文件或目录。
- 同一 API contract。
- 同一 schema / migration。
- 同一 auth / permission 文件。
- 同一全局状态管理。
- 同一 build config。
- 同一 shared utils / shared types。

共享文件必须指定唯一 owner，其他线程等待 owner 输出契约。
