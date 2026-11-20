# fzf

- 简介：通用的命令行模糊查找器，用来搜历史命令、文件和目录，也是 [zoxide](../zoxide/README.md) 的 `zi` 的交互界面。
- 官网：https://github.com/junegunn/fzf
- 安装：`brew install fzf`（Ubuntu：`apt install fzf`）

## 加载方式

在 `~/.zshrc` 中添加（需要 fzf 0.48 及以上，旧版本用安装包里的 `key-bindings.zsh`）：

```zsh
(( ! ${+commands[fzf]} )) || source <(fzf --zsh)
```

## 快捷键

| 按键 | 功能 |
| --- | --- |
| `Ctrl-R` | 模糊搜索历史命令，回车放到命令行 |
| `Ctrl-T` | 搜索当前目录下的文件，把路径插入命令行 |
| `Alt-C` | 搜索子目录并 `cd` 进去（macOS 终端要把 Option 设为 Meta 键） |
| `**<Tab>` | 补全时用 fzf 选择，如 `vim **<Tab>`、`cd **<Tab>`、`kill -9 **<Tab>` |

在 fzf 界面里：`Ctrl-J` / `Ctrl-K` 上下移动，`Tab` 多选，`Esc` 退出。

## 搜索语法

| 输入 | 含义 |
| --- | --- |
| `foo bar` | 同时包含 `foo` 和 `bar`（模糊匹配） |
| `'foo` | 精确包含 `foo` |
| `^foo` / `foo$` | 以 `foo` 开头 / 结尾 |
| `!foo` | 不包含 `foo` |
| `foo \| bar` | 包含 `foo` 或 `bar` |
