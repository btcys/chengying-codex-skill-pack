# PRD变更记录

## 用途

`PRD-CHANGELOG.md`是PRD专属的简短历史索引。根PRD和领域PRD只维护当前事实；每次已确认的产品事实、用户流程或业务规则变化，同时更新PRD版本 / 日期，并在这里追加一条结果和链接。

## 模板

```markdown
# PRD变更记录

**Document Version:** `v1.0`（与当前PRD同步）
**Last Updated:** `YYYY-MM-DD`
**PRD Source:** `PRD.md`

## 2026-09

- `v1.1` — `<Contract ID或NONE>`：确认<稳定产品结论>；影响`<领域和引用文档>`；详见`docs/prd/<domain>.md`。
```

## 维护规则

- 一条记录只写稳定结论、影响范围和链接，不写实现细节、Task状态、测试日志、截图说明或失败过程。
- 活动区只保留仍会影响事实判断的近期结论；旧结论按年份归档，例如`docs/archive/prd/PRD-CHANGELOG-2026.md`，归档文件只作追溯，不作为普通Task输入。
- 活动文件超过150行时按年份归档；归档前先更新链接，不删除历史。
- 新功能、用户流程或业务规则变化由PM在唯一领域PRD原位更新；跨领域规则才更新根PRD，禁止创建`v2`、`latest`、`old`或平行事实源。
- 多个领域PRD并存时，记录条目写实际被改领域的`Document Version`；根PRD只有在全局产品规则变化时才递增，变更记录头部版本取当前最新PRD版本。
- 跨领域重要规则写稳定`Contract ID`和受影响引用方；普通领域内变化写`NONE`，不为每个段落增加编号。
