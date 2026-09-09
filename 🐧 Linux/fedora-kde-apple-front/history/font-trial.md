> 这是原工作目录中的历史记录。当前复用入口见 [README](../README.md)，本机原始回滚使用本目录的 `rollback-font-trial.py`。

# 本机字体试用记录

2026-09-09，Fedora 44 KDE / Wayland / zh_CN.UTF-8。已安装并应用。

## 当前设置

| 用途 | 设置 |
| --- | --- |
| KDE 常规、菜单、窗口标题 | SF Pro Text 10pt |
| 工具栏 | SF Pro Text 9pt，保留原字号 |
| 小字 | SF Pro Text 8pt，保留原字号 |
| 中文界面回退 | PingFang SC；缺字继续回退 Noto Sans CJK SC |
| 等宽 | SF Mono 10pt；中文回退 Noto Sans Mono CJK SC |
| Emoji | Apple Color Emoji；保留 Noto Color Emoji |
| 衬线 | 保留系统默认 |

安装了 35 个字体文件，均位于 `~/.local/share/fonts/apple-font-trial/`。
配置位于 `~/.config/fontconfig/conf.d/60-apple-font-trial.conf`，项目副本见
[config/60-apple-font-trial.conf](../config/60-apple-font-trial.conf)。
没有安装 RPM，也没有写入它附带的 `/etc/fonts/conf.d/50-apple-color-emoji.conf`。

SF Pro Text、SF Mono 来自 [Apple 官方字体页](https://developer.apple.com/fonts/)的 DMG，
使用 7z 解开 DMG → PKG → gzip Payload → cpio，安装静态 OTF。
苹方来自 [PingFangSC4Linux](https://github.com/yellowpeter2019/PingFangSC4Linux)，
下载固定 commit 的 Regular、Medium、Semibold、Light 四个 TTF。
该来源的 family 分散且字重均标记为 Regular，因此通过用户级 scan 规则规范为
PingFang SC 及对应字重，未修改字体二进制。
Emoji 仅从本目录 RPM 提取 TTF；其 SHA-256 与 RPM 文件清单一致。
下载 URL、固定 commit 和 SHA-256 保存在备份目录的 `sources.json` 中。
本机试用不会改变字体原有许可，字体文件未复制进项目目录。

## 验证结果与范围

- Fontconfig：英文 SF Pro Text；中文苹方；粗体中文匹配苹方 Semibold。
- 等宽英文 SF Mono，中文 Noto Sans Mono CJK SC。
- `emoji` 匹配 Apple；显式请求 `Noto Color Emoji` 仍匹配 Noto。
- Qt 实际 glyph runs 验证了上述中英文字体和字重。
- Qt 中肤色、家庭 ZWJ、国旗、爱心组合正常，9 个 Emoji 样例形成 9 个 Emoji 字形。
- 加入 Noto Sans Symbols 2 回退后，Qt 的文字心形保持单色，Emoji 心形为彩色。
- Qt 和 Pango 渲染结果已人工查看；两者的单色心形样式有差异。
- 稀有汉字 `𠮷` 回退 Noto 正常；`𠀀`（U+20000）、`𪚥`（U+2A6A5）缺字，
  `fc-list` 确认当前全部已安装字体均不覆盖这两个字符。
- 已回读全部 KDE 字体配置并核对；发送 `org.kde.KDEPlatformTheme.refreshFonts`，通知 KWin 重读配置。

预览是离屏排版结果，不代表逐个验证了浏览器、Flatpak 应用或实际终端。
其中框线样例是普通 Qt 文本布局，不能用它证明终端字符格严格对齐。
已运行应用可能仍缓存旧字体；重启对应应用后观察，有需要时再自行注销登录。
本次没有改动编辑器或终端的独立 profile，也没有关闭应用或注销会话。

- [Qt 预览](../verification/qt-font-preview.png)
- [Pango 预览](../verification/pango-font-preview.png)
- [Qt 字形记录](../verification/qt-glyph-runs.json)
- [Fontconfig 匹配记录](../verification/font-matches.json)

重新生成 Qt 预览：`python3 verify-font-trial.py`。

### 用户试用后的复测

- KDE 六项字体设置与应用值一致，用户级 fontconfig 与项目副本一致。
- 4 组常用中文、混排、代码字符和符号 × 6 种字号（8/9/10/11/12/14pt）× 常规/粗体，
  共 48 项 Qt 排版检查，没有缺字。
- 18 个 Emoji（包括肤色职业、家庭、国旗、彩虹旗、按键、摇头、凤凰、青柠）
  均使用 Apple Color Emoji，并各自形成一个字形。
- SF Mono 10pt 的 `i/W/0/空格/─` 宽度一致，均为 8.031px；
  Noto 中文回退在普通 Qt 排版中为 13px，不是西文的严格两倍。
  因此普通文本中的中英框线可能不齐，实际终端是否按字符格修正仍需终端内确认。
- 当前 UI 自动化没有可用的浏览器或原生应用连接，未直接检查用户桌面。
- [复测原始数据](../verification/retest.json)。本次复测未修改字体配置。

## 回滚

在本项目目录执行：

```bash
python3 rollback-font-trial.py
```

脚本恢复本次修改的 KDE 字体字段，保留其他 KDE 设置；如果某字段后来被手动改动，
保留该后续改动并提示。试用配置和字体移入备份目录，不直接删除，再刷新字体缓存。
回滚后重启使用这些字体的应用。

备份目录：`/home/zeke/.local/state/apple-font-trial/20260909-171254/`。
其中 `backup/` 保存修改前原始配置，`installed.json` 保存改动清单。
项目中的 `.font-trial-state` 指向本次备份；回滚脚本依赖此文件，请一并保留。
