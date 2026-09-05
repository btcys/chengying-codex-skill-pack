---
name: product-acceptance
description: 在帧芯开发工作流已启用且技术验证完成后，用于从真实产品入口验收用户闭环、UI、状态、权限、持久化和数据影响。
---

# 产品验收

技术测试通过不等于产品结果可用。本Skill只做真实入口的最终产品检查。

## 输入

- 已批准的PRD、Spec和Plan；
- Task/Plan中的`Execution Mode`及已授权的测试费用、账号和数据范围（如有）；
- Plan中的Acceptance与Global Constraints；
- 需求、问题和Golden证据；
- 最新技术验证结果。
- UI任务按需读取 [UI验收检查表](references/ui-acceptance-checklist.md)。

## 验收方法

1. 从用户实际入口开始，不用内部测试页代替。
2. 启动本地验收服务时优先使用动态空闲端口；固定端口必须先确认没有被其他进程占用，并记录实际URL。`LOCAL_DEV`或`STAGING_QA`下可直接执行授权范围内的登录、上传、保存、生成和测试数据库写入，不逐次询问。
3. 按真实角色和数据完成核心路径，覆盖与本次范围有关的默认、加载、空、错误、权限、刷新和重进状态。
4. 验证写入、刷新、持久化、撤销或恢复、跨页面一致性和对已有数据的影响。
5. UI改动按范围选择快速或完整检查，与当前 `Design-Brief.md`、相关设计域、已确认Golden比较，并实际检查组件一致性、设计规范、关键状态与动效、连续操作、布局跳动及减弱动效路径；允许的差异必须有Spec依据。
6. 将必要截图存入 `acceptance/`，在 `evidence.md` 建立 `ACCEPT-*` 记录。
7. 对每条验收项给出 `PASS`、`FAIL` 或 `BLOCKED`，附可复核证据；Acceptance下的每一项默认都是阻断项。
8. 验收 `PASS` 后回写原Plan Task的实际结果、Evidence、`Remaining`和`Spec Sync`/`Plan Sync`；没有产品或实现合同变化时写`NO_CHANGE`，不新建文档；有付费测试时同时记录次数和费用。

验收通过后如果代码、接口、状态或数据结构再次发生改动，受影响验收项的`PASS`和相关证据立即标为`SUPERSEDED`，Task转为`REWORK`，并在原Plan把`Product Acceptance: PASS`回写为`PENDING`。如果改动发生在Review或完整验证之后，旧Review和完整验证也不能覆盖最新diff；先做受影响范围的定向复审和新鲜验证，再重新走真实入口验收。未完成真实页面验收时，只能报告“开发完成，待真页验收”，不能报告“已修复”或“已完成”。

## 失败处理

- 实现错误：对应Plan Task转 `REWORK`，按 [failure-evidence-contract.md](../product-spec-governance/references/failure-evidence-contract.md) 记录期望、实际、证据、轮次和待确认根因。
- 产品或设计歧义：停止返工，回到PRD或Spec让用户确认。
- 环境或外部依赖不可用：标记 `BLOCKED`，写清恢复条件。
- 重复失败或同一Task三轮仍失败：按 [返工与停止条件](../systematic-debugging/SKILL.md#返工与停止条件) 重新调查，再依根因、进展和授权决定继续或阻塞。

只有所有阻断性Acceptance项通过，或纯内部交付明确记录`Product Acceptance: N/A`且技术验收通过，才能把交付单元标记为 `DONE`；标记为`Advisory`的非阻断项可以记录为未完成，不阻塞`DONE`。产品验收不授权发布。
