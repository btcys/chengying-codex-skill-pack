#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "用法: prepare-review.sh BASE_REF OUTFILE" >&2
  exit 2
fi

base=$1
output=$2

if [ "$base" = "UNBORN" ]; then
  base_mode="unborn"
  empty_tree=$(git hash-object -t tree /dev/null)
else
  git rev-parse --verify --quiet "$base" >/dev/null || { echo "无效的基准引用: $base" >&2; exit 2; }
  base_mode="commit"
fi

if head_commit=$(git rev-parse --verify HEAD 2>/dev/null); then
  :
else
  head_commit="UNBORN"
fi
max_inline_diff_bytes=${REVIEW_INLINE_DIFF_MAX_BYTES:-${REVIEW_UNTRACKED_DIFF_MAX_BYTES:-200000}}
if ! [[ "$max_inline_diff_bytes" =~ ^[1-9][0-9]*$ ]]; then
  echo "REVIEW_INLINE_DIFF_MAX_BYTES必须是正整数" >&2
  exit 2
fi
mkdir -p "$(dirname "$output")"

if [ "$base_mode" = "unborn" ]; then
  diff_base=$empty_tree
else
  diff_base=$base
fi

scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/zhenxin-review.XXXXXX")
temp_output="$scratch_dir/review.md"
trap 'rm -rf "$scratch_dir"' EXIT

emit_tracked_diff() {
  local file=$1
  local ordinal=$2
  local current_size=0
  local base_size=0
  local current_blob="DELETED"
  local base_blob="NONE"
  local numstat=""
  local metadata_only="false"
  local reason=""
  local diff_file="$scratch_dir/tracked-$ordinal.diff"

  if [ -f "$file" ]; then
    current_size=$(wc -c < "$file" | tr -d ' ')
    current_blob=$(git hash-object --no-filters "$file")
  fi
  if base_blob=$(git rev-parse --verify "$diff_base:$file" 2>/dev/null); then
    base_size=$(git cat-file -s "$base_blob" 2>/dev/null || echo 0)
  else
    base_blob="NONE"
  fi
  numstat=$(git diff --numstat "$diff_base" -- "$file" || true)

  if printf '%s\n' "$numstat" | grep -Eq '^-[[:space:]]+-[[:space:]]+'; then
    metadata_only="true"
    reason="二进制文件"
  elif [ "$current_size" -gt "$max_inline_diff_bytes" ] || [ "$base_size" -gt "$max_inline_diff_bytes" ]; then
    metadata_only="true"
    reason="文件内容超过 ${max_inline_diff_bytes} bytes"
  else
    git diff --find-renames -U10 "$diff_base" -- "$file" > "$diff_file"
    diff_size=$(wc -c < "$diff_file" | tr -d ' ')
    if [ "$diff_size" -gt "$max_inline_diff_bytes" ]; then
      metadata_only="true"
      reason="diff超过 ${max_inline_diff_bytes} bytes"
    fi
  fi

  echo
  echo "### \`$file\`"
  if [ "$metadata_only" = "true" ]; then
    echo
    echo "- Current size: $current_size bytes"
    echo "- Base size: $base_size bytes"
    echo "- Current Git blob: \`$current_blob\`"
    echo "- Base Git blob: \`$base_blob\`"
    echo "- Numstat: \`${numstat:-NONE}\`"
    echo
    echo "${reason}；为控制Review上下文，仅记录元数据，Reviewer按需读取相关区段。"
  else
    echo '```diff'
    cat "$diff_file"
    echo '```'
  fi
}

{
  echo "# 独立Review材料"
  echo
  echo "**Base:** \`$base\`"
  echo "**Head:** \`$head_commit\`"
  echo
  echo "## 工作区状态"
  echo '```text'
  git status --short
  echo '```'
  echo
  echo "## 提交"
  echo '```text'
  if [ "$head_commit" = "UNBORN" ]; then
    echo "NONE"
  elif [ "$base_mode" = "unborn" ]; then
    git log --oneline HEAD
  else
    git log --oneline "$base..HEAD"
  fi
  echo '```'
  echo
  echo "## 变更统计"
  echo '```text'
  if [ "$base_mode" = "unborn" ]; then
    git diff --stat "$empty_tree"
  else
    git diff --stat "$base"
  fi
  echo '```'
  echo
  echo "## Tracked diff（受控上下文）"
  tracked_count=0
  while IFS= read -r -d '' file; do
    tracked_count=$((tracked_count + 1))
    emit_tracked_diff "$file" "$tracked_count"
  done < <(git diff --name-only -z "$diff_base")
  if [ "$tracked_count" -eq 0 ]; then
    echo
    echo "NONE"
  fi
  echo
  echo "## 未跟踪文件（自包含diff）"
  untracked_count=0
  while IFS= read -r -d '' file; do
    untracked_count=$((untracked_count + 1))
    echo
    echo "### \`$file\`"
    if [ -f "$file" ]; then
      size=$(wc -c < "$file" | tr -d ' ')
      hash=$(git hash-object --no-filters "$file")
      echo
      echo "- Size: $size bytes"
      echo "- Git blob: \`$hash\`"
      echo
      if [ "$size" -gt "$max_inline_diff_bytes" ]; then
        echo "文件超过 ${max_inline_diff_bytes} bytes；为控制Review上下文，仅记录元数据，Reviewer按需读取相关部分。"
      else
        untracked_diff="$scratch_dir/untracked-$untracked_count.diff"
        diff_status=0
        git diff --no-index --no-ext-diff -U10 -- /dev/null "$file" > "$untracked_diff" || diff_status=$?
        if [ "$diff_status" -gt 1 ]; then
          echo "生成未跟踪文件diff失败: $file" >&2
          exit "$diff_status"
        fi
        diff_size=$(wc -c < "$untracked_diff" | tr -d ' ')
        if [ "$diff_size" -gt "$max_inline_diff_bytes" ]; then
          echo "diff超过 ${max_inline_diff_bytes} bytes；为控制Review上下文，仅记录元数据，Reviewer按需读取相关区段。"
        else
          echo '```diff'
          cat "$untracked_diff"
          echo '```'
        fi
      fi
    else
      echo
      echo "非普通文件；Reviewer需按路径和实际类型检查。"
    fi
  done < <(git ls-files --others --exclude-standard -z)
  if [ "$untracked_count" -eq 0 ]; then
    echo
    echo "NONE"
  fi
} > "$temp_output"

mv "$temp_output" "$output"
trap - EXIT
rm -rf "$scratch_dir"

echo "已生成Review材料: $output ($(wc -c < "$output" | tr -d ' ') bytes)"
