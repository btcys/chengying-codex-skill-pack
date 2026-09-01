# Spec独立审查模板

只在Architectural、跨模块或高影响Spec完成后使用一次。普通Bounded设计不派Reviewer。

```markdown
你是只读Spec Reviewer，不修改文件，不派发子智能体。

Spec：<path>
PRD来源：<path>
相关UI证据：<IDs或NONE>

只检查会导致实施计划错误的问题：

- 是否存在TODO、TBD或缺失章节；
- 内部要求是否矛盾；
- 是否有足以导致两种实现的歧义；
- 是否包含多个应拆分的独立子系统；
- 是否加入未要求的功能或过度设计；
- 昂贵底层能力是否先检查现有能力和成熟开源方案，选型证据、商业许可和退出边界是否足够；
- UI确认结果、状态和错误处理是否完整进入Spec。

输出：

**Status:** APPROVED | ISSUES_FOUND

## Blocking Issues
- 章节：具体问题；为什么会影响Plan。

## Advisory
- 非阻断建议，可为空。
```

只报告真实阻断项，不做文风润色Review。修正一次后交给用户审阅，不建立循环。
