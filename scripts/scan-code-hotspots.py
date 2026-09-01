#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SOURCE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".dart", ".ex", ".exs", ".go",
    ".h", ".hpp", ".html", ".java", ".js", ".jsx", ".kt", ".kts", ".lua",
    ".m", ".mjs", ".mm", ".mts", ".php", ".py", ".rb", ".rs", ".scala",
    ".scss", ".sh", ".sql", ".svelte", ".swift", ".ts", ".tsx", ".vue",
    ".cjs", ".cts",
}
EXCLUDED_PARTS = {
    ".git", ".next", ".nuxt", ".output", ".turbo", ".venv", "build",
    "coverage", "dist", "generated", "migrations", "node_modules", "out",
    "snapshots", "third_party", "vendor", "vendors",
}
TEST_PARTS = {"test", "tests", "__tests__", "spec", "specs"}


@dataclass
class FileResult:
    path: str
    kind: str
    lines: int
    base_lines: int | None
    delta: int | None
    tracked: bool
    new_file: bool
    status: str
    reason: str


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=root, check=False, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )


def git_paths(root: Path) -> tuple[list[Path], set[str], set[str]] | None:
    inside = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside.returncode != 0 or inside.stdout.strip() != b"true":
        return None
    listed = run_git(root, ["ls-files", "--cached", "--others", "--exclude-standard", "-z"])
    tracked = run_git(root, ["ls-files", "--cached", "-z"])
    staged_new = run_git(root, ["diff", "--cached", "--name-only", "--diff-filter=A", "-z"])
    if listed.returncode != 0 or tracked.returncode != 0 or staged_new.returncode != 0:
        return None
    paths = [Path(raw.decode("utf-8", "surrogateescape")) for raw in listed.stdout.split(b"\0") if raw]
    tracked_set = {
        raw.decode("utf-8", "surrogateescape") for raw in tracked.stdout.split(b"\0") if raw
    }
    staged_new_set = {
        raw.decode("utf-8", "surrogateescape") for raw in staged_new.stdout.split(b"\0") if raw
    }
    return paths, tracked_set, staged_new_set


def filesystem_paths(root: Path) -> tuple[list[Path], set[str], set[str]]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file():
            paths.append(path.relative_to(root))
    return paths, {path.as_posix() for path in paths}, set()


def is_generated_or_excluded(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    return bool(lowered_parts & EXCLUDED_PARTS) or any(
        marker in name for marker in (".generated.", ".min.", ".snap")
    )


def is_test(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts[:-1]}
    name = path.name.lower()
    return bool(lowered_parts & TEST_PARTS) or any(
        marker in name for marker in (".test.", ".spec.", "_test.", "_spec.")
    )


def count_lines(data: bytes) -> int | None:
    if b"\0" in data[:8192]:
        return None
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def base_line_count(root: Path, base: str | None, rel: Path) -> int | None:
    if not base or base == "UNBORN":
        return None
    shown = run_git(root, ["show", f"{base}:{rel.as_posix()}"])
    if shown.returncode != 0:
        return None
    return count_lines(shown.stdout)


def classify(
    *, kind: str, lines: int, tracked: bool, new_file: bool, base_requested: bool,
    base_lines: int | None,
) -> tuple[str, str]:
    hard_limit = 1500 if kind == "TEST" else 1000
    warning_limit = 1000 if kind == "TEST" else 600

    if base_requested:
        if base_lines is None and lines > hard_limit:
            return "VIOLATION", f"新增文件超过{hard_limit}行硬上限"
        if base_lines is not None and base_lines <= hard_limit < lines:
            return "VIOLATION", f"从{base_lines}行增长并跨过{hard_limit}行硬上限"
        if base_lines is not None and base_lines > hard_limit and lines > base_lines:
            return "VIOLATION", f"既有超限文件从{base_lines}行增长到{lines}行"

    if lines > hard_limit:
        if new_file and not base_requested:
            return "VIOLATION", f"新增文件超过{hard_limit}行硬上限"
        return "NO_GROWTH", f"既有热点；不得超过当前{lines}行"
    if warning_limit is not None and lines > warning_limit:
        return "WARNING", f"超过{warning_limit}行预警线"
    return "OK", ""


def scan(root: Path, base: str | None, allowed_over_limit: set[str]) -> tuple[list[FileResult], int]:
    discovered = git_paths(root)
    paths, tracked_set, staged_new_set = discovered if discovered is not None else filesystem_paths(root)
    results: list[FileResult] = []
    total_lines = 0

    for rel in sorted(set(paths), key=lambda item: item.as_posix()):
        if rel.suffix.lower() not in SOURCE_EXTENSIONS or is_generated_or_excluded(rel):
            continue
        absolute = root / rel
        if not absolute.is_file() or absolute.is_symlink():
            continue
        try:
            data = absolute.read_bytes()
        except OSError:
            continue
        lines = count_lines(data)
        if lines is None:
            continue
        tracked = rel.as_posix() in tracked_set
        new_file = not tracked or rel.as_posix() in staged_new_set
        old_lines = base_line_count(root, base, rel) if base else None
        kind = "TEST" if is_test(rel) else "SOURCE"
        status, reason = classify(
            kind=kind, lines=lines, tracked=tracked, new_file=new_file,
            base_requested=bool(base), base_lines=old_lines,
        )
        if status == "VIOLATION" and rel.as_posix() in allowed_over_limit:
            status = "EXCEPTION"
            reason = f"Plan显式批准例外；{reason}"
        delta = lines - old_lines if old_lines is not None else None
        results.append(FileResult(rel.as_posix(), kind, lines, old_lines, delta, tracked, new_file, status, reason))
        total_lines += lines

    return sorted(results, key=lambda item: (-item.lines, item.path)), total_lines


def print_markdown(root: Path, results: list[FileResult], total_lines: int, top: int, base: str | None) -> None:
    hotspots = [item for item in results if item.status != "OK"]
    print("# 代码热点扫描")
    print()
    print(f"- 项目：`{root}`")
    print(f"- 代码文件：{len(results)}")
    print(f"- 总行数：{total_lines}")
    print(f"- 对比基线：`{base or 'NONE'}`")
    print("- 规则：普通源文件600行预警、1000行硬上限；测试文件1000行预警、1500行硬上限；既有超限文件no-growth。")
    print("- EXCEPTION：只由显式--allow-over-limit路径产生，不阻断check；Plan必须记录原因和边界。")
    print()
    print("## 热点")
    print()
    if not hotspots:
        print("NONE")
    else:
        print("| 状态 | 行数 | 基线 | 类型 | 文件 | 原因 |")
        print("|---|---:|---:|---|---|---|")
        for item in hotspots:
            baseline = "-" if item.base_lines is None else str(item.base_lines)
            print(f"| {item.status} | {item.lines} | {baseline} | {item.kind} | `{item.path}` | {item.reason} |")
    print()
    print(f"## 最大的{min(top, len(results))}个代码文件")
    print()
    for item in results[:top]:
        print(f"- {item.lines:>6}  `{item.path}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="扫描项目代码行数并识别热点文件")
    parser.add_argument("--root", default=".", help="项目根目录，默认当前目录")
    parser.add_argument("--base", help="可选Git基线，用于检查硬上限和no-growth；空仓库可传UNBORN")
    parser.add_argument("--top", type=int, default=20, help="展示最大的代码文件数量")
    parser.add_argument("--json", action="store_true", help="输出JSON")
    parser.add_argument("--check", action="store_true", help="存在VIOLATION时返回非零")
    parser.add_argument(
        "--allow-over-limit", action="append", default=[], metavar="PATH",
        help="显式批准一个项目内相对路径超过硬上限；可重复，Plan必须记录原因和边界",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"项目目录不存在: {root}")
    if args.top < 1:
        parser.error("--top必须大于0")
    if args.base and args.base != "UNBORN":
        verified = run_git(root, ["rev-parse", "--verify", f"{args.base}^{{commit}}"])
        if verified.returncode != 0:
            parser.error(f"Git基线无效: {args.base}")

    allowed_over_limit: set[str] = set()
    for raw_path in args.allow_over_limit:
        candidate = Path(raw_path)
        if candidate.is_absolute():
            try:
                candidate = candidate.resolve().relative_to(root)
            except ValueError:
                parser.error(f"例外路径不在项目内: {raw_path}")
        if ".." in candidate.parts or candidate.as_posix() in ("", "."):
            parser.error(f"例外路径无效: {raw_path}")
        allowed_over_limit.add(candidate.as_posix())

    results, total_lines = scan(root, args.base, allowed_over_limit)
    scanned_paths = {item.path for item in results}
    unknown_exceptions = allowed_over_limit - scanned_paths
    if unknown_exceptions:
        parser.error("例外路径未被扫描: " + ", ".join(sorted(unknown_exceptions)))
    violations = [item for item in results if item.status == "VIOLATION"]
    exceptions = [item for item in results if item.status == "EXCEPTION"]
    if args.json:
        print(json.dumps({
            "root": str(root), "base": args.base, "files": len(results),
            "total_lines": total_lines, "violations": len(violations),
            "exceptions": len(exceptions),
            "results": [asdict(item) for item in results],
        }, ensure_ascii=False, indent=2))
    else:
        print_markdown(root, results, total_lines, args.top, args.base)
    return 1 if args.check and violations else 0


if __name__ == "__main__":
    sys.exit(main())
