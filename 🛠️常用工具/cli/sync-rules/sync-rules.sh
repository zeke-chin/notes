#!/usr/bin/env bash
set -euo pipefail

TARGET="${RULES_FILE:-.rules.md}"
LINKS=(AGENTS.md CLAUDE.md)
INCLUDE_GEMINI=false
DIR="."

while (( $# > 0 )); do
  case "$1" in
    -g|--gemini)
      INCLUDE_GEMINI=true
      shift
      ;;
    -h|--help)
      echo "用法: $(basename "$0") [-g|--gemini] [项目目录]"
      echo "  -g, --gemini  额外纳入 GEMINI.md（默认仅 AGENTS.md、CLAUDE.md）"
      echo "环境变量: RULES_FILE 可自定义真实文件名（默认 .rules.md）"
      exit 0
      ;;
    -*)
      echo "未知参数: $1" >&2
      exit 1
      ;;
    *)
      DIR="$1"
      shift
      ;;
  esac
done

if $INCLUDE_GEMINI; then
  LINKS+=(GEMINI.md)
fi

cd "$DIR"

# 1. 收集现有的真实文件（排除软链接）
candidates=()
if [[ -f "$TARGET" && ! -L "$TARGET" ]]; then
  candidates+=("$TARGET")
fi
for f in "${LINKS[@]}"; do
  if [[ "$f" != "$TARGET" && -f "$f" && ! -L "$f" ]]; then
    candidates+=("$f")
  fi
done

# 2. 决定保留哪一个作为真实规则文件
if (( ${#candidates[@]} == 0 )); then
  if [[ -L "$TARGET" ]]; then
    rm "$TARGET"
  fi
  touch "$TARGET"
  echo "已创建空的 $TARGET"
else
  if (( ${#candidates[@]} == 1 )); then
    chosen="${candidates[0]}"
  else
    echo "发现多个规则文件，请选择要保留哪一个作为 ${TARGET}："
    PS3="输入编号: "
    select chosen in "${candidates[@]}"; do
      [[ -n "${chosen:-}" ]] && break
    done
    [[ -n "${chosen:-}" ]] || exit 1
  fi

  if [[ "$chosen" != "$TARGET" ]]; then
    mv -f "$chosen" "$TARGET"
    echo "已将 $chosen 设为 $TARGET"
  else
    echo "保留已存在的 $TARGET"
  fi
fi

# 3. 统一指向 $TARGET（ln -sfn 会直接覆盖旧文件或旧软链接）
for f in "${LINKS[@]}"; do
  if [[ "$f" == "$TARGET" ]]; then
    continue
  fi
  ln -sfn "$TARGET" "$f"
  echo "$f -> $TARGET"
done
