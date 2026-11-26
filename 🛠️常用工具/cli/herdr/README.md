# Herdr

- 简介：面向 AI 编程助手的终端多路复用工具，支持分屏、会话管理和助手状态跟踪。
- 官网：https://herdr.dev/
- 安装：`curl -fsSL https://herdr.dev/install.sh | sh`

## 组织方式

按官方推荐（[Concepts](https://herdr.dev/tui/docs/concepts/)）：

- **workspace**：一个项目（repo、任务或排查）一个，名称用目录名。侧边栏的 agent 状态按 workspace 汇总。
- **tab**：项目内的不同视图，agent 标签由 herdr-bar 按任务标题自动命名；其他标签手动起名，如 `server`、`logs`。

## 按键配置

配置文件：`~/.config/herdr/config.toml`，备份见 [config.toml](config/config.toml)。

```toml
onboarding = false

[keys]
split_vertical = "prefix+%"
split_horizontal = 'prefix+"'

[[keys.command]]
key = ["prefix+k", "ctrl+cmd+w"]
type = "plugin_action"
command = "herdr-bar.open"
description = "command bar"

[[keys.command]]
key = ["prefix+o", "ctrl+cmd+o"]
type = "plugin_action"
command = "herdr-bar.open-dirs"
description = "open a project"

[ui]
prompt_new_tab_name = false
```

`prefix` 默认是 `Ctrl+b`，先按前缀键，再按对应按键；不带 `prefix+` 的写法（如 `ctrl+cmd+w`）为单次直达快捷键，依赖终端的 Kitty 键盘协议（Ghostty 原生支持且默认未占用这两个组合键），数组写法可同时保留 `prefix+` 兜底：

| 按键 | 功能 |
| --- | --- |
| `Ctrl+b` → `%` | 垂直分割（左右分屏） |
| `Ctrl+b` → `"` | 水平分割（上下分屏） |
| `Ctrl+Cmd+w` / `Ctrl+b` → `k` | herdr-bar 搜索栏（见下文） |
| `Ctrl+Cmd+o` / `Ctrl+b` → `o` | 用 zi 选目录，打开项目 workspace 并选择启动的 agent（见下文） |
| `Ctrl+b` → `g` | 内置 Goto picker：按 workspace 分组列出所有 agent/终端，`/` 搜索，`b`/`w`/`i`/`d` 按状态筛选 |
| `Ctrl+b` → `w` | workspace 导航 |
| `Ctrl+b` → `Shift+n` / `Shift+w` | 新建 / 重命名 workspace |
| `Ctrl+b` → `c` | 新建 tab（`c` = create，类似 tmux window；配 `prompt_new_tab_name = false` 后不弹窗） |
| `Ctrl+b` → `Shift+t` | 重命名 tab |

## herdr-bar：搜索跳转与 tab 自动命名

插件 [jeffarese/herdr-bar](https://github.com/jeffarese/herdr-bar)（Rust，Herdr ≥ 0.9.0）。目前用自己的 fork [zeke-chin/herdr-bar](https://github.com/zeke-chin/herdr-bar) 的 `local` 分支（agy 命名、树形布局、`Ctrl+b o` 打开项目、侧边栏 logo），本地 clone 在 `~/workspace/github_work/herdr-bar`，用 `herdr plugin link` 安装。

```sh
herdr plugin install jeffarese/herdr-bar --yes
herdr server reload-config
```

- **搜索栏**（`Ctrl+Cmd+w` / `Ctrl+b` → `k`）：模糊搜索 agent、tab、workspace、命名过的 pane，匹配标题、cwd、分支、agent 名。打开即可输入；最近访问排前面，回车即 alt-tab；右侧实时预览；`ctrl+r` 重命名，`delete` 关闭 tab；`@` `%` `$` `!` 筛选 agent / pane / 普通 tab / 需要处理的。
- **自动命名**：只有一个 agent 的 tab，用 agent 的任务标题（Claude、Codex、Pi、OpenCode、Copilot 等）命名。只改默认数字名或自己写过的名字，手动改过的保留。无 agent 的 tab 不动。

配置：`herdr plugin config-dir herdr-bar` 下的 `config.json`，备份见 [config.json](config/herdr-bar/config.json)。

```json
{
  "auto_titles": true,
  "follow_new_sessions": true,
  "tab_status": false,
  "layout": "tree",
  "zoxide_commands": ["claude", "codex", "agy", "opencode", "pi", ""],
  "sidebar_logos": true
}
```

- `layout: "tree"`：按 workspace 分组显示（类似 `Ctrl+b g`），保留右侧预览。
- `zoxide_commands`：`Ctrl+b o` 新建 workspace 时可选的命令，见下文「打开新项目」。
- `sidebar_logos`：给 herdr 侧边栏上报 agent logo，见下文「agent logo」。

- `follow_new_sessions`：`/clear` 或重启 agent 后，tab 名跟随新会话的标题。
- `tab_status`：在 tab 名前加状态符号（`◉` 需要你、`◐` 运行中、`●` 完成、`✓` 空闲）。
- 后台 watcher 每 2 秒检查一次；启停：`herdr plugin action invoke herdr-bar.start-titles` / `stop-titles`。
- 若启用了其他改名插件，herdr-bar 会自动停止改名。

### 打开新项目：`Ctrl+Cmd+o` / `Ctrl+b o`（替代 zi → 启动 claude）

action `herdr-bar.open-dirs`：弹窗里运行 zoxide 自带的选择界面（`zoxide query --interactive`，即 `zi`），匹配、排序、预览都和终端里的 `zi` 一致。

1. 选目录，回车。
2. 已有 pane 在该目录的 workspace → 直接跳过去，不再询问。
3. 没有 → 第二个 fzf 列表选要运行的命令（`zoxide_commands` 的顺序，带 agent logo 和品牌色；默认第一项 claude，`shell` 只开 shell，`Esc` 取消、什么都不建），然后新建以目录名命名的 workspace 并运行。

- 命令通过 `$SHELL -lic '<命令>; exec $SHELL -l'` 由 Herdr 直接启动（`layout.apply`），不是往 shell 里打字：p10k instant prompt 期间打进去的字会被原样回显而不执行。退出 agent 后留下一个 shell。
- `zoxide_commands` 只有一项时不弹菜单；旧写法 `"zoxide_command": "claude"` 也可用。
- 命令行等价：`herdr-bar --open-dir <目录>`（直接运行第一项，不询问）。
- `Ctrl+b k` 搜索栏不含目录，只用来在已打开的项目间跳转。

### agent logo（依赖图标字体）

#### 1. 字体：Herdr Agent Icons Max

社区插件 [herdr-radar](https://github.com/hhdebb/herdr-radar) 做的图标字体（18 KB，MIT，logo 版权归各厂商），把 24 个 agent logo 放在 Unicode 私有区 `U+E1A0`–`U+E1B7`，按顺序：claude、codex、opencode、omp、cline、mastracode、kimi、kilo、maki、pi、hermes、cursor、copilot、deepseek、gemini、gpt、qwen、grok、agy、kiro、amp、devin、qodercli、glm（如 claude `U+E1A0`、codex `U+E1A1`、agy `U+E1B2`）。Herdr 本体不用它。

```sh
curl -fsSL -o ~/Library/Fonts/HerdrAgentIconsMax-Regular.ttf \
  https://raw.githubusercontent.com/hhdebb/herdr-radar/main/dist/HerdrAgentIconsMax-Regular.ttf
```

Ghostty（`~/.config/ghostty/config`）把这段编码映射到该字体，主字体 `MesloLGS NF` 不变：

```
font-codepoint-map = U+E1A0-U+E1B7=Herdr Agent Icons Max
```

装完要 `Cmd+Q` 彻底重启 Ghostty（只开新窗口不会重新扫描字体；没生效时 logo 会显示成 STIXNonUnicode 里的希腊字母 λ μ ϱ）。herdr 会话不受影响，重开后 `herdr` 连回。验证：`printf '\ue1a0 \ue1a1 \ue1a2 \ue1a9 \ue1b2\n'`。

字体只需装在**画终端的那台机器**（Mac）。远程连容器时容器里的 herdr-bar 检测不到字体，需在容器的 herdr-bar 配置里加 `"agent_icons": "font"`。

装好后 herdr-bar 自动使用：`Ctrl+b k` 每行前的 logo、`Ctrl+b o` 命令菜单的 logo。没装字体时退回文字和彩色 `●`。

#### 2. herdr 侧边栏显示 logo

herdr 侧边栏没有图标选项，插件也不能加行，但可以给 pane 上报自定义值（`$name` 显示项）。herdr-bar 配置 `"sidebar_logos": true` 后，后台 watcher 给每个 agent pane 上报 `logo`（变化时才报，agent 退出时清除）。再在 `config.toml` 里把 `$logo` 放进侧边栏布局，用 `rules` 按值上色（logo 和名字同色，放在第二行名字前，第一行留给 workspace/tab）：

```toml
[ui.sidebar.agents]
rows = [
  ["state_icon", "machine", "workspace", "tab"],
  [{ token = "$logo", rules = [
  { equals = "\uE1A0", fg = "#D97757" },  # claude
  { equals = "\uE1A1", fg = "#10A37F" },  # codex
  { equals = "\uE1A2", fg = "#38BDF8" },  # opencode
  { equals = "\uE1A6", fg = "#9B8AFB" },  # kimi
  { equals = "\uE1AB", fg = "#A78BFA" },  # cursor
  { equals = "\uE1AE", fg = "#4285F4" },  # gemini
  { equals = "\uE1B2", fg = "#7298F3" },  # agy
  ] }, { token = "agent", rules = [
  { equals = "claude", fg = "#D97757" },
  { equals = "codex", fg = "#10A37F" },
  { equals = "opencode", fg = "#38BDF8" },
  { equals = "kimi", fg = "#9B8AFB" },
  { equals = "cursor", fg = "#A78BFA" },
  { equals = "gemini", fg = "#4285F4" },
  { equals = "agy", fg = "#7298F3" },
  ] }],
]
```

颜色与 herdr-bar 主题一致；pi 没有品牌色，用默认色。查看上报值：`herdr api snapshot | jq '.result.snapshot.agents[] | {pane_id, agent, tokens}'`（值在 `agents[].tokens`，不在 `panes[]`）。

### 旧方案：按目录命名 tab（已停用）

2026-11-24 前使用 [zeke-chin/herdr-auto-tab-name](https://github.com/zeke-chin/herdr-auto-tab-name)（[dev-shimada/herdr-auto-tab-name](https://github.com/dev-shimada/herdr-auto-tab-name) 的 fork，新增 `sync-current` 动作并改了 shell 钩子），让 tab 用当前目录名。改为一个项目一个 workspace 后，同一 workspace 内的 tab 目录相同，按目录命名无法区分，已卸载插件并从 `~/.zshrc` 移除钩子。本地 clone 保留在 `~/workspace/github_work/herdr-auto-tab-name`。

恢复：

```sh
herdr plugin install zeke-chin/herdr-auto-tab-name --yes
# ~/.zshrc
[[ ! -r "$HOME/workspace/github_work/herdr-auto-tab-name/shell/hook.zsh" ]] || source "$HOME/workspace/github_work/herdr-auto-tab-name/shell/hook.zsh"
```

同时把 herdr-bar 的 `auto_titles` 设为 `false`。

## `herdr --remote`

远程模式下服务端、分屏和插件都在远端机器上运行，本地插件和配置不会同步过去，需要在远端机器上单独安装 herdr-bar 并写配置（容器里另加 `"agent_icons": "font"`，字体装在本地 Mac 上即可）。

本地 `config.toml` 里的自定义命令快捷键（`[[keys.command]]`，如 `prefix+k` / `ctrl+cmd+w`）在远程模式下不会发到远端，要用远端的按键配置：`herdr --remote <host> --remote-keybindings server`（只能用命令行参数指定），改自定义快捷键时需同步改远端 `~/.config/herdr/config.toml` 并 `herdr server reload-config`。内置快捷键（如 `prefix+g`）不受影响。

来源：Codex 会话 `01a1777a-8c7f-76b2-b022-bda9215c8461`（最早的 Python 脚本方案）。
