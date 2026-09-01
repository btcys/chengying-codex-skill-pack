#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from typing import Any


PLUGIN_NAME = "zhenxin-development-workflow"


def codex_json(*args: str) -> dict[str, Any]:
    result = subprocess.run(
        ["codex", "plugin", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "未知错误"
        raise RuntimeError(message)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Codex没有返回有效JSON，未执行手动删除。") from exc


def installed_matches(data: dict[str, Any]) -> list[dict[str, Any]]:
    installed = data.get("installed", [])
    if not isinstance(installed, list):
        raise RuntimeError("Codex插件列表格式异常，未执行卸载。")
    if any(not isinstance(item, dict) for item in installed):
        raise RuntimeError("Codex插件安装项格式异常，未执行卸载。")
    return [item for item in installed if item.get("name") == PLUGIN_NAME]


def main() -> int:
    parser = argparse.ArgumentParser(description="安全卸载帧芯开发工作流插件")
    parser.add_argument("--marketplace", help="存在多个同名安装时指定准确marketplace")
    parser.add_argument("--dry-run", action="store_true", help="只检测，不执行卸载")
    args = parser.parse_args()

    if shutil.which("codex") is None:
        print("找不到codex命令，未执行卸载。", file=sys.stderr)
        return 2

    try:
        before = codex_json("list", "--available", "--json")
        all_matches = installed_matches(before)
    except RuntimeError as exc:
        print(f"无法读取插件安装状态：{exc}", file=sys.stderr)
        return 2

    matches = all_matches
    if args.marketplace:
        matches = [item for item in matches if item.get("marketplaceName") == args.marketplace]
        if all_matches and not matches:
            names = ", ".join(sorted(str(item.get("marketplaceName")) for item in all_matches))
            print(
                f"没有找到marketplace={args.marketplace}的安装；当前匹配为：{names}。未执行卸载。",
                file=sys.stderr,
            )
            return 3

    if not matches:
        print("帧芯开发工作流当前未安装；没有修改任何项目或插件源文件。")
        return 0

    if len(matches) > 1:
        names = ", ".join(sorted(str(item.get("marketplaceName")) for item in matches))
        print(f"检测到多个同名安装：{names}。请使用 --marketplace 指定一个。", file=sys.stderr)
        return 3

    marketplace = matches[0].get("marketplaceName")
    if not isinstance(marketplace, str) or not marketplace:
        print("安装记录缺少marketplaceName，未执行卸载。", file=sys.stderr)
        return 2

    selector = f"{PLUGIN_NAME}@{marketplace}"
    if args.dry_run:
        print(f"将卸载：{selector}")
        print("将保留插件源文件以及所有项目代码、文档、截图和执行记录。")
        return 0

    try:
        codex_json("remove", selector, "--json")
        after = codex_json("list", "--available", "--json")
        remaining = [
            item
            for item in installed_matches(after)
            if item.get("marketplaceName") == marketplace
        ]
    except RuntimeError as exc:
        print(f"卸载失败：{exc}", file=sys.stderr)
        return 1

    if remaining:
        print(f"Codex仍报告{selector}已安装，请检查插件状态。", file=sys.stderr)
        return 1

    print(f"已卸载：{selector}")
    print("插件源文件和所有项目资料均已保留。请新开Codex任务以使用更新后的Skill列表。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
