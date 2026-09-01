#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "用法: $0 <要检查的文件或目录> <测试文件模式>" >&2
  echo "示例: $0 '.git' 'src/**/*.test.ts'" >&2
  exit 2
fi

pollution_check=$1
test_pattern=${2#./}

echo "正在查找会创建以下内容的测试: $pollution_check"
echo "测试文件模式: $test_pattern"

test_files=$(find . \( -path "./$test_pattern" -o -path "./${test_pattern//\*\*\//}" \) | sort -u)
if [ -z "$test_files" ]; then
  echo "未找到匹配的测试文件。"
  exit 3
fi

total=$(printf '%s\n' "$test_files" | wc -l | tr -d ' ')
count=0

while IFS= read -r test_file; do
  count=$((count + 1))

  if [ -e "$pollution_check" ]; then
    echo "在运行第 $count/$total 个测试前污染目标已经存在: $pollution_check" >&2
    exit 4
  fi

  echo "[$count/$total] 运行: $test_file"
  npm test "$test_file" >/dev/null 2>&1 || true

  if [ -e "$pollution_check" ]; then
    echo "找到污染源测试: $test_file"
    echo "创建了: $pollution_check"
    ls -la "$pollution_check"
    exit 1
  fi
done <<< "$test_files"

echo "未发现污染源，所有匹配测试运行后目标都不存在。"
