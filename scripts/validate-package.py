#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


EXPECTED_SKILLS = {
    "using-development-workflow",
    "uninstall-development-workflow",
    "brainstorming",
    "using-git-worktrees",
    "writing-plans",
    "executing-plans",
    "subagent-driven-development",
    "test-driven-development",
    "systematic-debugging",
    "dispatching-parallel-agents",
    "requesting-code-review",
    "receiving-code-review",
    "verification-before-completion",
    "finishing-a-development-branch",
    "writing-skills",
    "product-spec-governance",
    "product-acceptance",
    "release-risk-review",
    "release-governance",
    "optimizing-development-workflow",
    "project-quality-gates",
}

PACKAGE_VERSION = "6.2.0"
DISPLAY_NAME = "帧芯开发工作流 6.2"


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("缺少YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("frontmatter未闭合") from exc
    values: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    manifest_path = root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("name") != "zhenxin-development-workflow":
            errors.append("plugin name不正确")
        manifest_version = str(manifest.get("version", ""))
        valid_version = manifest_version == PACKAGE_VERSION or bool(
            re.fullmatch(rf"{re.escape(PACKAGE_VERSION)}\+codex\.[A-Za-z0-9._-]+", manifest_version)
        )
        if not valid_version:
            errors.append(f"plugin version不是{PACKAGE_VERSION}或有效Codex cachebuster版本")
        interface = manifest.get("interface", {})
        if interface.get("displayName") != DISPLAY_NAME:
            errors.append(f"plugin displayName不是{DISPLAY_NAME}")
        if DISPLAY_NAME not in interface.get("defaultPrompt", ""):
            errors.append(f"plugin defaultPrompt未使用{DISPLAY_NAME}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"plugin.json无效: {exc}")

    behavior_cases = root / "tests" / "workflow-routing-cases.md"
    if not behavior_cases.is_file():
        errors.append("缺少Codex前向测试场景: tests/workflow-routing-cases.md")

    entry_skill = root / "skills" / "using-development-workflow" / "SKILL.md"
    entry_agent = root / "skills" / "using-development-workflow" / "agents" / "openai.yaml"
    if f"# {DISPLAY_NAME}" not in entry_skill.read_text(encoding="utf-8"):
        errors.append(f"总入口标题未使用{DISPLAY_NAME}")
    if DISPLAY_NAME not in entry_agent.read_text(encoding="utf-8"):
        errors.append(f"总入口UI名称未使用{DISPLAY_NAME}")

    companion_smoke = root / "tests" / "visual-companion-smoke.mjs"
    if not companion_smoke.is_file():
        errors.append("缺少Visual Companion冒烟测试: tests/visual-companion-smoke.mjs")

    workflow_smoke = root / "tests" / "workflow-scripts-smoke.sh"
    if not workflow_smoke.is_file():
        errors.append("缺少空项目脚本冒烟测试: tests/workflow-scripts-smoke.sh")

    hotspot_script = root / "scripts" / "scan-code-hotspots.py"
    if not hotspot_script.is_file():
        errors.append("缺少代码热点扫描脚本: scripts/scan-code-hotspots.py")

    context_audit = root / "scripts" / "audit-context.py"
    if not context_audit.is_file():
        errors.append("缺少上下文预算审计脚本: scripts/audit-context.py")
    else:
        result = subprocess.run(
            [sys.executable, str(context_audit)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors.append(result.stdout.strip() or result.stderr.strip() or "上下文预算审计失败")

    skills_dir = root / "skills"
    actual = {p.name for p in skills_dir.iterdir() if p.is_dir()}
    if actual != EXPECTED_SKILLS:
        errors.append(
            "Skill目录不匹配: 缺少="
            + ",".join(sorted(EXPECTED_SKILLS - actual))
            + " 多余="
            + ",".join(sorted(actual - EXPECTED_SKILLS))
        )

    names: set[str] = set()
    forbidden_runtime_terms = (
        "using-superpowers",
        "superpowers:",
        "docs/superpowers/",
        ".superpowers/",
    )

    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"缺少 {skill_dir.name}/SKILL.md")
            continue
        text = skill_file.read_text(encoding="utf-8")
        try:
            fm = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(f"{skill_file}: {exc}")
            continue
        name = fm.get("name", "")
        description = fm.get("description", "")
        if name != skill_dir.name:
            errors.append(f"{skill_file}: name与目录不一致")
        if name in names:
            errors.append(f"重复Skill name: {name}")
        names.add(name)
        if not description or "TODO" in description:
            errors.append(f"{skill_file}: description缺失或仍含TODO")
        if "[TODO:" in text:
            errors.append(f"{skill_file}: 仍含脚手架占位符")
        for term in forbidden_runtime_terms:
            if term.lower() in text.lower():
                errors.append(f"{skill_file}: 含禁用运行时词 {term}")

    for markdown_file in sorted(root.rglob("*.md")):
        markdown_text = markdown_file.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown_text):
            if "://" in link or link.startswith("#"):
                continue
            relative = link.split("#", 1)[0]
            if not relative:
                continue
            target = (markdown_file.parent / relative).resolve()
            if not target.exists():
                errors.append(f"{markdown_file}: 相对链接不存在 {link}")

    for runtime_file in sorted(p for p in skills_dir.rglob("*") if p.is_file()):
        try:
            runtime_text = runtime_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for term in forbidden_runtime_terms:
            if term.lower() in runtime_text.lower():
                errors.append(f"{runtime_file}: 含禁用运行时词 {term}")

    if errors:
        print("帧芯开发工作流6.2校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"帧芯开发工作流6.2静态包校验通过：{len(EXPECTED_SKILLS)}个Skill，manifest、界面版本、frontmatter、链接、命名、上下文预算和测试文件清单检查正常；运行脚本需另行烟测。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
