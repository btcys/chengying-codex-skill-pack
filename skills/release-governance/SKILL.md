---
name: release-governance
description: 在帧芯开发工作流的正式版本或生产hotfix已完成技术验证、产品验收和发布风险审查后，用于准备发布计划、授权门禁、执行记录和版本收尾。
---

# 发布治理

把“已经开发完成”和“可以安全发布”分开管理。

## 发布前置条件

- 候选版本、commit和目标环境明确；
- 分支收尾已由用户选择集成方式，并形成将实际发布的候选commit；
- Plan完成，完整验证有新鲜证据；
- 若候选版本包含用户可见Acceptance，相关项已通过产品验收；纯API、内部数据或基础设施交付可用`Product Acceptance: N/A`并以技术验收替代；
- 正式发布风险审查结论允许继续；
- 数据迁移、配置、Secret、监控和回滚方案已确认；
- 已获得执行发布所需的明确授权。

任何条件缺失都保持“准备中”，不得把准备发布理解为授权发布。

## release-plan.md

写入 `docs/releases/<version>/release-plan.md`：

```markdown
# <version> 发布计划

**Candidate:** `<commit>`
**Environment:** `<target>`
**Status:** `READY | BLOCKED | RELEASED | ROLLED_BACK`

## 发布范围
## 前置检查
## 数据与配置变更
## 执行步骤
## 冒烟验证
## 监控指标
## 回滚条件与步骤
## 授权记录
## 发布结果
```

## 执行纪律

1. 发布前重新确认候选commit未变化；变化后风险审查和关键验证失效，必须更新。
2. 按计划执行，每个不可逆步骤前再次确认目标和备份。
3. 发布后立即完成真实入口冒烟验证和关键指标检查。
4. 达到回滚条件时停止继续发布，按计划回滚并记录证据。
5. 成功后更新发布结果和ROADMAP；失败则保留现场并标记 `BLOCKED` 或 `ROLLED_BACK`。

未经用户明确授权，不push、merge、deploy、release或执行生产写入。
