#!/usr/bin/env bash
# install.sh - 安装「神算子周半仙」算命 agent 团队
#
# 用法:
#   bash install/install.sh
#   bash install/install.sh --target-dir ~/.claude/agents
#   bash install/install.sh --datapack-root /path/to/datapack
set -euo pipefail

TARGET_DIR="${HOME}/.zcode/agents"
DATAPACK_ROOT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --target-dir)    TARGET_DIR="$2"; shift 2 ;;
    --datapack-root) DATAPACK_ROOT="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$HERE")"
SRC_DIR="$REPO/agents"

echo
echo "=== 算命 agent 团队 安装程序 ==="
echo "源目录  : $SRC_DIR"
echo "目标目录: $TARGET_DIR"
if [ -n "$DATAPACK_ROOT" ]; then echo "数据包  : $DATAPACK_ROOT"; else echo "数据包  : 未指定（agent 将走降级路径，功能不受影响）"; fi
echo

[ -d "$SRC_DIR" ] || { echo "错误：找不到 agents 目录：$SRC_DIR" >&2; exit 1; }
mkdir -p "$TARGET_DIR"

if [ -n "$DATAPACK_ROOT" ]; then REPL="${DATAPACK_ROOT%/}"; else REPL="NOT_INSTALLED"; fi

count=0
for f in "$SRC_DIR"/*.md; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  # 替换占位符（用 | 作分隔符，避免路径里的 / 冲突）
  sed "s|{{DATAPACK_ROOT}}|$REPL|g" "$f" > "$TARGET_DIR/$base"
  printf '  [OK] %-30s %7s bytes\n' "$base" "$(wc -c < "$TARGET_DIR/$base" | tr -d ' ')"
  count=$((count+1))
done

echo
echo "已安装 $count 个 agent 到："
echo "  $TARGET_DIR"
echo
echo "下一步："
echo "  1) 重启宿主，使新 agent 被加载"
echo "  2) 在 agent 列表选择「神算子周半仙」开始提问"
echo "  3) 按 docs/VERIFY.md 做验收（尤其 V4 分诊与 V5 断网自包含性）"
echo
echo "自检：占位符解析"
if [ -n "$DATAPACK_ROOT" ]; then
  if grep -q '{{DATAPACK_ROOT}}' "$TARGET_DIR"/*.md 2>/dev/null; then
    echo "  [警告] 仍有未替换的占位符："
    grep -n '{{DATAPACK_ROOT}}' "$TARGET_DIR"/*.md | head -3
  else
    echo "  [通过] 占位符已全部替换为：$REPL"
  fi
else
  if grep -nE 'D:\\|Obsidian|/home/|/Users/' "$TARGET_DIR"/*.md 2>/dev/null | grep -v 'NOT_INSTALLED' >/dev/null 2>&1; then
    echo "  [警告] 发现残留的源码机绝对路径，agent 可能读取失败："
    grep -nE 'D:\\|Obsidian|/home/|/Users/' "$TARGET_DIR"/*.md | grep -v 'NOT_INSTALLED' | head -5
  else
    echo "  [通过] 无源码机绝对路径残留，已按降级模式安装（功能不受影响）"
  fi
fi
echo
