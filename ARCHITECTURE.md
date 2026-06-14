# ARCHITECTURE.md

## 架构图规则

按项目复杂度决定是否生成架构图。

### Level 1

只写模块列表。

### Level 2

生成简单 Mermaid 依赖图。

### Level 3

生成：

- 模块结构图
- 依赖关系图
- 数据流图
- 多线程图
- 风险模块标记

## Mermaid 示例

```mermaid
flowchart LR
  UI[UI Layer] --> State[State Store]
  State --> API[API Layer]
  API --> Domain[Domain Service]
  Domain --> Data[Data Layer]
```

## 风险检查

- 跨层调用
- 循环依赖
- 状态污染
- UI 直接操作底层数据
- 多线程冲突
