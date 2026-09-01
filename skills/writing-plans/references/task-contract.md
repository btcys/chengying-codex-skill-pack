# Task精确合同

Task不需要拆成微步骤，但必须让无上下文开发代理知道改什么、交付什么和如何证明。

## 必填

- `Result`：完成后可观察结果；
- `Depends On`：真实前置Task；
- `Parallel`：只有无共享文件、接口和状态时才为YES；
- `Files`：准确Create、Modify、Test路径；
- `Interfaces`：接口名、输入输出、调用方或组件事件；
- `Acceptance`：可逐条判断的产品或工程结果；
- `Verification`：准确的定向命令或真实页面检查；
- `Remaining`：部分完成时的剩余结果。
- `Execution Mode`：本Task使用的环境模式；付费测试或数据范围不明确时只询问一次，不逐次询问普通本地操作。
- 若Task未覆盖环境或费用差异，使用Plan的`Execution Mode`和`Authorized Test Scope`；只有需要切换环境或范围时才在Task中覆盖。

验收 `PASS` 后在原Task回写 `Actual Result`、Evidence、`Remaining`、`Spec Sync` 和 `Plan Sync`；实现方式变化只更新Plan，产品行为变化需确认后更新PRD或Spec。

## TDD任务

简要写清：

- RED测试覆盖的行为；
- 预期失败原因，不要求复制完整控制台输出；
- GREEN需要通过的同一命令；
- 必要的邻近回归范围。

## 非TDD视觉任务

引用Visual Companion确认结果、状态矩阵、动效合同、UI Compliance和Golden ID，写明目标入口与视口。不能只写“按设计稿实现”。

## 热点文件

Task触及Plan列出的热点文件时，写明保持不增长、在本Task拆出哪个职责，或引用已批准例外。不得借行数治理扩大为无关重构。

## 禁止

- `TODO`、`TBD`、`相关文件`等占位符；
- 根据PRD猜测不存在的路径和接口；
- 粘贴大段最终实现；
- 每个命令单独建Task；
- 强制每Task commit。
