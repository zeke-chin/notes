# Karabiner-Elements

- 简介：macOS 底层键盘改键与快捷键自动化工具，支持按当前应用条件触发映射和切换输入法。
- 仓库：https://github.com/pqrs-org/Karabiner-Elements
- 安装：`brew install --cask karabiner-elements`
- 配置文件：`~/.config/karabiner/karabiner.json`

## 备份文件

| 文件 | 本机位置 | 说明 |
| --- | --- | --- |
| [karabiner.json](config/karabiner.json) | `~/.config/karabiner/karabiner.json` | 键位映射与复杂规则配置 |

## 简单改键（Simple Modifications）

对所有键盘生效：

| 原按键 | 映射为 |
| --- | --- |
| `fn`（`keyboard_fn`） | `left_control` |
| `right_option` | `fn`（`keyboard_fn`） |

## 复杂规则（Complex Modifications）

### 1. `Ctrl+Shift+L`：锁屏并熄屏

- 发送 `Ctrl+Cmd+Q` 锁屏，按键抬起后执行 `/bin/sleep 1; /usr/bin/pmset displaysleepnow` 关闭显示器。

### 2. Ghostty：`Ctrl+b` 自动切换为 ABC 英文输入法

- 仅在前台应用为 Ghostty（`com.mitchellh.ghostty`）时生效，用于配合 Herdr / tmux 前缀键 `Ctrl+b`，避免中文输入法下后续命令无法触发（远程会话同样有效）。
- 同时兼容上面的 `fn → left_control` 映射。
- 触发时先调用 `select_input_source` 切到 `^com\.apple\.keylayout\.ABC$`，再把 `Ctrl+b` 原样发给 Ghostty：

```json
{
    "description": "Ghostty: Ctrl+b 切换为 ABC 英文输入法",
    "manipulators": [
        {
            "conditions": [
                {
                    "bundle_identifiers": ["^com\\.mitchellh\\.ghostty$"],
                    "type": "frontmost_application_if"
                }
            ],
            "from": {
                "key_code": "b",
                "modifiers": { "mandatory": ["control"] }
            },
            "to": [
                {
                    "select_input_source": {
                        "input_source_id": "^com\\.apple\\.keylayout\\.ABC$"
                    }
                },
                {
                    "key_code": "b",
                    "modifiers": ["left_control"]
                }
            ],
            "type": "basic"
        }
    ]
}
```

## 恢复方式

在本目录下执行：

```sh
mkdir -p ~/.config/karabiner
cp config/karabiner.json ~/.config/karabiner/
```

会覆盖已有配置，Karabiner-Elements 会自动检测变更并热重载生效。
