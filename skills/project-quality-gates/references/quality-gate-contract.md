# 项目质量门禁落地合同

本合同约束门禁在业务项目中的文件、证据和维护方式。具体实现必须先适配项目现有技术栈，不复制与项目不兼容的通用脚本。

## 项目文件

```text
.codex/
├── quality-gates.json
└── quality-gates-baseline.json   # 只有旧项目确有历史债务时建立

tools/quality-gates/
├── <gate implementation>
└── tests/
    ├── <invalid fixture or test>
    └── <valid fixture or test>
```

门禁必须通过项目自己的包命令、Makefile或任务工具提供逻辑入口：

- `quality:fast`：只检查改动相关的快速门禁，供开发中使用；
- `quality:pr`：运行全部已启用静态门禁和项目测试，供合并前及CI使用；
- `quality:release`：在`quality:pr`基础上增加构建、迁移和部署合同检查，不执行生产写入。

## 最小配置

`.codex/quality-gates.json`至少记录：

```json
{
  "schemaVersion": 1,
  "lastUpdated": "YYYY-MM-DD",
  "capabilities": ["ui", "api", "database"],
  "commands": {
    "fast": "<project command>",
    "pr": "<project command>",
    "release": "<project command>"
  },
  "gates": {
    "check:secrets": {
      "enabled": true,
      "implementation": "tools/quality-gates/<exact-file>",
      "modes": ["fast", "pr", "release"]
    }
  },
  "authorities": {},
  "baseline": "NONE"
}
```

使用实际路径和命令，不保留占位符。新增、删除或改变门禁时更新`lastUpdated`和当前Plan；它不是PRD变更，不写入`PRD-CHANGELOG.md`。

## 门禁合同

每个门禁必须：

1. 有稳定名称、中文说明、适用能力和运行档位；
2. 只读取检查所需文件，不修改业务代码或自动修复；
3. 成功退出码为0，违规退出码非0，工具或环境缺失不得伪装通过；
4. 输出规则、准确位置和修复方向，不输出Secret值；
5. 有一项违规自测和一项合法自测，并在临时目录运行；
6. 若使用白名单，只接受准确规则和位置，不接受目录级或通配符放行；
7. 跨平台项目不把单一系统命令写成唯一实现，除非项目已明确限定平台。

## 门禁目录

### `check:secrets`

使用项目已有或成熟Secret扫描能力，检查将进入Git的改动，并在CI覆盖受控仓库范围。不得在报告中回显密钥、Token或密码；示例凭据必须是明确无效的测试值。

### `check:workflow-contracts`

检查CI/CD引用的包名、版本、脚本和文件真实存在，命令与项目任务入口一致，`quality:pr`和`quality:release`已接入正确阶段。它不执行部署。

### `check:hotspots`

承接项目确认的普通源文件和测试文件阈值、既有超限文件no-growth及准确例外。生成代码、第三方代码、迁移、快照和纯数据按项目规则排除；不得借门禁要求无关重构。

### `check:vocabularies`

只检查配置中明确列出的状态、类型、权限或业务枚举唯一来源及其生成物或镜像。没有`authorities`映射时只给提示，不通过名称相似猜测语义重复。

### `check:product-contracts`

只检查活动的根PRD、领域索引、本次变化的领域PRD、直接依赖方、相关Design-Brief和当前Spec。按照产品治理的`Contract ID`、唯一Owner、`Depends On`和`Source`检查重复定义、失效引用、旧版本引用及漏写PRD变更记录；疑似语义冲突输出`NEEDS_CONFIRMATION`，不得自动选择事实源。

文档变化后可单独运行；`quality:pr`和`quality:release`再次检查当前活动链。普通代码开发过程不重复扫描PRD，归档和无关领域始终不读。

### UI门禁

- `check:ui-tokens`检查项目定义范围内的颜色、字号、间距、圆角、阴影和控件尺寸是否使用已确认Token；既有例外必须准确登记。
- `check:dangling-tokens`检查CSS变量或等价Token引用是否存在定义，并覆盖项目支持的主题和入口。
- `check:component-contracts`检查配置中的共享组件唯一入口、禁止的重复实现或越界依赖、已有无障碍lint和公共组件测试；无法静态判断的复用质量保留给Review。

### 条件门禁

- `check:heavy-path`只在项目确有重负载路径时启用，预算和测量方式必须来自真实场景，不使用通用臆测阈值。
- `check:api-contracts`核对项目选定的API唯一合同及客户端/服务端一致性。
- `check:boundaries`核对项目已确认的模块依赖方向，不为建立门禁发明新架构。
- `check:migrations`核对Schema变化、迁移文件、顺序、从零建立和CI/发布接入；危险数据操作另行提示。
- `check:authorization-contracts`核对已确认的权限矩阵、服务端执行点和关键拒绝测试，不把前端隐藏按钮当成授权证据。

## 旧项目基线

仅在首次接入确有历史违规时创建`.codex/quality-gates-baseline.json`。每项记录门禁、规则、准确文件或对象、稳定指纹、理由、确认日期和关联Plan。

运行时只豁免仍与原指纹匹配的历史问题；新问题、位置扩大或规则变化都必须失败。修复后删除对应基线项，禁止扫描后自动重写整个基线。

## CI接入

优先修改已有CI并沿用缓存、运行器和包管理方式。没有CI时，推荐卡必须说明将创建哪种CI、运行时机和维护成本，用户确认后才建立。

CI中`quality:pr`是合并前事实来源，`quality:release`是发布候选检查之一；二者不能替代独立Review、产品验收、发布风险审查或生产发布授权。
