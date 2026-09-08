# zoxide

比 `cd` 聪明的跳转：只记**进去过的目录**（frecency），不是按名字搜磁盘。
和 autojump 同类，但 **没有** `j abc<Tab>` 那种数据库补全。

初始化（zsh，放 `~/.zshrc` 末尾）：

```zsh
eval "$(zoxide init zsh)"
```

需要 [fzf](https://github.com/junegunn/fzf)。

## 1. 用法

| 命令 | 作用 |
|---|---|
| `z alg` | 跳到库里最匹配 `alg` 的目录 |
| `z wm alg` | 关键字 AND，路径要同时包含 |
| `zi` | **交互**：fzf 里从库中选一个再 cd |
| `zi alg` | 先按 `alg` 过滤，再交互选 |

`zi` 里：打字过滤，`Tab` / `Shift-Tab` 上下移动，`Enter` 进入，`Esc` 取消。

Tab 和 autojump 不一样：

- `z alg<Tab>` → 当 `cd` 补全，补**当前目录的子目录**
- `z alg <空格><Tab>` → 和 `zi alg` 一样，进 fzf

多个结果要挑，只能 `zi`，没有 Tab 列表。

## 2. 为啥库是空的

`z` / `zi` 不扫磁盘。没 `cd` 进去过的路径不会出现。
手动 `zoxide add` 只是跳过等待、先把常用目录写进库。

```bash
zoxide query -l          # 看库
zoxide query -l alg      # 看 alg 能匹配到什么
zoxide add ~/path        # 手动加一条
```

## 3. 把当前目录下的子目录加入候选（不递归）

zsh（`(/)` 只匹配目录）：

```zsh
# 当前目录 + 一级子目录
zoxide add . ./*(/)
```

没有子目录时，zsh 可能因 nomatch 报错，用 `N`：

```zsh
zoxide add . ./*(/N)
```

写成函数，随用随加：

```zsh
# ~/.zshrc
za() {
  zoxide add . ./*(/N)
}
```

进到 `~/workspace/wm_work` 后执行 `za`，再 `zi alg` 就能选 `alg-cli-server`、`alg-nexus` 等。

递归（慎用，库会很脏）：

```zsh
zoxide add . ./**/*(/N)
```

bash 没有 `(/)`，可以用：

```bash
zoxide add .
find . -mindepth 1 -maxdepth 1 -type d -print0 | xargs -0 zoxide add
```

## 4. 常见坑

`$FZF_DEFAULT_OPTS: unknown option: --no-filter`

当前 fzf 不认识 `--no-filter`。清掉再试：

```bash
unset FZF_DEFAULT_OPTS _ZO_FZF_OPTS
zi
```

自定义 fzf 用 `_ZO_FZF_OPTS`，不要写不存在的 flag：

```zsh
export _ZO_FZF_OPTS="--height 45% --layout reverse"
eval "$(zoxide init zsh)"
```
