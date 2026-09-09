#!/usr/bin/env python3
"""Render representative text through Qt and record actual fallback glyph runs."""
import json
import os
from pathlib import Path

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PySide6.QtCore import QPointF
from PySide6.QtGui import QFont, QGuiApplication, QImage, QPainter, QColor, QTextLayout

app = QGuiApplication([])
project = Path(__file__).resolve().parent
out = project / 'verification'
out.mkdir(exist_ok=True)
samples = [
    ('UI 10pt', 'SF Pro Text', 10, False, 'Fedora KDE Plasma 6 — 文件 编辑 查看 设置 0123456789'),
    ('UI 11pt', 'SF Pro Text', 11, False, '中英混排 Hello World：你好，世界！“引号”（括号）《书名》'),
    ('UI bold', 'SF Pro Text', 11, True, 'Save changes 保存更改 — 确认 / 取消'),
    ('Chinese regular', 'SF Pro Text', 16, False, '简体中文：永国汉字，标点。繁體中文：臺灣香港。'),
    ('Monospace', 'SF Mono', 12, False, 'const answer = 42;  // 中文注释  O0 Il1 {} [] -> !='),
    ('Terminal grid', 'SF Mono', 12, False, '┌──────────────┐\n│ 中文 ABC 123 │\n└──────────────┘'),
    ('Emoji', 'SF Pro Text', 20, False, '😀 😃 🎉 🚀 🍎 👍🏽 👨‍👩‍👧‍👦 🇨🇳 ❤️'),
    ('Text vs emoji', 'SF Pro Text', 15, False, '© ™ → ♥︎ ❤︎  |  ♥️ ❤️  |  123 # *'),
    ('Rare Han fallback', 'SF Pro Text', 16, False, '生僻字：𠮷 𠀀 𪚥'),
]
image = QImage(1120, 840, QImage.Format.Format_ARGB32_Premultiplied)
image.fill(QColor('#f8fafc'))
painter = QPainter(image)
painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
report = []
y = 24
for label, family, size, bold, text in samples:
    painter.setPen(QColor('#64748b'))
    painter.setFont(QFont('Noto Sans', 10))
    painter.drawText(QPointF(24, y + 16), label)
    y += 27
    font = QFont(family, size)
    font.setBold(bold)
    painter.setPen(QColor('#0f172a'))
    for part in text.split('\n'):
        layout = QTextLayout(part, font)
        layout.beginLayout()
        line = layout.createLine()
        line.setLineWidth(1072)
        layout.endLayout()
        layout.draw(painter, QPointF(24, y))
        runs = []
        for run in layout.glyphRuns():
            raw = run.rawFont()
            runs.append({'family': raw.familyName(), 'style': raw.styleName(),
                         'glyphs': len(run.glyphIndexes()),
                         'missing_glyphs': sum(g == 0 for g in run.glyphIndexes())})
        report.append({'label': label, 'text': part, 'runs': runs})
        y += line.height() + 5
    y += 15
painter.end()
image.copy(0, 0, 1120, min(840, int(y + 12))).save(str(out / 'qt-font-preview.png'))
(out / 'qt-glyph-runs.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
