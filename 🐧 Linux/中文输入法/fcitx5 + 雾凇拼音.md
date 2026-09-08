# fcitx5 + 中州韵 + 雾凇拼音

Fedora / KDE Wayland 上的简体中文输入。目标：

- 只留一套输入法：中州韵（Rime）
- 方案只留 **雾凇拼音全拼**（简体）
- 左 Shift 切中英
- 不要 `Ctrl+\``（和编辑器冲突）
- 不要全角、不要误切繁体
- 词库用雾凇，不用自带的明月拼音（2018，词太少）

本机实际路径（fcitx5，不是 ibus，也不是 `~/.config/fcitx5/rime`）：

```
~/.config/fcitx5/                 # fcitx5 自身
~/.local/share/fcitx5/rime/       # Rime 用户目录（词库、方案、补丁都在这）
/usr/share/rime-data/             # 系统自带明月拼音等，装雾凇后基本不用
```

---

## 1. 三层分别干什么

```
应用 ← 输入法框架 fcitx5 ← 引擎 Rime（中州韵）← 方案 雾凇拼音 rime_ice
```

| 层 | 管什么 | 配置 |
|---|---|---|
| fcitx5 | 启停、候选翻页、和程序对接 | `~/.config/fcitx5/config` `profile` |
| Rime | 方案列表、快捷键、标点、中英 | `~/.local/share/fcitx5/rime/default.yaml` + `default.custom.yaml` |
| 雾凇方案 | 词库、emoji、简繁、全半角开关 | `rime_ice.schema.yaml` + `rime_ice.custom.yaml` |

改 Rime / 雾凇必须 **重新部署** 才生效。改 fcitx5 用 `fcitx5-remote -r`。

**不要两层都抢 Shift。** 曾经踩过的坑：

- fcitx5 `AltTriggerKeys=Shift_L`：按 Shift 激活/关闭整个输入法
- 雾凇 `Shift_L: commit_code`：在 Rime 里切 `ascii_mode`（中/英）
- 两套一起开会「按两次才切过去」或状态错乱
- 把 Rime 的 `Shift_L` 设成 `noop` 更糟：雾凇注释里写了 **noop = 屏蔽**，中文状态下 Shift 被吞掉，fcitx 也收不到 → 完全切不了

当前选择：**只让雾凇切中英**，关掉 fcitx 的 Shift 临时切换，并默认激活输入法。

---

## 2. 安装

```bash
sudo dnf install fcitx5 fcitx5-rime fcitx5-configtool \
    fcitx5-gtk fcitx5-qt librime-lua
```

- `fcitx5-rime`：中州韵前端
- `librime-lua`：雾凇的日期/计算器/纠错等 Lua 功能依赖它

KDE 里把输入法选成 fcitx5，重新登录。环境变量至少要有（本机 Wayland 实际是 `@im=fcitx5`，两种都能认）：

```bash
export XMODIFIERS=@im=fcitx
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
```

检查：

```bash
echo $XMODIFIERS
fcitx5-remote          # 0 没跑 / 1 未激活 / 2 激活
fcitx5-remote -n       # 应是 rime
```

只留一个输入法：`fcitx5-configtool` → 输入法 → 组里只放 **中州韵**，键盘英文可以去掉。对应 `~/.config/fcitx5/profile`：

```ini
[Groups/0]
Name=默认
Default Layout=us
DefaultIM=rime

[Groups/0/Items/0]
Name=rime
Layout=

[GroupOrder]
0=默认
```

---

## 3. fcitx5 快捷键

文件：`~/.config/fcitx5/config`

关键项：

```ini
[Hotkey/TriggerKeys]
0=Control+space

[Hotkey/AltTriggerKeys]
# 空。不要再写 Shift_L

[Behavior]
ActiveByDefault=True
```

| 键 | 作用 |
|---|---|
| `Ctrl+空格` | 激活 / 关闭整个输入法（应急） |
| 左 Shift | **不归 fcitx 管**，归雾凇 |
| `Super+空格` | 切输入法组（只有一组，基本用不到） |

改完：

```bash
fcitx5-remote -r
```

---

## 4. 装雾凇拼音（词库）

官方：[iDvel/rime-ice](https://github.com/iDvel/rime-ice)

用户目录必须清空再拷（保留 `installation.yaml`）。**不要**和系统明月拼音混用。

```bash
RIME="$HOME/.local/share/fcitx5/rime"
git clone --depth 1 https://github.com/iDvel/rime-ice.git /tmp/rime-ice

# 备份
cp -a "$RIME/installation.yaml" /tmp/rime-installation.yaml 2>/dev/null || true

# 拷配置（不要 .git、小狼毫/鼠须管专用 yaml、双拼/九键）
rsync -a \
  --exclude '.git/' --exclude '.github/' --exclude '.gitignore' \
  --exclude 'squirrel.yaml' --exclude 'weasel.yaml' \
  --exclude 'others/' --exclude 'double_pinyin*' \
  --exclude 't9.schema.yaml' --exclude 'build/' \
  /tmp/rime-ice/ "$RIME/"

test -f /tmp/rime-installation.yaml && cp /tmp/rime-installation.yaml "$RIME/installation.yaml"
```

词库规模（数量级）：

- `cn_dicts/8105` 常用字
- `base` + `ext` + `tencent` 词库，编译后 `rime_ice.table.bin` 大约 50MB+
- 另有英文 `melt_eng`、emoji（opencc）

自带明月拼音大约 7 万条（单字居多，词才 2 万，版本还停在 2018），日常专名、网络词经常打不出来。

---

## 5. 精简方案和快捷键（补丁）

Rime 的正确改法是 `*.custom.yaml`，不要直接改上游 yaml，方便以后更新雾凇。

### `~/.local/share/fcitx5/rime/default.custom.yaml`

```yaml
# encoding: utf-8
# 只保留雾凇全拼；关掉方案菜单和容易误触的开关快捷键
patch:
  schema_list:
    - schema: rime_ice

  switcher/hotkeys: []

  # 左 Shift 切换中英（雾凇 ascii_mode）
  ascii_composer/switch_key/Shift_L: commit_code

  key_binder/bindings:
    - { when: composing, accept: Shift+Tab, send: Shift+Left }
    - { when: composing, accept: Tab, send: Shift+Right }
    - { when: composing, accept: Alt+Left, send: Shift+Left }
    - { when: composing, accept: Alt+Right, send: Shift+Right }
    - { when: has_menu, accept: minus, send: Page_Up }
    - { when: has_menu, accept: equal, send: Page_Down }
    - { when: composing, accept: KP_0, send: 0 }
    - { when: composing, accept: KP_1, send: 1 }
    - { when: composing, accept: KP_2, send: 2 }
    - { when: composing, accept: KP_3, send: 3 }
    - { when: composing, accept: KP_4, send: 4 }
    - { when: composing, accept: KP_5, send: 5 }
    - { when: composing, accept: KP_6, send: 6 }
    - { when: composing, accept: KP_7, send: 7 }
    - { when: composing, accept: KP_8, send: 8 }
    - { when: composing, accept: KP_9, send: 9 }
    - { when: composing, accept: KP_Decimal, send: period }
    - { when: composing, accept: KP_Multiply, send: asterisk }
    - { when: composing, accept: KP_Add, send: plus }
    - { when: composing, accept: KP_Subtract, send: minus }
    - { when: composing, accept: KP_Divide, send: slash }
    - { when: composing, accept: KP_Enter, send: Return }
```

这里等于做了三件事：

1. `schema_list` 只留 `rime_ice`，托盘里那些明月拼音 / 注音 / 仓颉 / 五笔 / 地球拼音全部消失
2. `switcher/hotkeys: []` 关掉方案选单：`Ctrl+\``、`Ctrl+Shift+\``、`F4`
3. 重写 `key_binder`，去掉默认的：
   - `Shift+空格` 全角半角（最容易误触）
   - `Ctrl+.` 中英标点
   - `Ctrl+Shift+1/3/4` 切方案 / 标点 / 繁简
4. `Shift_L: commit_code`：有未上屏编码就先上屏编码，再切到英文；再按一下回到中文

雾凇 `Shift_L` 可选值（打到一半时按 Shift）：

| 值 | 行为 |
|---|---|
| `commit_code` | 上屏原始拼音，切英文（当前） |
| `commit_text` | 上屏当前词，切英文 |
| `clear` | 丢掉未上屏内容，切英文 |
| `inline_ascii` | 临时英文，回车后回到中文 |
| `noop` | **屏蔽**，不要用，Shift 会没反应 |

### `~/.local/share/fcitx5/rime/rime_ice.custom.yaml`

```yaml
# encoding: utf-8
# 菜单只留中英和 emoji；固定半角、简体
patch:
  switches:
    - name: ascii_mode
      states: [ 中, Ａ ]
    - name: emoji
      states: [ 💀, 😄 ]
      reset: 1
    - name: ascii_punct
      reset: 0
    - name: traditionalization
      reset: 0
    - name: full_shape
      reset: 0
    - name: search_single_char
      reset: 0
```

`states` 去掉的开关不会出现在菜单里。`reset: 0` 把全角、繁体钉死。emoji 默认开。

---

## 6. 部署

改 yaml 之后必须部署，否则还在用 `build/` 里的旧编译结果。

图形界面：托盘 **中州韵 → 重新部署**。

命令行（本机没有 `rime_deployer` 包，用 librime API；部署腾讯词库可能 1～2 分钟）：

```bash
python3 << 'PY'
import ctypes
from ctypes import Structure, c_int, c_char_p, c_void_p, POINTER, CFUNCTYPE

class RimeTraits(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("shared_data_dir", c_char_p),
        ("user_data_dir", c_char_p),
        ("distribution_name", c_char_p),
        ("distribution_code_name", c_char_p),
        ("distribution_version", c_char_p),
        ("app_name", c_char_p),
        ("modules", c_char_p),
        ("min_log_level", c_int),
        ("log_dir", c_char_p),
        ("prebuilt_data_dir", c_char_p),
        ("staging_dir", c_char_p),
    ]

class RimeApi(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("setup", c_void_p),
        ("set_notification_handler", c_void_p),
        ("initialize", c_void_p),
        ("finalize", c_void_p),
        ("start_maintenance", c_void_p),
        ("is_maintenance_mode", c_void_p),
        ("join_maintenance_thread", c_void_p),
        ("deployer_initialize", c_void_p),
        ("prebuild", c_void_p),
        ("deploy", c_void_p),
    ]

lib = ctypes.CDLL("/usr/lib64/librime.so.1")
lib.rime_get_api.restype = POINTER(RimeApi)
api = lib.rime_get_api()
t = RimeTraits()
t.data_size = ctypes.sizeof(RimeTraits) - ctypes.sizeof(c_int)
t.shared_data_dir = b"/usr/share/rime-data"
t.user_data_dir = b"/home/zeke/.local/share/fcitx5/rime"
t.distribution_name = b"Rime"
t.distribution_code_name = b"fcitx-rime"
t.distribution_version = b"5.1.14"
t.app_name = b"rime.fcitx-rime-deployer"
t.min_log_level = 1
setup = CFUNCTYPE(None, POINTER(RimeTraits))(api.contents.setup)
dep_init = CFUNCTYPE(None, POINTER(RimeTraits))(api.contents.deployer_initialize)
start_m = CFUNCTYPE(c_int, c_int)(api.contents.start_maintenance)
join_m = CFUNCTYPE(None)(api.contents.join_maintenance_thread)
finalize = CFUNCTYPE(None)(api.contents.finalize)
setup(ctypes.byref(t))
dep_init(ctypes.byref(t))
print("maintenance", start_m(1))
join_m()
finalize()
print("done")
PY

dbus-send --print-reply --dest=org.fcitx.Fcitx5 \
  /controller org.fcitx.Fcitx.Controller1.ReloadAddonConfig string:rime
```

验收：

```bash
dbus-send --print-reply --dest=org.fcitx.Fcitx5 /rime \
  org.fcitx.Fcitx.Rime1.ListAllSchemas
# 只应有 rime_ice

rg 'Shift_L|schema_list|hotkeys:' ~/.local/share/fcitx5/rime/build/default.yaml
```

`build/default.yaml` 里应当是：

- `schema_list` 只有 `rime_ice`
- `hotkeys: []`
- `Shift_L: commit_code`

KDE 下 `CanRestart=false`，`dbus ... Restart` 不会真重启 fcitx5，所以部署后要 `ReloadAddonConfig` 或点「重新部署」。

---

## 7. 日常怎么用

先点进输入框（输入法要处于激活状态）。

| 操作 | 按键 |
|---|---|
| 中 ↔ 英 | 轻点 **左 Shift**（不要按住配别的键） |
| 整个输入法开关 | `Ctrl+空格` |
| 候选翻页 | `-` `=` |
| 音节间跳转 | `Tab` / `Shift+Tab` |
| 日期 | `rq` |
| 时间 | `sj` |
| 星期 | `xq` |
| 农历 | `nl` |
| 符号列表 | `vhelp` |
| 拆字反查生僻字 | `uU` + 部件拼音 |
| 计算器 | `cC` + 算式 |
| Unicode | `U` + 十六进制 |
| 金额大写 | `R` + 数字 |

打不出中文时：点一下输入框，或 `Ctrl+空格` 激活，再 Shift。

---

## 8. 更新词库

```bash
cd /tmp
rm -rf rime-ice
git clone --depth 1 https://github.com/iDvel/rime-ice.git
# 再跑第 4 节 rsync（不会覆盖 *.custom.yaml，gitignore 里排除了）
# 然后重新部署
```

`default.custom.yaml` / `rime_ice.custom.yaml` 是自己的补丁，更新上游后还在。

---

## 9. 排障

| 现象 | 原因 / 处理 |
|---|---|
| Shift 没反应 | 是不是把 `Shift_L` 设成了 `noop`；输入法是否激活（`fcitx5-remote` 应为 2） |
| Shift 要按两次 | fcitx `AltTriggerKeys` 和雾凇 `Shift_L` 抢键，只留一层 |
| 突然全角 | 默认 `Shift+空格`，已从 `key_binder` 去掉 |
| `Ctrl+\`` 弹出方案菜单 | `switcher/hotkeys: []` 后部署 |
| 托盘一堆方案 | `schema_list` 没补丁，或没部署 |
| 改了 yaml 没变化 | 没部署；看 `build/` 时间戳 |
| 候选没有 Lua 功能 | 没装 `librime-lua` |
| 词很少、专名打不出 | 还在用系统明月拼音，确认当前 schema 是 `rime_ice` |

```bash
fcitx5-remote                  # 状态
fcitx5-remote -n               # 当前 IM 名
dbus-send --print-reply --dest=org.fcitx.Fcitx5 /rime \
  org.fcitx.Fcitx.Rime1.GetCurrentSchema
ls -lh ~/.local/share/fcitx5/rime/build/rime_ice.table.bin
```

---

## 10. 本机软件版本（写笔记时）

- Fedora 44，KDE Wayland
- `fcitx5-rime-5.1.14`
- `librime-1.16.1` + `librime-lua`
- 雾凇拼音 schema version `2026-03-08`
