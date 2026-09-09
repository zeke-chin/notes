按你这台机器来选：Fedora 44 + KDE Plasma 6 + Wayland + `zh_CN.UTF-8`，现在还是 Noto Sans。最合适不是整仓 clone xMuu，而是 **新字体 + 一份自己的 fontconfig**。

## 推荐组合

| 用途 | 字体 | 来源 |
|------|------|------|
| 西文 / UI | **SF Pro Text**（界面 10–11pt） | [developer.apple.com/fonts](https://developer.apple.com/fonts/) 的 SF Pro.dmg |
| 中文 | **PingFang SC** | 从 Mac 的 `PingFang.ttc` 拆，或社区 otf |
| 等宽 | **SF Mono** | 同一页的 SF Mono.dmg |
| Emoji | **Apple Color Emoji** | [samuelngs/apple-emoji-ttf](https://github.com/samuelngs/apple-emoji-ttf) 的 Fedora rpm |
| 衬线（可选） | New York 或继续 Noto Serif CJK | 不关键 |

不要用 2019 的 xMuu 字体文件，只借它的「西文 SF、中文苹方」思路。

## Fedora 安装顺序

**1. Emoji（有现成 rpm）**

从 Releases 下 `fonts-apple-color-emoji.rpm`：

```bash
sudo dnf install ./fonts-apple-color-emoji.rpm
# 降低 Noto emoji 抢优先级，不必强删
```

**2. SF Pro / SF Mono**

```bash
sudo dnf install p7zip p7zip-plugins
# 下载 SF-Pro.dmg、SF-Mono.dmg
7z x SF-Pro.dmg
# 再解里面的 .pkg / Payload，把 *.otf 拷走
mkdir -p ~/.local/share/fonts/{SF-Pro,SF-Mono}
cp *.otf ~/.local/share/fonts/SF-Pro/
fc-cache -fv
```

一键脚本也可以：[MohamedElashri/apple-fonts](https://github.com/MohamedElashri/apple-fonts)

**3. 苹方**

有 Mac：拷 `/System/Library/Fonts/PingFang.ttc`，用 `otc2otf` 拆出 `PingFangSC-*.otf`。  
没有 Mac：用已经改过 family 名的包，例如 [yellowpeter2019/PingFangSC4Linux](https://github.com/yellowpeter2019/PingFangSC4Linux) 或 [vzxxbacq/PingFang_Font_For_Linux](https://github.com/vzxxbacq/PingFang_Font_For_Linux) 的 SC。

装到 `~/.local/share/fonts/PingFang/`，确认：

```bash
fc-list :lang=zh | grep -i pingfang
```

应看到 `PingFang SC`，不要是 `.PingFang SC`。

## fontconfig（用户级，别改系统文件）

`~/.config/fontconfig/fonts.conf`：

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
      <family>SF Pro Text</family>
      <family>PingFang SC</family>
    </prefer>
  </alias>
  <alias>
    <family>monospace</family>
    <prefer>
      <family>SF Mono</family>
      <family>PingFang SC</family>
    </prefer>
  </alias>
  <alias>
    <family>serif</family>
    <prefer>
      <family>Noto Serif CJK SC</family>
    </prefer>
  </alias>
  <alias>
    <family>emoji</family>
    <prefer>
      <family>Apple Color Emoji</family>
    </prefer>
  </alias>
</fontconfig>
```

```bash
fc-cache -fv
```

## KDE 里怎么设

系统设置 → 字体：

- 常规 / 菜单 / 小工具：**SF Pro Text 10pt**（你现在是 Noto Sans 10pt，字号先别动）
- 等宽：**SF Mono 10pt**
- 不要把苹方设成全局西文字体，中文靠 fallback
- Plasma 6 Wayland 改完注销一次更稳

Herdr / 终端单独选 SF Mono。

## 不建议的

- 整仓装 xMuu（字体旧、无 emoji、ttc 在 Fedora 上容易选不中）
- 系统级覆盖 `/etc/fonts`（升级容易打架）
- 把 Apple Color Emoji 当 UI 字体

先装 emoji + SF + 苹方三件，确认 `fc-match sans-serif`、`fc-match monospace`、`fc-match emoji` 分别落到 SF Pro Text、SF Mono、Apple Color Emoji，再改 KDE 字体面板。
