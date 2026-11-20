# Herdr

- 简介：面向 AI 编程助手的终端多路复用工具，支持分屏、会话管理和助手状态跟踪。
- 官网：https://herdr.dev/
- 安装：`curl -fsSL https://herdr.dev/install.sh | sh`

## 按键配置

配置文件：`~/.config/herdr/config.toml`，备份见 [config.toml](config/config.toml)。

```toml
onboarding = false

[keys]
split_vertical = "prefix+%"
split_horizontal = 'prefix+"'
```

`prefix` 默认是 `Ctrl+b`，先按前缀键，再按对应按键：

| 按键 | 功能 |
| --- | --- |
| `Ctrl+b` → `%` | 垂直分割（左右分屏） |
| `Ctrl+b` → `"` | 水平分割（上下分屏） |

## 脚本配置

让标签使用当前目录的最后一级名称，替代默认的 `1`、`2`、`3`。

- [cwd-tab-name.zsh](config/cwd-tab-name.zsh)：注册 zsh 钩子，首次显示提示符及切换目录时触发更新。
- [cwd-tab-name.py](config/cwd-tab-name.py)：获取当前标签并更新名称，记录手动改名状态。

### 加载方式

依赖 `zsh`、`python3`，以及 PATH 中可用的 `herdr`。在本目录下执行，将配置和脚本复制到本机：

```sh
mkdir -p ~/.config/herdr
cp config/config.toml config/cwd-tab-name.zsh config/cwd-tab-name.py ~/.config/herdr/
```

复制 `config.toml` 会覆盖已有的同名文件；如果已有其他设置，只合并上面的按键配置。

在 `~/.zshrc` 中添加一行：

```zsh
[[ ! -r "$HOME/.config/herdr/cwd-tab-name.zsh" ]] || source "$HOME/.config/herdr/cwd-tab-name.zsh"
```

已有终端执行 `source ~/.zshrc`，新开的 zsh 会自动加载。脚本仅在 `HERDR_ENV=1` 的 Herdr 终端中生效。

### 命名规则

- 首次加载时，将数字标签或与目录名匹配的标签纳入自动命名；已有的其他自定义名称保留。
- 执行 `cd` 后，标签随目录更新，例如 `/Users/zeke/workspace` 显示为 `workspace`。
- 检测到标签名与脚本上次设置的名称不同时，视为手动改名，停止该标签的自动更新；重新加载 shell 配置也不会覆盖。
- 同一标签有多个分屏时，以最后触发目录更新的分屏为准；各分屏共享手动改名状态。
- 状态保存在 `~/.cache/herdr/cwd-tab-names/`，按服务端 socket 身份和标签 ID 区分。

手动改成与当前名称完全相同的名字无法被检测；手动改名检测发生在下一次脚本触发时。

来源：Codex 会话 `01a1777a-8c7f-76b2-b022-bda9215c8461`。
