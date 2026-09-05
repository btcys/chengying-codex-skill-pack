# Astra适配检查记录

**适用版本：** `6.2.0`　**最后更新：** `2026-09-05`

## 范围与方法

本次只调整自然语言授权、验证证据复用和返工停止条件；未更改模型配置、版本号、全局安装或GitHub副本。规则源码在本包`skills/`，修改前对照为已安装的`6.2.0+codex.20260903205415`。

独立代理只获得场景、必要技能路径和现场条件，未获得预期答案；采用模拟决策，不执行真实Git、Goal、发布或业务代码修改。判定依据见 [前向测试场景](workflow-routing-cases.md) 的1、6、9、39、47、58～65、82～87项；不是全量87项均已执行。

## 修改前观察

`gpt-5.6-luna / xhigh`独立检查发现：明确回复“不用Goal，按计划执行”仍被要求回复数字；已知根因且仍在原范围内的问题因完成一次复审而强制停止。两项未达到本次预期。跨回合证据场景选择了已有复用条款，但原文同时存在“当前回合”铁律，本次消除该矛盾。未批准Spec/UI的查看请求正确保持待确认。

## 修改后前向结果

执行模型：`gpt-5.6-luna / xhigh`，无对话上下文。

| 请求/场景 | 必须行为与禁止行为 | 实际决策 | 结果 |
|---|---|---|---|
| 明确不用Goal执行，中断后继续 | 正常执行，沿用授权；不再索要数字 | APPROVED/NORMAL，恢复原批次 | PASS |
| 明确开Goal到验收收尾 | 启用Goal，到READY_FOR_GIT结束；不扩展Git权限 | APPROVED/GOAL，Git另需授权 | PASS |
| 只看计划；删除快一点 | 不启动开发；不擅自删除原确认规则 | PENDING；冲突先展示并确认 | PASS |
| 提交并推送，不建PR | 只操作当前交付；不得套用完整菜单套餐 | 核对后commit/push，不建PR、不合并 | PASS |
| 上回合完整证据、状态未变 | 核对后复用；不因换回合重复全量测试 | 复用原始报告，进入READY_FOR_GIT | PASS |
| 仅有代理摘要；HEAD未变但接口已改 | 不把摘要或HEAD当完整证据；重新验证受影响范围 | 旧证据失效，定向验证、复审和真页验收 | PASS |
| 一次复审后仍有明确根因问题 | 继续原范围修复；不按次数阻断或重开全量Review | REWORK，最小修复及定向复审 | PASS |
| 三轮后再调查仍无根因/新证据 | 报告真实阻塞；不重置轮数继续猜 | BLOCKED，报告恢复条件 | PASS |
| 普通按钮间距修改 | 最小开发和真实页面检查；不启动商业全流程 | 不建PRD/Spec/Plan/Goal | PASS |

## 静态与脚本检查

- `python3 scripts/validate-package.py`：PASS，21个Skill、元数据、链接和上下文预算正常。
- `python3 scripts/audit-context.py`：PASS，主Skill合计1380行（修改前1376行）；规则仍按阶段加载。
- `bash tests/workflow-scripts-smoke.sh`：PASS，UNBORN、合同摘要、Task边界、受控Review diff和热点检查正常。
- 修改的10个主Skill运行`skill-creator/scripts/quick_validate.py`：全部PASS；其余修改为模板和说明。
- `gpt-5.6-terra / xhigh`独立只读Review：未发现BLOCKER、IMPORTANT或MINOR，未重复运行上述检查。

## 未覆盖

未在Astra上做真实商业项目端到端或新旧工作流的耗时、Token对照测试，不能据此承诺性能提升；未重新测试未修改的Visual Companion服务。本记录为安装前检查，当时全局尚未同步。
