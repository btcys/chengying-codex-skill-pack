#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


MAX_SKILL_LINES = 140
MAX_REFERENCE_LINES = 180
MAX_ALL_SKILL_LINES = 1300
MAX_DESCRIPTION_CHARS = 7000


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip().strip('"\'') if match else ""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill_files = sorted(root.glob("skills/*/SKILL.md"))
    reference_files = sorted(root.glob("skills/*/references/*.md"))
    errors: list[str] = []

    skill_sizes = [(line_count(path), path) for path in skill_files]
    reference_sizes = [(line_count(path), path) for path in reference_files]
    all_skill_lines = sum(size for size, _ in skill_sizes)
    description_chars = sum(len(description(path)) for path in skill_files)

    for size, path in skill_sizes:
        if size > MAX_SKILL_LINES:
            errors.append(f"主Skill过长: {path.relative_to(root)} = {size}行")
    for size, path in reference_sizes:
        if size > MAX_REFERENCE_LINES:
            errors.append(f"reference过长: {path.relative_to(root)} = {size}行")
    if all_skill_lines > MAX_ALL_SKILL_LINES:
        errors.append(f"全部主Skill共{all_skill_lines}行，超过预算{MAX_ALL_SKILL_LINES}行")
    if description_chars > MAX_DESCRIPTION_CHARS:
        errors.append(
            f"全部description共{description_chars}字符，超过触发上下文预算{MAX_DESCRIPTION_CHARS}字符"
        )

    entry = root / "skills" / "using-development-workflow" / "SKILL.md"
    entry_text = entry.read_text(encoding="utf-8")
    required_rules = (
        "每次只加载当前阶段的主Skill",
        "不读取完整PRD、完整词汇表与其他批次报告",
        "Review读取Spec、Plan、受控变更材料和验证证据",
        "一个阶段完成后先落文档和状态",
    )
    for rule in required_rules:
        if rule not in entry_text:
            errors.append(f"总入口缺少上下文隔离规则: {rule}")

    implementer = root / "skills" / "subagent-driven-development" / "references" / "implementer-prompt.md"
    implementer_text = implementer.read_text(encoding="utf-8")
    if "相关章节" not in implementer_text or "NEEDS_CONTEXT" not in implementer_text:
        errors.append("开发子智能体合同缺少Spec片段或缺上下文升级协议")

    brainstorming = root / "skills" / "brainstorming" / "SKILL.md"
    brainstorming_text = brainstorming.read_text(encoding="utf-8")
    for rule in ("适度需求访谈", "全部按推荐", "最多三轮", "architecture-reuse-research.md"):
        if rule not in brainstorming_text:
            errors.append(f"Brainstorming缺少需求或架构调研规则: {rule}")

    visual = root / "skills" / "brainstorming" / "references" / "visual-companion.md"
    visual_text = visual.read_text(encoding="utf-8")
    for rule in ("组件复用", "设计规范", "状态与动效", "prefers-reduced-motion"):
        if rule not in visual_text:
            errors.append(f"Visual Companion缺少UI控制: {rule}")

    frontend_rules = (
        root / "skills" / "using-development-workflow" / "references" / "frontend-six-rules.md"
    )
    if not frontend_rules.is_file():
        errors.append("缺少前端六点参考: skills/using-development-workflow/references/frontend-six-rules.md")
    else:
        frontend_text = frontend_rules.read_text(encoding="utf-8")
        for rule in ("1. 先确认用户任务和业务对象", "2. 删除无效信息和伪操作", "3. 保证数据、状态和作用域真实", "4. 让界面结构和代码各自归位", "5. 让视觉与动效真正落地", "6. 修改源头并完成迁移"):
            if rule not in frontend_text:
                errors.append(f"前端六点参考缺少规则: {rule}")

    execution_modes = (
        root / "skills" / "using-development-workflow" / "references" / "execution-modes.md"
    )
    if not execution_modes.is_file():
        errors.append("缺少执行模式参考: skills/using-development-workflow/references/execution-modes.md")
    else:
        execution_text = execution_modes.read_text(encoding="utf-8")
        for rule in ("LOCAL_DEV", "STAGING_QA", "PRODUCTION_RELEASE", "本地测试数据库", "付费测试"):
            if rule not in execution_text:
                errors.append(f"执行模式参考缺少规则: {rule}")

    plans = root / "skills" / "writing-plans" / "SKILL.md"
    plan_text = plans.read_text(encoding="utf-8")
    for rule in ("scan-code-hotspots.py", "600行", "1000行", "1500行", "no-growth"):
        if rule not in plan_text:
            errors.append(f"Plan缺少代码热点控制: {rule}")

    document_system = (
        root / "skills" / "product-spec-governance" / "references" / "document-system.md"
    )
    document_text = document_system.read_text(encoding="utf-8")
    prd_changelog = (
        root / "skills" / "product-spec-governance" / "references" / "prd-changelog.md"
    )
    if not prd_changelog.is_file():
        errors.append("缺少PRD变更记录参考: skills/product-spec-governance/references/prd-changelog.md")
        changelog_text = ""
    else:
        changelog_text = prd_changelog.read_text(encoding="utf-8")
    if "CONTEXT.md职责" not in document_text or "不能新增或覆盖PRD需求" not in document_text:
        errors.append("产品文档体系缺少CONTEXT.md词汇边界")
    for rule in ("文档现实性", "DOC_STALE", "CODE_DRIFT", "NO_CHANGE", "变更记录只属于PRD", "PRD-CHANGELOG.md", "150行"):
        if rule not in document_text + changelog_text:
            errors.append(f"产品文档体系缺少现实性规则: {rule}")

    failure_contract = (
        root / "skills" / "product-spec-governance" / "references" / "failure-evidence-contract.md"
    )
    failure_text = failure_contract.read_text(encoding="utf-8")
    for rule in ("FAIL-EVIDENCE", "预期发生的RED", "RootCause", "不因为记录失败自动触发"):
        if rule not in failure_text:
            errors.append(f"失败证据合同缺少边界: {rule}")

    optimizing = root / "skills" / "optimizing-development-workflow" / "SKILL.md"
    optimizing_text = optimizing.read_text(encoding="utf-8")
    for rule in ("只有用户明确要求", "NO_CHANGE", "最多给三条建议", "不建立信号队列", "FAIL-EVIDENCE"):
        if rule not in optimizing_text:
            errors.append(f"工作流复盘缺少轻量边界: {rule}")
    optimizing_ui = root / "skills" / "optimizing-development-workflow" / "agents" / "openai.yaml"
    if "allow_implicit_invocation: false" not in optimizing_ui.read_text(encoding="utf-8"):
        errors.append("工作流复盘必须保持显式调用")

    largest_skills = ", ".join(
        f"{path.parent.name}={size}行" for size, path in sorted(skill_sizes, reverse=True)[:3]
    )
    largest_refs = ", ".join(
        f"{path.parent.parent.name}/{path.name}={size}行"
        for size, path in sorted(reference_sizes, reverse=True)[:3]
    )

    if errors:
        print("上下文预算审计失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "上下文预算审计通过："
        f"{len(skill_files)}个主Skill共{all_skill_lines}行，"
        f"description共{description_chars}字符。"
    )
    print(f"最大主Skill：{largest_skills}")
    print(f"最大reference：{largest_refs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
