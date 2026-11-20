#!/usr/bin/env bash
# 把一个目录往下若干层的子目录批量加入 zoxide 索引，新机器上不用先 cd 一遍就能用 z / zi 跳转。
#
# 用法：zoxide-index.sh [选项] <起始目录>
# 示例：zoxide-index.sh -d 2 -e old_work /Users/zeke/workspace

set -eo pipefail

# 默认排除：隐藏目录、依赖和构建产物。可以用 -i 把其中某项加回来。
DEFAULT_EXCLUDES=('.*' node_modules __pycache__ .venv venv dist build target vendor)

usage() {
  cat <<'EOF'
用法：zoxide-index.sh [选项] <起始目录>

把 <起始目录> 及其往下若干层的子目录加入 zoxide 索引。

选项：
  -d, --depth N        往下扫描的层数，默认 2（起始目录本身总会加入）
  -e, --exclude 名称   排除该名称的目录及其下所有内容，可重复；支持通配符，如 'old_*'
  -i, --include 名称   不排除该名称的目录，可重复；用来加回默认排除的目录，如 .config
  -n, --dry-run        只列出会加入的目录，不写入 zoxide
  -h, --help           显示帮助

默认排除：.* node_modules __pycache__ .venv venv dist build target vendor
名称按目录名（最后一级）匹配；-i 优先于 -e 和默认排除。

示例：
  zoxide-index.sh -d 2 -e old_work /Users/zeke/workspace
  zoxide-index.sh -d 1 -i .config ~
EOF
}

die() {
  echo "错误：$*" >&2
  echo "运行 zoxide-index.sh --help 查看用法。" >&2
  exit 1
}

depth=2
dry_run=0
root=""
excludes=("${DEFAULT_EXCLUDES[@]}")
includes=()

while (($#)); do
  case $1 in
    -d|--depth)
      [[ $# -ge 2 ]] || die "$1 需要一个数字"
      depth=$2; shift 2 ;;
    -e|--exclude)
      [[ $# -ge 2 ]] || die "$1 需要一个目录名"
      excludes+=("$2"); shift 2 ;;
    -i|--include)
      [[ $# -ge 2 ]] || die "$1 需要一个目录名"
      includes+=("$2"); shift 2 ;;
    -n|--dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    -*) die "未知选项 $1" ;;
    *)
      [[ -z $root ]] || die "只能指定一个起始目录，多出了 $1"
      root=$1; shift ;;
  esac
done
if (($#)); then
  [[ -z $root && $# -eq 1 ]] || die "只能指定一个起始目录"
  root=$1
fi

[[ -n $root ]] || { usage >&2; exit 1; }
[[ $depth =~ ^[0-9]+$ ]] || die "层数必须是非负整数：$depth"
[[ -d $root ]] || die "目录不存在：$root"
((dry_run)) || command -v zoxide >/dev/null || die "没有找到 zoxide，先安装：brew install zoxide"

root=$(cd "$root" && pwd -P)

# find 表达式：名称命中排除列表且不在包含列表里的目录，整个剪掉。
expr=(\( -false)
for name in "${excludes[@]}"; do expr+=(-o -name "$name"); done
expr+=(\))
if ((${#includes[@]})); then
  expr+=(! \( -false)
  for name in "${includes[@]}"; do expr+=(-o -name "$name"); done
  expr+=(\))
fi

dirs=()
while IFS= read -r -d '' dir; do
  dirs+=("$dir")
done < <(find "$root" -mindepth 1 -maxdepth "$depth" -type d \( "${expr[@]}" -prune -o -print0 \))
dirs=("$root" "${dirs[@]}")

if ((dry_run)); then
  printf '%s\n' "${dirs[@]}"
  echo "共 ${#dirs[@]} 个目录（预览，未写入）" >&2
  exit 0
fi

zoxide add -- "${dirs[@]}"
echo "已加入 ${#dirs[@]} 个目录到 zoxide 索引。用 zi 交互选择，或 zoxide query -l 查看全部。" >&2
