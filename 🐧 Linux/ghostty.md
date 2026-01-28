https://ghostty.org/docs/config/keybind

这是 Ghostty 终端默认快捷键的翻译与功能详细解释。

**注意：**
*   **Super** 键在 macOS 上是 `Command (⌘)`，在 Linux/Windows 上通常是 `Windows` 键。
*   **Alt** 键在 macOS 上是 `Option (⌥)`。

---

### 1. 窗口与标签页管理 (Windows & Tabs)
*   `super + n`: **新建窗口** (`new_window`)
*   `super + t`: **新建标签页** (`new_tab`)
*   `super + w`: **关闭当前表面** (标签页或窗口) (`close_surface`)
*   `super + alt + w`: **关闭当前标签页** (`close_tab:this`)
*   `super + shift + w`: **关闭当前窗口** (`close_window`)
*   `super + alt + shift + w`: **关闭所有窗口** (`close_all_windows`)
*   `super + q`: **退出 Ghostty** (`quit`)

**切换标签页：**
*   `super + digit_1` 到 `8` (或 `super + 1` 到 `8`): **切换到第 1-8 个标签页**
*   `super + 9`: **切换到最后一个标签页** (`last_tab`)
*   `super + shift + bracket_left` (`[`): **上一个标签页**
*   `super + shift + bracket_right` (`]`): **下一个标签页**
*   `ctrl + tab`: **下一个标签页**
*   `ctrl + shift + tab`: **上一个标签页**

---

### 2. 分屏管理 (Splits)
*   `super + d`: **垂直分屏** (在右侧打开新分屏) (`new_split:right`)
*   `super + shift + d`: **水平分屏** (在下方打开新分屏) (`new_split:down`)
*   `super + shift + enter`: **缩放分屏切换** (将当前分屏临时最大化/恢复) (`toggle_split_zoom`)
*   `super + ctrl + equal` (`=`): **等分屏幕** (让所有分屏大小一致) (`equalize_splits`)

**分屏导航与调整：**
*   `super + alt + arrow_up/down/left/right`: **按方向切换分屏焦点**
*   `super + bracket_left` (`[`): **切换到上一个分屏**
*   `super + bracket_right` (`]`): **切换到下一个分屏**
*   `super + ctrl + arrow_up/down/left/right`: **调整分屏边缘大小** (每次 10 个单位)

---

### 3. 文本操作与剪贴板 (Text & Clipboard)
*   `super + c` / `copy`: **复制到剪贴板**
*   `super + v` / `paste`: **从剪贴板粘贴**
*   `super + shift + v`: **从选中的文本粘贴** (`paste_from_selection`)
*   `super + a`: **全选** (`select_all`)
*   `super + z`: **撤销** (在某些支持的输入场景)
*   `super + shift + z` / `super + shift + t`: **重做** (`redo` / `undo`)
*   `super + k`: **清除屏幕** (相当于 `clear` 命令)

---

### 4. 屏幕滚动与光标导航 (Navigation & Scroll)
*   `super + home` / `super + end`: **滚动到最顶部 / 最底部**
*   `super + page_up` / `super + page_down`: **向上 / 向下翻页滚动**
*   `super + arrow_up` / `super + arrow_down`: **跳转到上一个 / 下一个提示符(Prompt)** (需要 Shell 集成支持)
*   `super + arrow_left`: **移动光标到行首** (发送 `Ctrl+A`)
*   `super + arrow_right`: **移动光标到行尾** (发送 `Ctrl+E`)
*   `alt + arrow_left`: **光标向后跳一个单词** (发送 `Esc b`)
*   `alt + arrow_right`: **光标向前跳一个单词** (发送 `Esc f`)
*   `super + backspace`: **删除光标前整行** (发送 `Ctrl+U`)

**选择模式调整 (Shift + 方向键):**
*   `shift + arrow_up/down/left/right`: **按方向调整选择范围**
*   `shift + home/end/page_up/page_down`: **快速扩展选择范围**

---

### 5. 字体与 UI 控制 (Font & UI)
*   `super + equal` (`=`) / `super + +`: **增大字体**
*   `super + minus` (`-`): **减小字体**
*   `super + 0`: **重置字体大小**
*   `super + enter` / `super + ctrl + f`: **切换全屏**
*   `super + alt + i`: **打开/关闭检查器** (用于调试终端渲染和状态)
*   `super + shift + p`: **打开命令面板** (类似 VS Code 的 Command Palette)

---

### 6. 配置管理 (Configuration)
*   `super + ,`: **打开配置文件** (`open_config`)
*   `super + shift + ,`: **重新加载配置文件** (`reload_config`)

---

### 7. 屏幕录制/文件操作 (Screen File)
*   `super + alt + shift + j`: **打开屏幕内容文件** (通常用于导出当前屏幕内容查看)
*   `super + ctrl + shift + j`: **复制屏幕内容到文件**
*   `super + shift + j`: **从屏幕文件粘贴内容**

---

### 总结
这些快捷键让 Ghostty 的体验非常接近一个现代编辑器（如 VS Code）。**核心逻辑**是：
*   `Super + 字母/数字`：基础操作（标签、窗口、复制粘贴）。
*   `Super + Alt`：侧重于分屏导航。
*   `Super + Ctrl`：侧重于调整 UI（大小、全屏）。
*   `Super + Shift`：侧重于高级动作（重载配置、命令面板、跳转提示符）。