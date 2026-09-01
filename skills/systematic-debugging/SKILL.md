---
name: systematic-debugging
description: 在帧芯开发工作流中遇到Bug、测试失败、异常行为、性能退化或同一Task反复返工时，用于在提出修复前定位可证明的根因。
---

# 系统化调试

随机试改会增加变量并制造新Bug。先证明根因，再做最小修复。

## 铁律

```text
没有完成根因调查，就不能提出修复方案。
```

## 第一阶段：调查根因

1. 完整阅读错误、堆栈、日志和失败输出，不跳过警告。
2. 稳定复现：写清入口、步骤、输入、环境、频率和实际结果；无法复现时先增加证据，不猜。
3. 检查最近相关变更、依赖、配置和环境差异，同时保护用户已有未提交改动。
4. 在多组件边界记录输入和输出：UI→API、API→服务、服务→数据库、构建→部署。先找值在哪一层第一次变错。
5. 逆着调用链追踪错误值的来源，直到找到最早产生错误状态的位置。方法见 [root-cause-tracing.md](references/root-cause-tracing.md)。

## 第二阶段：比较模式

- 查找同仓库中正常工作的相似实现；
- 完整比较差异，不先判断“小差异无关”；
- 明确依赖、隐含前提、生命周期和状态所有权；
- 先确认问题是实现偏差、合同错误、环境问题还是Spec本身错误。

## 第三阶段：提出并验证假设

一次只写一个假设：

```text
我认为 <根因> 导致 <现象>，因为 <证据>。
```

用能区分真假且改动最小的实验验证。失败后形成新假设，不在同一轮叠加多个改动。

## 第四阶段：修复

1. 适用时用 `$zhenxin-development-workflow:test-driven-development` 写最小失败回归测试；
2. 修复根因而不是最后出现症状的位置；
3. 运行回归测试和受影响邻近验证；
4. 若该失败已改变Task状态，按 [failure-evidence-contract.md](../product-spec-governance/references/failure-evidence-contract.md) 原地更新RootCause和Resolution；
5. 使用 `$zhenxin-development-workflow:verification-before-completion` 后再宣称修复。

## 三轮停止规则

同一Task连续三轮修复或返工仍不通过时：

- Task转为 `BLOCKED`；
- 停止继续追加补丁；
- 汇总每轮假设、证据和结果；
- 重新检查Spec、Architecture、状态所有权、模块边界和Task拆分；
- 需要改变产品或设计时返回用户确认。

## 红旗

- “先试着改这个看看”；
- 同时改多个变量；
- 没稳定复现就声称找到原因；
- 只增加timeout或sleep；
- 把错误吞掉、加fallback或重试来掩盖根因；
- 在数据流末端修补错误值；
- 两次失败后仍用同一种思路继续猜。

## 支持方法

- 测试依赖sleep、timeout或在并行时不稳定：读 [condition-based-waiting.md](references/condition-based-waiting.md)。
- 无效数据能穿过多个层级造成破坏：读 [defense-in-depth.md](references/defense-in-depth.md)。
- 需要找出哪个测试污染文件或目录：在确认命令适合当前项目后使用 `scripts/find-polluter.sh`；脚本默认调用 `npm test <file>`，非npm项目先修改执行命令。
