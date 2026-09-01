#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "用法: execution-workspace.sh PLAN_FILE" >&2
  exit 2
fi

plan=$1
[ -f "$plan" ] || { echo "计划文件不存在: $plan" >&2; exit 2; }

plan_dir=$(cd "$(dirname "$plan")" && pwd -P)
plan_abs="$plan_dir/$(basename "$plan")"
plan_identity=$(printf '%s\n' "$plan_abs" | git hash-object --stdin)

plan_contract_digest() {
  awk '
    /^```/ { in_fence = !in_fence }
    {
      if (!in_fence && in_rework && $0 ~ /^#+[[:space:]]/) in_rework = 0
      if (!in_fence && $0 ~ /^\*\*Rework:\*\*/) { in_rework = 1; next }
      if (in_rework) next
      if (!in_fence && $0 ~ /^\*\*(Status|Remaining):\*\*/) next
      line = $0
      if (!in_fence) gsub(/\[[ xX]\]/, "[ ]", line)
      print line
    }
  ' "$1" | git hash-object --stdin
}

plan_digest=$(plan_contract_digest "$plan_abs")

slug=$(basename "$plan" .md | tr -cs 'A-Za-z0-9._-' '-')
slug=${slug#-}
slug=${slug%-}
[ -n "$slug" ] || { echo "无法从计划文件生成执行目录名: $plan" >&2; exit 2; }

repo_root=$(git rev-parse --show-toplevel)
if base_commit=$(git rev-parse --verify HEAD 2>/dev/null); then
  :
else
  base_commit="UNBORN"
fi
base="$repo_root/.codex/execution"
target="$base/$slug-${plan_identity:0:10}"

mkdir -p "$target/task-briefs" "$target/reports" "$target/reviews"
printf '*\n' > "$base/.gitignore"

if [ ! -f "$target/progress.md" ]; then
  {
    echo "# 执行进度"
    echo
    echo "**Plan:** \`$plan_abs\`"
    echo "**Plan Identity:** \`$plan_identity\`"
    echo "**Initial Plan Contract Digest:** \`$plan_digest\`"
    echo "**Last Seen Plan Contract Digest:** \`$plan_digest\`"
    echo "**Base:** \`$base_commit\`"
    echo "**Current Batch:** \`TODO\`"
    echo
    echo "## Completed"
    echo
    echo "- NONE"
    echo
    echo "## Current"
    echo
    echo "- NONE"
    echo
    echo "## Tasks"
    echo
    echo "| Task | Status | Round | Report | Evidence |"
    echo "|---|---|---:|---|---|"
    echo "| NONE | TODO | 0 | - | - |"
    echo
    echo "## Blockers"
    echo
    echo "- NONE"
    echo
    echo "## Rulings"
    echo
    echo "- NONE"
  } > "$target/progress.md"
else
  stored_identity=$(sed -n 's/^\*\*Plan Identity:\*\* `\([^`]*\)`.*/\1/p' "$target/progress.md" | head -1)
  if [ "$stored_identity" != "$plan_identity" ]; then
    echo "执行目录中的Plan Identity与当前计划不一致，拒绝恢复: $target" >&2
    exit 3
  fi

  stored_digest=$(sed -n 's/^\*\*Last Seen Plan Contract Digest:\*\* `\([^`]*\)`.*/\1/p' "$target/progress.md" | head -1)
  if [ -z "$stored_digest" ]; then
    stored_digest=$(sed -n 's/^\*\*Initial Plan Contract Digest:\*\* `\([^`]*\)`.*/\1/p' "$target/progress.md" | head -1)
  fi
  if [ -z "$stored_digest" ]; then
    stored_digest=$(sed -n 's/^\*\*Initial Plan Digest:\*\* `\([^`]*\)`.*/\1/p' "$target/progress.md" | head -1)
  fi
  if [ -n "$stored_digest" ] && [ "$stored_digest" != "$plan_digest" ]; then
    echo "提示：Plan合同内容有变化；恢复前必须核对Files、Interfaces、Acceptance、Steps和Verification。" >&2
    tmp_progress="$target/progress.md.tmp.$$"
    awk -v digest="$plan_digest" '
      /^\*\*Last Seen Plan Contract Digest:\*\*/ {
        print "**Last Seen Plan Contract Digest:** `" digest "`"
        updated = 1
        next
      }
      { print }
      END {
        if (!updated) print "\n**Last Seen Plan Contract Digest:** `" digest "`"
      }
    ' "$target/progress.md" > "$tmp_progress"
    mv "$tmp_progress" "$target/progress.md"
  fi
fi

cd "$target"
pwd
