# Zed

- 简介：Rust 编写的高性能代码编辑器，内置 Agent 面板和 Git 面板。当前使用自己维护的 fork 版本，`settings.json` 里 `fork.*` 开头的设置只有 fork 版本能识别。
- 官网：https://zed.dev/
- 配置目录：`~/.config/zed/`

## 备份文件

| 文件 | 本机位置 | 说明 |
| --- | --- | --- |
| [settings.json](config/settings.json) | `~/.config/zed/settings.json` | 主设置；`fork.windsurf.api_key` 已替换为占位符 |
| [keymap.json](config/keymap.json) | `~/.config/zed/keymap.json` | 自定义快捷键 |
| [jetbrains-darcula.json](config/themes/jetbrains-darcula.json) | `~/.config/zed/themes/jetbrains-darcula.json` | 深色主题 JetBrains Darcula |

## 主要设置

- 主题跟随系统：浅色 `One Light`，深色 `JetBrains Darcula`；图标主题 `Symbols Icon Theme`。
- 字体：编辑器 JetBrains Mono 14，中文回退 PingFang SC；UI 字号 16；终端 MesloLGS NF。
- 布局：项目面板和 Git 面板在左侧，Agent 面板在右侧；隐藏协作面板按钮。
- 编辑器：彩色括号、行内 git blame、diff 左右分栏。
- `file_scan_exclusions` 在默认规则上追加 `__pycache__`、`.venv`、`node_modules` 等目录。
- Python 使用 `ty` + `ruff` 语言服务。
- Agent 默认模型 deepseek-flash，附中文 commit message 规范。

## 快捷键

| 按键 | 功能 |
| --- | --- |
| `cmd-b` | 切换项目面板 |
| `cmd-shift-b` | 切换项目侧栏（覆盖默认的大纲面板） |
| `cmd-l` | 打开/隐藏 Agent 面板（编辑器内覆盖默认的选中整行） |
| `cmd-g` | 打开/聚焦 Git 面板（覆盖默认的查找下一个） |

## 扩展

csv、dockerfile、env、git-firefly、html、java、log、symbols、toml

在命令面板执行 `zed: extensions` 搜索安装。

## 恢复方式

在本目录下执行：

```sh
mkdir -p ~/.config/zed/themes
cp config/settings.json config/keymap.json ~/.config/zed/
cp config/themes/jetbrains-darcula.json ~/.config/zed/themes/
```

会覆盖已有的同名文件。恢复后需要把 `settings.json` 里的 `<YOUR_WINDSURF_API_KEY>` 换成真实的 token。
