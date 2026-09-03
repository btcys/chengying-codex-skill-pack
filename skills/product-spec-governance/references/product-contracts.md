# 拆分PRD产品合同

拆分PRD后，检查重点不是文件日期，而是同一条产品规则是否只有一个负责人，以及引用方是否仍跟随当前版本。

## 检查范围

只读取根`PRD.md`、`docs/prd/README.md`、本次变更的领域PRD、直接依赖它的领域PRD、相关`Design-Brief.md`或设计域，以及当前ACTIVE Spec。`archive/`、无依赖领域和未来版本默认不读。

## 唯一负责人

- 全局产品规则由根PRD负责，领域规则由一个领域PRD负责；
- 跨领域或容易重复的重要规则使用稳定`Contract ID`，例如`PRD-AUTH-001`；普通段落不编号；
- 一个`Contract ID`只能有一个`Owner`，其他PRD、Design-Brief和Spec只引用，不复制成第二份事实；
- 领域PRD按需记录`Owns`和`Depends On`，`docs/prd/README.md`负责把领域和负责人路由到唯一文件。

引用至少包含：

```text
Source: PRD-AUTH-001 @ docs/prd/account.md v2.1
```

## 变更检查

产品合同确认变化后：

1. 只更新负责该合同的PRD，递增其`Document Version`并更新`Last Updated`；
2. 在`PRD-CHANGELOG.md`记录`Contract ID`、稳定结论、影响领域和受影响文档；
3. 沿`Depends On`和`Source`检查直接引用方是否仍引用旧版本或保留冲突正文；
4. 结构性问题直接失败，语义取舍标记`NEEDS_CONFIRMATION`并暂停受影响范围；
5. 用户确认后才更新引用方，不能用较新的日期自动覆盖另一份规则。

结构性失败包括：重复Owner、找不到Contract ID、引用路径失效、引用版本落后、已确认合同变更没有进入PRD变更记录。文字含义疑似冲突但证据不足时只能提示，不能自动判定谁正确。

## 冲突提示

```text
发现产品规则冲突：PRD-AUTH-001
账号PRD：管理员可以删除全部素材。
素材PRD：已产生订单的素材不能删除。
影响：素材管理页、删除接口和权限测试。

1. 以账号PRD为准
2. 以素材PRD为准
3. 补充一条统一规则
```

用户选择后更新唯一Owner、受影响引用和版本信息；未选择前保持`NEEDS_CONFIRMATION`，不得修改PRD、Design-Brief、Spec或代码。
