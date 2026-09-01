#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "用法: task-brief.sh PLAN_FILE TASK_NUMBER [OUTFILE]" >&2
  exit 2
fi

plan=$1
task_number=$2
[ -f "$plan" ] || { echo "计划文件不存在: $plan" >&2; exit 2; }
[[ "$task_number" =~ ^[1-9][0-9]*$ ]] || { echo "Task编号必须是正整数: $task_number" >&2; exit 2; }

if [ "$#" -eq 3 ]; then
  output=$3
else
  script_dir=$(cd "$(dirname "$0")" && pwd)
  workspace=$("$script_dir/execution-workspace.sh" "$plan")
  output="$workspace/task-briefs/task-$task_number.md"
fi

mkdir -p "$(dirname "$output")"

awk -v n="$task_number" '
  /^```/ { in_fence = !in_fence }
  !in_fence && /^#+[[:space:]]/ {
    match($0, /^#+/)
    heading_level = RLENGTH
    if (in_task && heading_level <= task_level) exit
    if ($0 ~ ("^#+[[:space:]]+Task[[:space:]]+" n "([^0-9]|$)")) {
      in_task = 1
      task_level = heading_level
    }
  }
  in_task { print }
' "$plan" > "$output"

if [ ! -s "$output" ]; then
  echo "在计划中找不到 Task $task_number: $plan" >&2
  exit 3
fi

echo "已写入 ${output}，共 $(wc -l < "$output" | tr -d ' ') 行"
