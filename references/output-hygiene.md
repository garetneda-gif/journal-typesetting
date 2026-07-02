# 输出可见性与文件夹治理

本文件是文章目录整理、源文件归档、隐藏中间产物和最终可见文件规则的唯一权威入口。执行完成前必须运行 `scripts/audit_visible_outputs.py`。

## 1. 根目录治理

工作根目录：`/Users/jikunren/Documents/期刊排版`。

允许保留的根级可见目录：

- `mbamNN-{short_title}` 文章目录。

允许保留的根级可见文件：

- `MedBA-期刊排版规格-vN.N.pdf`
- `MedBA-期刊排版规范-vN.N.pdf`

允许保留的根级隐藏目录：

- `.logs`
- `.sequence`
- `.reference`
- `.incoming`

根目录不应散落源文件、临时脚本、截图、JSON 报告、zip、下载副本或调试 HTML。

## 2. 文章目录可见文件规则

每个 `mbamNN-{short_title}` 目录默认只显式展示：

- `two-column-{short_title}.html`
- `single-column-{short_title}.html`

用户明确要求 PDF 时，可以额外显式展示：

- `10.65079/mbamNN.pdf`

不得显式展示：

- `preview`、`local`、`typography-fixed`、`final-v2`、hash 命名 HTML。
- 调试截图。
- 构建脚本。
- 中间 JSON。
- 上传源文件。
- 临时压缩包。

## 3. 文章目录隐藏子目录

每篇文章的中间产物归入隐藏目录：

- `.source`：用户上传的原始 Word、图片、zip、补充文件。
- `.assets`：本地处理后的图片、表格图、图床上传准备文件。
- `.tmp`：一次性脚本、构建草稿、导出辅助文件。
- `.screenshot`：Playwright 逐页截图。
- `.validation`：几何指标、链接验证、样式验证、审计输出。

如 macOS Finder 仍显示这些目录，可执行：

```bash
chflags hidden .source .assets .tmp .screenshot .validation 2>/dev/null || true
```

## 4. 源文件进入规则

- 用户上传的源文件不得散落在根目录。
- 若已能确定文章短标题，源文件进入对应文章目录的 `.source/`。
- 若短标题尚未确定，源文件先进入根目录 `.incoming/`。
- 短标题确认后，从 `.incoming/` 移入 `{doi_suffix}-{short_title}/.source/`。

## 5. 文件命名短标题原则

- 文件名使用 `short_title`，不得使用整篇长标题。
- `short_title` 同步用于文章目录、HTML、PDF、图床目录、验证目录。
- 最终文件名必须是：
  - `two-column-{short_title}.html`
  - `single-column-{short_title}.html`
  - `10.65079/mbamNN.pdf`（仅按需）
- PDF 路径必须直接使用 DOI 斜杠形式，禁止继续使用 `two-column-{short_title}.pdf`。

## 6. 必用审计命令

默认不允许 PDF 显式展示：

```bash
python3 scripts/audit_visible_outputs.py "/Users/jikunren/Documents/期刊排版"
```

用户要求输出 PDF 时允许 PDF：

```bash
python3 scripts/audit_visible_outputs.py "/Users/jikunren/Documents/期刊排版" --allow-pdf
```

审计失败时，必须先移动或隐藏无关文件，再交付。
