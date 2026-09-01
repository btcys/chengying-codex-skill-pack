---
name: executing-plans
description: 在帧芯开发工作流已有书面Plan，但当前环境没有子智能体能力或用户明确要求单线程时，用于在一个开发任务中按依赖连续执行功能Task。
---

# 单线程执行计划

这是回退路线；有子智能体能力时默认使用 `subagent-driven-development`。

## 1. 载入与审查

1. 读取Plan、关联Spec、Global Constraints和适用项目指令。
2. 检查文件、接口、依赖和验证命令是否仍与仓库一致。
3. 发现关键歧义、缺失前置条件或不合理设计时，在写代码前停止并报告。
4. 按Task依赖排序，创建执行清单。

不要在执行Plan时自动搜索其他PRD或旧计划补全上下文。

## 2. 连续执行

对每个Task：

1. 标记 `IN_PROGRESS`；
2. 完成完整功能结果，不为每个微步骤增加门禁；
3. 适用时执行TDD；
4. 运行Task的定向验证；
5. 更新Acceptance、Remaining和必要的Rework记录；
6. 只有所有阻断性Acceptance满足才标记 `DONE`；明确标记为`Advisory`的事项不参与完成门禁。

开发中无需每完成一个Task就请求独立Review。遇到失败先系统化调试；同一Task连续三轮仍不通过时转 `BLOCKED`，停止继续打补丁。

## 3. Plan级收尾

所有Task完成后：

1. 请求一次独立代码Review；
2. 阻断问题统一修复后只做一次定向复审；
3. 运行完整test、typecheck、build和项目门禁；
4. 用户可见能力进行产品验收；纯API、内部数据或基础设施Plan记录`Product Acceptance: N/A`并完成技术验收；
5. 使用分支收尾Skill让用户选择集成方式。

## 停止条件

- Plan、Spec、PRD或用户确认的UI相互冲突；
- 依赖、权限、凭据或环境缺失；
- 验证连续失败且根因未明；
- 下一步需要未授权的worktree、依赖安装、commit、push、merge、deploy或生产写入。
