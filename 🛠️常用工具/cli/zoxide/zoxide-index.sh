#!/usr/bin/env bash
# 把一个目录往下若干层的子目录批量加入 zoxide 索引，新机器上不用先 cd 一遍就能用 z / zi 跳转。
# 写入前用树形展示要加入的目录，确认后再写。
#
# 用法：zoxide-index.sh [选项] <起始目录>
# 示例：zoxide-index.sh -d 2 -e old_work /Users/zeke/workspace

set -eo pipefail

# 默认排除：隐藏目录、依赖和构建产物。可以用 -i 把其中某项加回来。
DEFAULT_EXCLUDES=('.*' '*.app' node_modules __pycache__ .venv venv dist build target vendor)

usage() {
  cat <<'EOF'
用法：zoxide-index.sh [选项] <起始目录>

把 <起始目录> 及其往下若干层的子目录加入 zoxide 索引。写入前展示目录树并要求确认。

选项：
  -d, --depth N        往下扫描的层数，默认 2（起始目录本身总会加入）
  -e, --exclude 名称   排除该名称的目录及其下所有内容，可重复；支持通配符，如 'old_*'
  -i, --include 名称   不排除该名称的目录，可重复；用来加回默认排除的目录，如 .config
  -n, --dry-run        只展示，不写入
  -a, --all            展示时列出已在索引的全部目录（灰色）；默认只列新目录及其上级
  -y, --yes            不询问，直接写入（脚本里调用时用）
  -h, --help           显示帮助

默认排除：.* *.app node_modules __pycache__ .venv venv dist build target vendor
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
show_all=0
yes=0
root=""
user_excludes=()
includes=()

while (($#)); do
  case $1 in
    -d|--depth)
      [[ $# -ge 2 ]] || die "$1 需要一个数字"
      depth=$2; shift 2 ;;
    -e|--exclude)
      [[ $# -ge 2 ]] || die "$1 需要一个目录名"
      user_excludes+=("$2"); shift 2 ;;
    -i|--include)
      [[ $# -ge 2 ]] || die "$1 需要一个目录名"
      includes+=("$2"); shift 2 ;;
    -n|--dry-run) dry_run=1; shift ;;
    -a|--all) show_all=1; shift ;;
    -y|--yes) yes=1; shift ;;
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
command -v zoxide >/dev/null || die "没有找到 zoxide，先安装：brew install zoxide"
if ((!dry_run && !yes)) && ! { : </dev/tty; } 2>/dev/null; then
  die "没有终端可以确认；非交互运行请加 -y"
fi

root=$(cd "$root" && pwd -P)
excludes=("${DEFAULT_EXCLUDES[@]}" ${user_excludes[@]+"${user_excludes[@]}"})

# find 表达式：名称命中排除列表且不在包含列表里的目录，整个剪掉。
expr=(\( -false)
for name in "${excludes[@]}"; do expr+=(-o -name "$name"); done
expr+=(\))
if ((${#includes[@]})); then
  expr+=(! \( -false)
  for name in "${includes[@]}"; do expr+=(-o -name "$name"); done
  expr+=(\))
fi

dirs=("$root")
skipped=()
while IFS= read -r -d '' line; do
  case $line in
    D*) dirs+=("${line#D}") ;;
    S*) skipped+=("${line#S}") ;;
  esac
done < <(find "$root" -mindepth 1 -maxdepth "$depth" -type d \
  \( "${expr[@]}" -prune -exec printf 'S%s\0' {} + -o -exec printf 'D%s\0' {} + \) 2>/dev/null)

# 被 -e 排除的单独列出；默认排除的（.git 等）只计数。
user_skipped=()
default_skipped=0
for path in ${skipped[@]+"${skipped[@]}"}; do
  name=${path##*/} hit=""
  for pat in ${user_excludes[@]+"${user_excludes[@]}"}; do
    # shellcheck disable=SC2053  # 有意按通配符匹配
    if [[ $name == $pat ]]; then hit=$pat; break; fi
  done
  if [[ -n $hit ]]; then
    user_skipped+=("${path#"$root"/}/	$hit")
  else
    default_skipped=$((default_skipped + 1))
  fi
done

color=0
[[ -t 1 && -z ${NO_COLOR:-} ]] && color=1

render() {
  printf '起始目录：%s（往下 %s 层）\n' "$root" "$depth"
  printf '排除：%s\n' "${excludes[*]}"
  ((${#includes[@]})) && printf '包括：%s\n' "${includes[*]}"
  echo

  # 按路径分段排序（把 / 换成最小的字符），保证子目录紧跟在父目录后面，再画成树。
  printf '%s\n' "${dirs[@]}" | awk '{ gsub("/", "\001"); print }' | LC_ALL=C sort | tr '\001' '/' |
    awk -v root="$root" -v color="$color" -v all="$show_all" '
      NR == FNR { have[$0] = 1; next }
      { path[++n] = $0 }
      END {
        dim = color ? "\033[2m" : ""; bold = color ? "\033[1m" : ""; reset = color ? "\033[0m" : ""
        rl = length(root)
        added = 0; existing = 0
        for (i = 1; i <= n; i++) {
          old[i] = (path[i] in have)
          if (old[i]) existing++; else added++
          if (path[i] == root) { depth[i] = 0; continue }
          rel = substr(path[i], rl + 2)
          depth[i] = split(rel, parts, "/")
          name[i] = parts[depth[i]]
          parent[i] = substr(rel, 1, length(rel) - length(name[i]))
        }
        # 默认只展示新目录，以及它们的上级（即使已有，也要显示出来才能看清位置）。
        for (i = 1; i <= n; i++) {
          keep[i] = all || !old[i] || depth[i] == 0
          for (j = i + 1; !keep[i] && j <= n && depth[j] > depth[i]; j++) if (!old[j]) keep[i] = 1
        }
        # 只在展示出来的同级目录里判断谁是最后一个，决定画 ├── 还是 └──。
        for (i = 1; i <= n; i++) {
          last[i] = 1
          for (j = i + 1; j <= n; j++) {
            if (!keep[j]) continue
            if (depth[j] < depth[i]) break
            if (depth[j] == depth[i]) { if (parent[j] == parent[i]) last[i] = 0; break }
          }
        }
        for (i = 1; i <= n; i++) {
          if (!keep[i]) continue
          tag = old[i] ? "  (已有)" : ""
          if (depth[i] == 0) { printf "%s%s/%s%s%s\n", bold, root, reset, dim, tag reset; continue }
          prefix = ""
          for (d = 1; d < depth[i]; d++) prefix = prefix (lastAt[d] ? "    " : "│   ")
          lastAt[depth[i]] = last[i]
          branch = last[i] ? "└── " : "├── "
          if (old[i]) printf "%s%s%s%s/%s%s\n", prefix, branch, dim, name[i], tag, reset
          else printf "%s%s%s/\n", prefix, branch, name[i]
        }
        printf "\n共 %d 个目录：新加入 %d 个，已在索引 %d 个（会加分）\n", n, added, existing
        if (!all && existing > 0) printf "已在索引的目录只展示新目录的上级，加 -a 查看全部\n"
      }' <(zoxide query -l 2>/dev/null || true) -

  if ((${#user_skipped[@]})); then
    printf '\n按 -e 排除了 %d 个目录（连同其下内容）：\n' "${#user_skipped[@]}"
    for entry in "${user_skipped[@]}"; do
      printf '  %s  (%s)\n' "${entry%%	*}" "${entry#*	}"
    done
  fi
  ((default_skipped == 0)) || printf '默认排除跳过了 %d 个目录（隐藏目录、依赖和构建产物）\n' "$default_skipped"
}

if [[ -t 1 ]] && command -v less >/dev/null; then
  render | less -RFX
else
  render
fi

if ((dry_run)); then
  echo "（预览，未写入）"
  exit 0
fi

if ((!yes)); then
  printf '\n确认加入 zoxide 索引？[y/N] ' >/dev/tty
  read -r answer </dev/tty || answer=""
  case $answer in
    y|Y|yes|YES) ;;
    *) echo "已取消，未写入。"; exit 0 ;;
  esac
fi

zoxide add -- "${dirs[@]}"
echo "已加入 ${#dirs[@]} 个目录。用 zi 交互选择，或 zoxide query -l 查看全部。"
