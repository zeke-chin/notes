# zoxide

- 简介：按使用频率和最近访问时间记住目录，输入部分名称就能跳转，替代 `cd`。
- 官网：https://github.com/ajeetdsouza/zoxide
- 安装：`brew install zoxide`（Ubuntu：`apt install zoxide`）。`zi` 的交互选择依赖 [fzf](../fzf/README.md)。

## 加载方式

在 `~/.zshrc` 中添加，要放在 `compinit` 之后（用 zim、oh-my-zsh 时放在它们的配置之后）：

```zsh
(( ! ${+commands[zoxide]} )) || eval "$(zoxide init zsh)"
alias j="zi"
```

## 常用命令

| 命令 | 功能 |
| --- | --- |
| `z foo` | 跳到匹配 `foo` 的最常用目录 |
| `z foo bar` | 多个关键词依次匹配路径，如 `z work cc` → `.../github_work/cc-runtime` |
| `z -` | 回到上一个目录 |
| `zi` / `j` | 用 fzf 交互选择目录，可加关键词预先过滤 |
| `z foo<空格><Tab>` | 补全时用 fzf 选择匹配的目录 |
| `zoxide query -l` | 列出索引里的全部目录（`-s` 显示分数） |
| `zoxide remove <路径>` | 从索引删除目录 |

## 数据位置

| 系统 | 路径 |
| --- | --- |
| macOS | `~/Library/Application Support/zoxide/db.zo` |
| Linux | `~/.local/share/zoxide/db.zo` |

可用 `_ZO_DATA_DIR` 改位置。数据库在家目录里，只重装 zoxide 不会丢索引；换新机器或新家目录时才需要重建。

## 批量建立索引

zoxide 只记录 `cd` 进去过的目录，新机器上索引是空的。[zoxide-index.sh](zoxide-index.sh) 把一个目录往下若干层的子目录一次性加入索引：

```sh
# /Users/zeke/workspace 往下两层，排除 old_work
./zoxide-index.sh -d 2 -e old_work /Users/zeke/workspace
```

写入前先用树形展示要加入的目录，确认后才写入：

```
起始目录：/Users/zeke/workspace（往下 2 层）
排除：.* *.app node_modules __pycache__ .venv venv dist build target vendor old_work

/Users/zeke/workspace/  (已有)
├── github_work/  (已有)
│   ├── context-kit/
│   └── telegram-dl/
├── rust_work/  (已有)
│   └── cache-setup/
└── zed-fork-builds/

共 102 个目录：新加入 14 个，已在索引 88 个（会加分）
已在索引的目录只展示新目录的上级，加 -a 查看全部

按 -e 排除了 1 个目录（连同其下内容）：
  old_work/  (old_work)
默认排除跳过了 7 个目录（隐藏目录、依赖和构建产物）

确认加入 zoxide 索引？[y/N]
```

- 默认只列新目录；已在索引的目录只在作为新目录的上级时出现，标「(已有)」并显示为灰色。加 `-a` 列出全部。
- 超过一屏时用 `less` 翻页，按 `q` 退出后回答确认；直接回车即取消。

| 参数 | 说明 |
| --- | --- |
| `<起始目录>` | 必填，起始目录本身总会加入 |
| `-d, --depth N` | 往下扫描的层数，默认 2 |
| `-e, --exclude 名称` | 排除该名称的目录及其下所有内容，可重复，支持通配符（如 `'old_*'`） |
| `-i, --include 名称` | 不排除该名称的目录，可重复；用来加回默认排除的目录 |
| `-n, --dry-run` | 只展示，不写入 |
| `-a, --all` | 展示时也列出已在索引的目录（灰色） |
| `-y, --yes` | 不询问直接写入；没有终端时（脚本里调用）必须加 |

- 默认排除隐藏目录（`.*`）、应用包（`*.app`）和 `node_modules`、`__pycache__`、`.venv`、`venv`、`dist`、`build`、`target`、`vendor`。
- 名称按目录名（最后一级）匹配，`-i` 优先于 `-e` 和默认排除，例如 `-d 1 -i .config ~` 会加入 `~/.config`。
- 重复运行只会给已有目录加分，不会产生重复条目。加入的目录初始分数为 1，日常 `cd` 过的目录会自然排在前面。
