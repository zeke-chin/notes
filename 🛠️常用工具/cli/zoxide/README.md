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

# 先预览会加入哪些目录
./zoxide-index.sh -n -d 2 -e old_work /Users/zeke/workspace
```

| 参数 | 说明 |
| --- | --- |
| `<起始目录>` | 必填，起始目录本身总会加入 |
| `-d, --depth N` | 往下扫描的层数，默认 2 |
| `-e, --exclude 名称` | 排除该名称的目录及其下所有内容，可重复，支持通配符（如 `'old_*'`） |
| `-i, --include 名称` | 不排除该名称的目录，可重复；用来加回默认排除的目录 |
| `-n, --dry-run` | 只列出目录，不写入 |

- 默认排除隐藏目录（`.*`）和 `node_modules`、`__pycache__`、`.venv`、`venv`、`dist`、`build`、`target`、`vendor`。
- 名称按目录名（最后一级）匹配，`-i` 优先于 `-e` 和默认排除，例如 `-d 1 -i .config ~` 会加入 `~/.config`。
- 重复运行只会给已有目录加分，不会产生重复条目。加入的目录初始分数为 1，日常 `cd` 过的目录会自然排在前面。
