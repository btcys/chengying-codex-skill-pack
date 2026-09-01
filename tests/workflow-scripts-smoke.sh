#!/usr/bin/env bash
set -euo pipefail

package_root=$(cd "$(dirname "$0")/.." && pwd -P)
execution_script="$package_root/skills/subagent-driven-development/scripts/execution-workspace.sh"
brief_script="$package_root/skills/subagent-driven-development/scripts/task-brief.sh"
review_script="$package_root/skills/subagent-driven-development/scripts/prepare-review.sh"
hotspot_script="$package_root/scripts/scan-code-hotspots.py"

test_root=$(mktemp -d /tmp/zhenxin-workflow-scripts.XXXXXX)
trap 'rm -rf "$test_root"' EXIT

repo="$test_root/repo"
mkdir -p "$repo/docs/plans/0.1.0"
cd "$repo"
git init -q
git config user.name "Workflow Test"
git config user.email "workflow-test@example.invalid"

plan="docs/plans/0.1.0/0.1.0.1-smoke.md"
printf '%s\n' \
  '# Smoke Implementation Plan' \
  '' \
  '**Status:** `ACTIVE`' \
  '' \
  '### Task 1: Store' \
  '' \
  '**Status:** `TODO`' \
  '**Acceptance:**' \
  '- [ ] stores items' \
  '**Remaining:** `NONE`' \
  '**Rework:**' \
  '- NONE' \
  '' \
  '### Task 2: UI' \
  '' \
  '**Status:** `TODO`' \
  '**Acceptance:**' \
  '- [ ] renders items' \
  '**Remaining:** `NONE`' \
  '**Rework:**' \
  '- NONE' \
  '' \
  '## Plan Self-Review' \
  '' \
  '- Paths checked.' > "$plan"

first_stderr="$test_root/first.err"
workspace=$("$execution_script" "$plan" 2> "$first_stderr")
grep -Fq '**Base:** `UNBORN`' "$workspace/progress.md"
if grep -Fq 'fatal:' "$first_stderr"; then
  echo "unborn HEAD仍输出Git fatal" >&2
  exit 1
fi

status_plan="$test_root/status-plan.md"
sed -e 's/`ACTIVE`/`DONE`/' -e 's/\[ \]/[x]/g' "$plan" > "$status_plan"
mv "$status_plan" "$plan"
status_stderr="$test_root/status.err"
"$execution_script" "$plan" >/dev/null 2> "$status_stderr"
if grep -Fq 'Plan合同内容有变化' "$status_stderr"; then
  echo "纯状态更新错误触发合同变化警告" >&2
  exit 1
fi

printf '%s\n' '' '**Interfaces:**' '- `renderItems(items)`' >> "$plan"
contract_stderr="$test_root/contract.err"
"$execution_script" "$plan" >/dev/null 2> "$contract_stderr"
grep -Fq 'Plan合同内容有变化' "$contract_stderr"

repeat_stderr="$test_root/repeat.err"
"$execution_script" "$plan" >/dev/null 2> "$repeat_stderr"
if grep -Fq 'Plan合同内容有变化' "$repeat_stderr"; then
  echo "同一合同变化被重复警告" >&2
  exit 1
fi

brief="$test_root/task-2.md"
"$brief_script" "$plan" 2 "$brief" >/dev/null
grep -Fq '### Task 2: UI' "$brief"
if grep -Fq 'Plan Self-Review' "$brief"; then
  echo "最后一个Task仍泄漏后续Plan章节" >&2
  exit 1
fi

if "$brief_script" "$plan" 0 "$test_root/task-0.md" >/dev/null 2>&1; then
  echo "Task 0不应被接受" >&2
  exit 1
fi

mkdir -p src
printf '%s\n' 'export const staged = true;' > src/staged.js
git add src/staged.js

review="$workspace/reviews/smoke-review.md"
"$review_script" UNBORN "$review" >/dev/null
grep -Fq '**Base:** `UNBORN`' "$review"
grep -Fq '未跟踪文件（自包含diff）' "$review"
grep -Fq 'new file mode 100644' "$review"
grep -Fq 'renderItems(items)' "$review"
grep -Fq 'export const staged = true;' "$review"

git add docs src
git commit -qm "review baseline"
awk 'BEGIN { for (i = 1; i <= 30000; i++) print "large-line-" i "-abcdefghijklmnopqrstuvwxyz" }' > src/tracked-large.txt
git add src/tracked-large.txt
git commit -qm "add large tracked file"
printf '%s\n' 'large-line-30001-should-not-enter-review-material' >> src/tracked-large.txt
large_review="$workspace/reviews/large-review.md"
"$review_script" HEAD "$large_review" >/dev/null
grep -Fq '文件内容超过 200000 bytes' "$large_review"
if grep -Fq 'large-line-30001-should-not-enter-review-material' "$large_review"; then
  echo "超大tracked文件正文仍进入Review上下文" >&2
  exit 1
fi
if [ "$(wc -c < "$large_review" | tr -d ' ')" -gt 300000 ]; then
  echo "受控Review材料仍异常膨胀" >&2
  exit 1
fi

hotspot_repo="$test_root/hotspot-repo"
mkdir -p "$hotspot_repo/src"
cd "$hotspot_repo"
git init -q
git config user.name "Workflow Test"
git config user.email "workflow-test@example.invalid"
awk 'BEGIN { for (i = 1; i <= 1100; i++) print "export const line" i " = " i ";" }' > src/legacy-hotspot.ts
git add src/legacy-hotspot.ts
git commit -qm "baseline"

hotspot_report="$test_root/hotspots.md"
python3 "$hotspot_script" --root "$hotspot_repo" > "$hotspot_report"
grep -Fq '| NO_GROWTH | 1100 |' "$hotspot_report"

awk 'BEGIN { for (i = 1; i <= 601; i++) print "export const warning" i " = " i ";" }' > src/warning.ts
warning_report="$test_root/hotspot-warning.md"
if ! python3 "$hotspot_script" --root "$hotspot_repo" --check > "$warning_report"; then
  echo "601行普通源文件不应被硬阻断" >&2
  exit 1
fi
grep -Fq '| WARNING | 601 |' "$warning_report"
rm -f src/warning.ts

printf '%s\n' 'export const growth = true;' >> src/legacy-hotspot.ts
growth_report="$test_root/hotspot-growth.md"
if python3 "$hotspot_script" --root "$hotspot_repo" --base HEAD --check > "$growth_report"; then
  echo "既有超限文件增长未被热点检查拦截" >&2
  exit 1
fi
grep -Fq '既有超限文件从1100行增长到1101行' "$growth_report"

git show HEAD:src/legacy-hotspot.ts > src/legacy-hotspot.ts
awk 'BEGIN { for (i = 1; i <= 1001; i++) print "export const fresh" i " = " i ";" }' > src/new-large.ts
new_report="$test_root/hotspot-new.md"
if python3 "$hotspot_script" --root "$hotspot_repo" --base HEAD --check > "$new_report"; then
  echo "新增超限文件未被热点检查拦截" >&2
  exit 1
fi
grep -Fq '新增文件超过1000行硬上限' "$new_report"

git add src/new-large.ts
staged_new_report="$test_root/hotspot-staged-new.md"
if python3 "$hotspot_script" --root "$hotspot_repo" --check > "$staged_new_report"; then
  echo "已暂存新增超限文件未被无基线热点检查拦截" >&2
  exit 1
fi
grep -Fq '新增文件超过1000行硬上限' "$staged_new_report"

exception_report="$test_root/hotspot-exception.md"
python3 "$hotspot_script" --root "$hotspot_repo" --check \
  --allow-over-limit src/new-large.ts > "$exception_report"
grep -Fq '| EXCEPTION | 1001 |' "$exception_report"
rm -f src/new-large.ts

mkdir -p tests
awk 'BEGIN { for (i = 1; i <= 1501; i++) print "test(\"case" i "\", () => expect(true).toBe(true));" }' > tests/large.test.ts
test_report="$test_root/hotspot-test-limit.md"
if python3 "$hotspot_script" --root "$hotspot_repo" --base HEAD --check > "$test_report"; then
  echo "超过1500行的新增测试文件未被拦截" >&2
  exit 1
fi
grep -Fq '新增文件超过1500行硬上限' "$test_report"

echo "工作流脚本冒烟测试通过：UNBORN、合同摘要、Task边界、受控Review diff和代码热点检查均正常。"
