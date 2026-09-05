---
name: requesting-code-review
description: 在帧芯开发工作流的整个Plan实现完成后、合并前或用户明确要求时，用于发起一次独立的Spec合规和代码质量Review；默认不在每个Task后调用。
---

# 发起独立代码Review

Review的目标是在整合点发现真实缺陷，不是为每个小Task增加重复门禁。

## 何时使用

- 整个Plan的所有Task完成并通过定向验证后；
- 合并或正式发布候选形成前；
- 用户明确要求独立Review；
- 高风险核心模块的大范围重构完成后。

普通Task完成、纯文案或样式微调不单独触发。

## 准备材料

提供：

- Spec和Plan路径；
- Global Constraints原文；
- 准确base和head或完整工作区diff；
- 未跟踪文件清单；
- 开发测试证据；
- Golden或问题证据ID；
- 热点扫描结果，以及准确base可用时的no-growth检查结果；
- 已知裁定和残余风险。

不要让Reviewer依赖主任务的口头总结。使用 [code-reviewer.md](references/code-reviewer.md) 构造提示，派一个未参与实现的独立Reviewer。

## 处理结果

- `BLOCKER`/`IMPORTANT`：一个修复代理统一处理，再针对实际修复做定向复审；
- `MINOR`：记录并判断是否影响本次交付，不自动扩大范围；
- 与Spec冲突的建议：以批准的产品和设计合同为准，记录裁定；
- 证据不足的发现：先验证，不直接修改。

定向复审只检查原问题和修复diff的新回归，不重启全量Review或增加Reviewer。仍有原批准范围内、根因明确的问题且证据显示修复在推进时，继续集中修复和必要的定向复审；重复失败或范围有变时按 [返工与停止条件](../systematic-debugging/SKILL.md#返工与停止条件) 处理，不机械按轮数停止，也不无限循环。Reviewer报告问题，主任务据证据裁定`REWORK/BLOCKED`。
