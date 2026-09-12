# 企业微信 Wine

在 Fedora KDE Wayland 上用 Wine 跑企业微信（WXWork），以及**怎么把这套环境搬到另一台机器**。

本机实测环境：Fedora 44 / KDE Plasma / Wayland，`wine-11.0 (Staging)`，企业微信 `5.0.10.6015`（PE32 i386，跑在 win64 前缀里）。

前缀不是默认的 `~/.wine`，是独立的 **`~/.wine-wecom`**。所有命令都必须带 `WINEPREFIX`。

---

## 一、迁移清单

这套东西散在 5 个地方，拷贝时别漏：

| 路径 | 作用 | 能否省 |
|---|---|---|
| `~/.wine-wecom/` | Wine 前缀本体，企微装在里面 | 迁移必须 |
| `~/.local/bin/wecom-wine` | 启动脚本，所有环境变量在这 | 必须 |
| `~/.local/lib/wecom-wine/` | 标题栏辅助程序（`manage-titlebar.py` + `x11.py`） | 不修窗口重叠就得要 |
| `~/.local/share/applications/wine/` | 桌面图标 + 开始菜单项 | 可重建 |
| `~/.zshrc` 里两行 alias | `wxwork_start` / `wxwork_stop` | 可重建 |
| `~/.local/state/wecom-wine/` | 字体、注册表片段、日志、备份 | 字体要用 |

> `~/.local/state/wecom-wine/` 里那个 `NotoSansCJKsc-Regular.otf`（16MB）和 `chinese-fonts.reg` 要一起带走，重装字体时用。

---

## 二、装依赖

Fedora 装 wine 会连带拖一堆子包，直接装主包即可：

```bash
sudo dnf install wine winetricks
```

装完确认版本：

```bash
wine --version      # wine-11.0 (Staging)
```

要紧的是 `wine-core`、`wine-common`、`wine-pulseaudio`（声音）、`wine-dxvk`（图形）。这些是 wine 的依赖，`dnf` 会自动装。

---

## 三、建前缀 + 装企微

```bash
export WINEPREFIX="$HOME/.wine-wecom"
wineboot -u          # 初始化前缀，第一次会弹 mono/gecko 安装，等它跑完
```

然后装企微（安装包在 `~/Downloads/WeCom_5.0.10.6015.exe`）：

```bash
WINEPREFIX="$HOME/.wine-wecom" wine ~/Downloads/WeCom_5.0.10.6015.exe
```

一路下一步，装完路径是：

```
~/.wine-wecom/drive_c/Program Files (x86)/WXWork/WXWork.exe
```

装完**先别急着启动**，下面三节是必须改的，不改就是启动不了或者白屏。

---

## 四、关键配置（三个必改项）

这三个是本机踩出来的坑，缺一个企微就是起不来。

### 4.1 Windows 版本必须是 win10

**症状**：进程全起来了，但主窗口不显示，或者显示出来了点不动。

Wine 默认给的是 win8.1，企微 5.x 不认。必须设成 win10：

```bash
WINEPREFIX="$HOME/.wine-wecom" wine reg add \
  'HKCU\Software\Wine' /v Version /t REG_SZ /d win10 /f
```

企微内部还有个 CEF 浏览器子进程 `WXWorkWeb.exe`，它**反过来要保持 win8.1**，别一起改了：

```bash
WINEPREFIX="$HOME/.wine-wecom" wine reg add \
  'HKCU\Software\Wine\AppDefaults\WXWorkWeb.exe' /v Version /t REG_SZ /d win8.1 /f
```

对应注册表长这样：

```ini
[HKEY_CURRENT_USER\Software\Wine]
"Version"="win10"

[HKEY_CURRENT_USER\Software\Wine\AppDefaults\WXWork.exe]
"Version"="win10"

[HKEY_CURRENT_USER\Software\Wine\AppDefaults\WXWorkWeb.exe]
"Version"="win8.1"
```

### 4.2 图形驱动强制走 X11，不要 Wayland

**症状**：窗口不显示、渲染花屏，或者点不了。

Wine 11 检测到 `WAYLAND_DISPLAY` 就会用原生 Wayland 驱动（waylanddrv），企微这套 CEF 在它上面不好使。两个动作，**都要做**：

**① 注册表里指定 x11：**

```bash
WINEPREFIX="$HOME/.wine-wecom" wine reg add \
  'HKCU\Software\Wine\Drivers' /v Graphics /t REG_SZ /d x11 /f
```

**② 启动脚本里清掉 `WAYLAND_DISPLAY`**（见第五节，脚本里有 `unset WAYLAND_DISPLAY`）。

只在注册表设了但环境变量还在，Wine 仍可能挑 Wayland，所以两个一起做才稳。

顺带一个好处：走 XWayland 后，`xdotool` / `xwininfo` 这些 X 侧工具能查到企微窗口了。

### 4.3 语言必须是 zh_CN.UTF-8

**症状**：企微界面是英文的，或者中文显示成方块/乱码。

Wine 会读 `LC_ALL` 来定 Windows 的 locale。本机 shell 默认是 `C.UTF-8`，Wine 据此初始化为 en-US，企微就跟着变英文。

Fedora 上确认有 `zh_CN.UTF-8`：

```bash
locale -a | grep zh_CN
# zh_CN / zh_CN.utf8 / zh_CN.gb18030 / ...
```

有就行，没有的话：

```bash
sudo localedef -i zh_CN -f UTF-8 zh_CN.UTF-8
```

然后启动脚本里固定三个变量（注意是**只在企微这个脚本里**设，别污染整个 shell）：

```sh
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
export LANGUAGE=zh_CN:zh
```

---

## 五、中文字体

Wine 自带的替换字体没有中文，不配的话企微里中文全是方块。

做法是把 Noto Sans CJK SC 塞进前缀，再让「微软雅黑 / 宋体 / 黑体」这些字体名指向它。

**① 拷贝字体进前缀：**

```bash
cp ~/.local/state/wecom-wine/NotoSansCJKsc-Regular.otf \
   ~/.wine-wecom/drive_c/windows/Fonts/
```

> OTF 可以从 https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/SimplifiedChinese 下。用**静态** OTF，别用可变字体（VF）。

**② 导入注册表片段** `chinese-fonts.reg`：

```bash
WINEPREFIX="$HOME/.wine-wecom" wine regedit ~/.local/state/wecom-wine/chinese-fonts.reg
```

它干了三件事：

1. 在 `HKLM\...\CurrentVersion\Fonts` 注册 `Noto Sans CJK SC`
2. 在 `HKCU\Software\Wine\Fonts\Replacements` 和 `HKLM\...\FontSubstitutes` 里把微软雅黑、微软雅黑 UI、SimSun、NSimSun、SimHei、DengXian、宋体、新宋体、黑体、等线全部映射到 `Noto Sans CJK SC`
3. 打开字体平滑（`FontSmoothing=2`，ClearType）

**③ 注意**：那个 `.reg` 是 **UTF-16LE** 编码的（Windows 注册表编辑器导出的格式），里面既有英文名也有中文名两套键。别用文本编辑器存成 UTF-8 再导入，中文键会坏掉。

不想手动导的话，`winecfg` 图形界面里也能设字体替换，但批量映射还是导 reg 快。

---

## 六、启动脚本

主入口是 `~/.local/bin/wecom-wine`，所有环境变量都在这，桌面图标和 alias 都调它：

```sh
#!/bin/sh
# Enterprise WeChat on Fedora KDE: use XWayland in the dedicated prefix.
export WINEPREFIX=/home/zeke/.wine-wecom
# Override inherited C.UTF-8 so Wine and WeCom select Simplified Chinese.
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
export LANGUAGE=zh_CN:zh
unset WAYLAND_DISPLAY
# Long-lived terminals can retain an obsolete KDE Xauthority path.
if [ ! -r "${XAUTHORITY:-/nonexistent}" ]; then
    wecom_xauth=$(/usr/bin/python3 - <<'PYAUTH'
import os
from pathlib import Path
for proc in Path('/proc').glob('[0-9]*'):
    try:
        if proc.stat().st_uid != os.getuid() or (proc/'comm').read_text().strip() != 'plasmashell':
            continue
        env = dict(x.split(b'=', 1) for x in (proc/'environ').read_bytes().split(b'\0') if b'=' in x)
        auth = os.fsdecode(env.get(b'XAUTHORITY', b''))
        if auth and env.get(b'DISPLAY', b'').decode() == os.environ.get('DISPLAY') and Path(auth).is_file():
            print(auth)
            break
    except (OSError, ValueError):
        pass
PYAUTH
)
    if [ -n "$wecom_xauth" ]; then
        export XAUTHORITY="$wecom_xauth"
    fi
    unset wecom_xauth
fi
export WINEDEBUG="${WINEDEBUG:--all,err+all}"
state_dir=/home/zeke/.local/state/wecom-wine
mkdir -p "$state_dir"
chmod 700 "$state_dir"
# Repair WeCom's unmanaged title-bar popup (stacking and virtual desktops).
if [ "${WECOM_WINDOW_FIX:-1}" != "0" ]; then
    /usr/bin/python3 /home/zeke/.local/lib/wecom-wine/manage-titlebar.py \
        </dev/null >> "$state_dir/titlebar-manager.log" 2>&1 &
fi
cd "$WINEPREFIX/drive_c/Program Files (x86)/WXWork" || exit 1
exec /usr/bin/wine WXWork.exe "$@" >> "$state_dir/launcher.log" 2>&1
```

脚本里三块值得单独说：

| 段落 | 为什么 |
|---|---|
| `WINEPREFIX` / `LANG` / `unset WAYLAND_DISPLAY` | 第 4 节三个必改项，全在这 |
| `XAUTHORITY` 探测 | 长期开着的终端里 `XAUTHORITY` 指向的路径可能已经失效（KDE 重启过），X 连不上就起不来。这段从 `plasmashell` 进程的 `/proc/<pid>/environ` 里读当前有效的路径 |
| `manage-titlebar.py` 后台拉起 | 修窗口重叠，见第七节 |

装的时候记得路径里的 `/home/zeke/` 换成新机器上的家目录，然后 `chmod +x`。

---

## 七、桌面图标

三个地方指向同一个脚本。新机器上改掉里面的绝对路径即可。

`~/.local/share/applications/wine/企业微信.desktop`：

```ini
[Desktop Entry]
Name=企业微信
Exec=/home/zeke/.local/bin/wecom-wine
Type=Application
StartupNotify=true
Path=/home/zeke/.wine-wecom/drive_c/Program Files (x86)/WXWork
Icon=AF03_WXWork.0
StartupWMClass=wxwork.exe
```

另外两个（`~/Desktop/企业微信.desktop`、`~/.local/share/applications/wine/Programs/企业微信/企业微信.desktop`）内容一样。

`StartupWMClass=wxwork.exe` 别漏，漏了任务栏里会多出一个无名图标。

**注意 `Path=` 和 `Exec=` 里的空格**：这两个字段有空格但不加引号是合法的（desktop 文件的 `Path` 是单值，`Exec` 会按规则切分）。直接从这拷就行。

---

## 八、zsh alias

`~/.zshrc`：

```zsh
# 企业微信 (WXWork) — 自定义 Wine 前缀 ~/.wine-wecom
alias wxwork_start='"$HOME/.local/bin/wecom-wine" &!'
alias wxwork_stop='WINEPREFIX="$HOME/.wine-wecom" wineserver -k'
```

- `wxwork_start` 用 `&!` 把进程丢到后台并脱离，关掉终端不会带着企微一起死
- `wxwork_stop` 是 `wineserver -k`，杀掉该前缀下的所有 Windows 进程

> 旧文档里的 `go_wwork` alias 已经改名成 `wxwork_start` 了。

---

## 九、标题栏窗口重叠修复

**问题**：企微主窗口上方有一条 986×28 的独立按钮条，切换虚拟桌面或者叠窗口时它会乱跑／被盖住。

**原因**：这条按钮条被企微自己创建成了 `override_redirect=1` 的窗口——绕过窗口管理器，KWin 管不到它，所以它不遵守桌面归属和遮挡顺序。它的 `WM_TRANSIENT_FOR` 其实指对了主窗口，纯粹是这个标志的问题。

**做法**：`~/.local/lib/wecom-wine/manage-titlebar.py` 常驻，监听 X11 窗口事件，只匹配满足下面**全部**条件的窗口才动手：

- `WM_CLASS` 含 `wxwork.exe`
- `override_redirect=1` 且已显示
- 无标题（`_NET_WM_NAME` 为空）
- 高 15–64 像素
- 父窗口是同进程、同名「企业微信」、同 x/同 y/同宽的主窗口

命中后：先 unmap，把 `override_redirect` 清 0，设 `_MOTIF_WM_HINTS`（不要额外边框）、`_NET_WM_DESKTOP` 跟随主窗口、`_NET_WM_STATE` 加跳过任务栏/翻页器/切换器、`_NET_WM_USER_TIME=0`（不抢焦点），再 map 回去交给 KWin。

没有改 Wine 二进制，也没有一刀切屏蔽所有无标题窗口——**匹配不上的窗口原样保留**。

辅助程序由启动脚本自动拉起，单实例（`flock` 锁），企微退出后 45 秒左右自己退出。

**关掉它**（下次启动生效）：

```bash
WECOM_WINDOW_FIX=0 ~/.local/bin/wecom-wine
```

**回退**：

```bash
# 1. 停掉辅助程序
kill "$(cat ~/.local/state/wecom-wine/titlebar-manager.pid)"
# 2. 恢复窗口属性（需要有效的 X11 会话）
python3 ~/.local/lib/wecom-wine/manage-titlebar.py --restore
```

或者干脆退出企微重开，窗口属性会重建。

`x11.py` 是它用的 X11 调用封装（ctypes 直接调 libX11），两个文件要一起拷。

---

## 十、整体搬迁（直接打包前缀）

比重装快得多，推荐的「带走」方式。

```bash
# ── 旧机器 ──
WINEPREFIX="$HOME/.wine-wecom" wineserver -k        # 必须先停，否则注册表会拷成半截状态

tar -czf wecom-wine.tar.gz \
    -C "$HOME" \
    .wine-wecom \
    .local/bin/wecom-wine \
    .local/lib/wecom-wine \
    .local/state/wecom-wine
```

```bash
# ── 新机器 ──
sudo dnf install wine winetricks
tar -xzf wecom-wine.tar.gz -C "$HOME"
chmod +x ~/.local/bin/wecom-wine
```

**然后必须改路径**，新旧用户名/家目录不一样的话：

```bash
# 1. 启动脚本里的两个绝对路径
sed -i "s|/home/旧用户名|$HOME|g" ~/.local/bin/wecom-wine

# 2. 桌面文件（三个）
find ~/.local/share/applications ~/Desktop -name '企业微信.desktop' \
  -exec sed -i "s|/home/旧用户名|$HOME|g" {} \;

# 3. 前缀里的盘符软链（这个是重点，很容易漏）
cd ~/.wine-wecom/dosdevices
ln -sfn / z:
ln -sfn ../drive_c c:
```

`dosdevices/z:` 指向旧机器的根，不重建的话企微里打开文件对话框会指向一个不存在的路径。

`wineboot -u` 跑一遍让前缀适配新机器，然后启动。

> 前缀里有企微的登录态和聊天记录，整个拷过去是**带着登录状态**的。换机器等于迁移账号数据，确认这是你要的。

---

## 十一、日常使用

```bash
wxwork_start        # 启动
wxwork_stop         # 全部杀掉（企微卡死时用）
```

**退出企微后一定要等它真的退干净再重开**。企微是单实例的，上一个还没死透就重开，新进程会把参数转交给旧窗口然后自己退出，看起来像「启动没反应」。

**日志**：

```bash
tail -f ~/.local/state/wecom-wine/launcher.log        # 主程序输出
tail -f ~/.local/state/wecom-wine/titlebar-manager.log # 窗口修复
```

`launcher.log` 是追加的，很久没清的话几十 MB（现在 40MB）。里面**包含历史失败记录**，看的时候按时间戳看末尾，别被前面的旧报错带偏。

---

## 十二、排错速查

| 症状 | 原因 | 处理 |
|---|---|---|
| 进程起来了，窗口不显示 / 点不动 | Windows 版本不是 win10 | 见 4.1 |
| 窗口不显示、花屏 | 走了 Wayland 驱动 | 见 4.2，注册表 + `unset WAYLAND_DISPLAY` 都要 |
| 界面英文 | `LC_ALL` 是 `C.UTF-8` | 见 4.3 |
| 中文显示成方块 | 没装 CJK 字体 | 见第五节 |
| 启动没反应 | 旧实例没退干净 | `wxwork_stop` 后重开 |
| 启动报 X 连接失败 | `XAUTHORITY` 失效 | 启动脚本已自动探测，见第六节 |
| 窗口切换桌面时错位 | 标题栏 override_redirect | 见第九节，确认辅助程序在跑 |
| 任务栏出现无名图标 | 桌面文件缺 `StartupWMClass` | 见第七节 |

**查 Wine 到底用了哪个图形驱动**：

```bash
WINEPREFIX="$HOME/.wine-wecom" wine reg query 'HKCU\Software\Wine\Drivers'
```

**查窗口（走 XWayland，X 侧工具可见）**：

```bash
xwininfo -root -tree | grep -i wxwork
```

**看辅助程序在不在**：

```bash
pgrep -af manage-titlebar.py
```

---

## 十三、已知未解决 / 待观察

- **虚拟桌面模式试过，不采用**。`wine explorer /desktop=WeCom,1280x900 WXWork.exe` 把企微收进一个外层桌面窗口，实测有明显黑色边框，已回退。窗口重叠问题改用第九节的方案。
- **音频/语音**：麦克风链路有基础条件（`wine-pulseaudio` 已装、默认输入设备识别正常、`winepulse` 设备注册记录里有对应输入设备），但**企微自己的语音通话、语音消息未做端到端实测**，没有录音流、波形、延迟数据。详见 `~/.local/state/wecom-wine/语音程序兼容性评估.md`。
- **企微版本升级**：企微有自带的 `WXWorkUpgrader`，升级后窗口布局可能变，`manage-titlebar.py` 的匹配条件（高 15–64 像素、同宽同位置等）可能需要跟着调整。升级后如果窗口又开始乱跑，先怀疑这里。

---

## 参考

- Wine 11 图形驱动选择：[dlls/win32u/driver.c](https://github.com/wine-mirror/wine/blob/wine-11.0/dlls/win32u/driver.c)
- Wine 窗口受管判断（`is_window_managed`）：[dlls/winex11.drv/window.c](https://github.com/wine-mirror/wine/blob/wine-11.0/dlls/winex11.drv/window.c)
- KWin 受管窗口处理：[src/x11window.cpp](https://github.com/KDE/kwin/blob/master/src/x11window.cpp)
- KWin 验证接口：[develop.kde.org/docs/plasma/kwin/api](https://develop.kde.org/docs/plasma/kwin/api/)
- Noto CJK 静态字体：[notofonts/noto-cjk](https://github.com/notofonts/noto-cjk/tree/main/Sans/OTF/SimplifiedChinese)
- Winetricks 中文字体别名：[winetricks src](https://github.com/Winetricks/winetricks/blob/master/src/winetricks)
- 原始配置记录与备份：`~/.local/state/wecom-wine/配置说明.md`、`backup-20260907-145725/`
