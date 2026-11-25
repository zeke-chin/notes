# sync-rules

- 简介：统一项目里的 AI 规则文件。默认扫描 `AGENTS.md`、`CLAUDE.md`（可选 `-g` 纳入 `GEMINI.md`），将真实规则收敛到一个 `.rules.md`，其余文件以相对路径软链接指向它。

## 行为逻辑

1. 扫描 `.rules.md` 以及目标入口文件中的**真实文件**（自动忽略已有软链接）：
   - **0 个**：创建空的 `.rules.md`。
   - **1 个**：直接将其迁移为 `.rules.md`（若原本就是 `.rules.md` 则保留）。
   - **多个**：交互列出所有候选文件，由你输入编号选择保留哪一个作为 `.rules.md`。
2. 将入口文件统一创建为指向 `.rules.md` 的相对软链接。

## 使用方式

```sh
# 默认只处理 AGENTS.md、CLAUDE.md
./sync-rules.sh

# 额外纳入 GEMINI.md
./sync-rules.sh -g
./sync-rules.sh --gemini /path/to/project

# 自定义目标真实文件名（例如 Zed 风格的 .rules）
RULES_FILE=.rules ./sync-rules.sh
```

建议软链接到 `PATH` 下方便全局调用：

```sh
ln -sfn "/Users/zeke/workspace/github_work/notes/🛠️常用工具/cli/sync-rules/sync-rules.sh" ~/.local/bin/sync-rules
```
