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

[[keys.command]]
key = "prefix+shift+a"
type = "plugin_action"
command = "dev-shimada.auto-tab-name.sync-current"
description = "rename tab to its directory"
```

`prefix` 默认是 `Ctrl+b`，先按前缀键，再按对应按键：

| 按键 | 功能 |
| --- | --- |
| `Ctrl+b` → `%` | 垂直分割（左右分屏） |
| `Ctrl+b` → `"` | 水平分割（上下分屏） |
| `Ctrl+b` → `A` | 当前标签强制改回目录名（见下文） |

## 标签按目录命名

让标签使用当前目录的最后一级名称，替代默认的 `1`、`2`、`3`。使用社区插件 [herdr-auto-tab-name](https://github.com/dev-shimada/herdr-auto-tab-name) 的 fork [zeke-chin/herdr-auto-tab-name](https://github.com/zeke-chin/herdr-auto-tab-name)（依赖 Herdr ≥ 0.7.0、Node 22.18+）。

fork 新增了 `sync-current` 动作（强制改回目录名），并改了插件自带的 shell 钩子：原版每次 `cd` 都直接改名，会覆盖手动设置的名称；fork 改为调用插件的 sync 动作，遵循同一套手动改名规则，并跳过子 shell 中的 `cd`。上游仓库不接受外部 PR，改动已合并到 fork 的 `main`。同步上游：在 clone 中 `git pull upstream main && git push`，再执行 `herdr plugin update`。

```sh
# 插件
herdr plugin install zeke-chin/herdr-auto-tab-name

# 钩子从本地 clone 加载（插件安装目录带版本号，路径不固定）
gh repo clone zeke-chin/herdr-auto-tab-name ~/workspace/github_work/herdr-auto-tab-name
```

插件监听 Herdr 事件（标签/分屏创建、聚焦、切换工作区等），读取分屏的 `foreground_cwd` 后改名。shell 里 `cd` 不产生 Herdr 事件，所以需要 shell 钩子。在 `~/.zshrc` 中添加：

```zsh
[[ ! -r "$HOME/workspace/github_work/herdr-auto-tab-name/shell/hook.zsh" ]] || source "$HOME/workspace/github_work/herdr-auto-tab-name/shell/hook.zsh"
```

### 命名规则（插件行为）

- 只改名称为纯数字或插件上次设置的标签；手动改过的名称保留。设置 `overwrite_manual: true` 可强制全部改名。
- 家目录显示为 `~`。
- 一个标签有多个分屏时，取聚焦的分屏，否则取第一个分屏的目录。
- 配置：`herdr plugin config-dir dev-shimada.auto-tab-name` 下的 `config.json`（`overwrite_manual`、`max_length`）。
- 状态：`~/.local/state/herdr/plugins/dev-shimada.auto-tab-name/labels.json`。
- 手动同步：`herdr plugin action invoke dev-shimada.auto-tab-name.sync`（不动手动改过的名称）；运行日志：`herdr plugin log list`。
- 强制改回目录名：`Ctrl+b` → `A`（`prefix+shift+a`），或 `herdr plugin action invoke dev-shimada.auto-tab-name.sync-current`。作用于**当前聚焦的标签**，覆盖手动名称，之后该标签恢复自动命名。这是 fork 新增的动作。

### `herdr --remote`

远程模式下服务端、分屏和插件都在远端机器上运行，本地插件和配置不会同步过去。需要在远端机器上安装插件，clone fork 并在远端的 `~/.zshrc` 加载钩子（远端也要有 Node 22.18+）。

来源：Codex 会话 `01a1777a-8c7f-76b2-b022-bda9215c8461`（原 Python 脚本方案，已替换为插件）。
