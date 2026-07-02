# DOI、页码与输出序列规则

本文件是 MedBA 期刊排版中 DOI、页码、文章文件夹命名和序列表维护的唯一权威入口。执行任何新文章排版、页数调整、PDF 重导出或用户指定 DOI 时，先读本文件，再使用 `scripts/sequence_manager.py`。

## 1. 递增表位置与 schema

- 递增表固定位置：`/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json`。
- 该文件是隐藏维护文件，必须在每次新文章排版、页数变化、PDF 重导出、DOI 补号前读取。
- 若文件不存在，先扫描现有 `mbamNN-*` 文章目录、双栏 HTML 和 PDF 初始化，不得凭记忆分配 DOI 或页码。

递增表必须至少包含：

```json
{
  "issue": "MedBA Medicine working sequence",
  "doi_prefix": "10.65079",
  "last_updated": "2026-06-30T10:00:00+08:00",
  "entries": [
    {
      "order": 5,
      "short_title": "GERD-LBN-Mendelian-Randomization",
      "doi_suffix": "mbam05",
      "doi": "10.65079/mbam05",
      "page_start": 50,
      "page_end": 54,
      "page_count": 5,
      "two_column_html": "mbam05-GERD-LBN-Mendelian-Randomization/two-column-GERD-LBN-Mendelian-Randomization.html",
      "single_column_html": "mbam05-GERD-LBN-Mendelian-Randomization/single-column-GERD-LBN-Mendelian-Randomization.html",
      "pdf": "mbam05-GERD-LBN-Mendelian-Randomization/10.65079/mbam05.pdf",
      "status": "active",
      "folder": "mbam05-GERD-LBN-Mendelian-Randomization",
      "notes": ""
    }
  ]
}
```

## 2. DOI 分配规则

- DOI 前缀固定为 `10.65079`。
- DOI suffix 使用小写 `mbamNN`，`NN` 为两位或更多位数字，例如 `mbam04`、`mbam05`、`mbam06`。
- 新 active 文章默认使用当前最大 `mbamNN + 1`。
- DOI 字符串必须严格为 `10.65079/mbamNN`。
- 禁止出现：
  - `10.65079//mbamNN`
  - `10.65079mbamNN`
  - `10.65079/MBAMNN`
  - 双栏、单栏、PDF DOI 不一致

## 3. 页码分配规则

- 新 active 文章默认 `page_start = 当前最大 active page_end + 1`。
- `page_end = page_start + page_count - 1`。
- active entry 的页码必须连续；不得重叠、断档或倒序。
- 每次双栏分页页数变化后，立即更新递增表。
- 如果被修改文章后面还有 active entry，必须顺延后续文章的页码区间，并同步更新双栏 HTML 页脚和已导出的 PDF。

## 4. needs_doi_assignment 激活流程

当用户后续确认某篇待分配文章的 DOI，例如“WAA 是 04”：

1. 找到 `status = needs_doi_assignment` 且 `short_title` 匹配的 entry。
2. 设置 `doi_suffix = mbam04`、`doi = 10.65079/mbam04`。
3. 设置 `status = active`。
4. 按实际双栏页数设置 `page_count`、`page_start`、`page_end`。
5. 将文章文件夹重命名为 `{doi_suffix}-{short_title}`。
6. 同步更新 `two_column_html`、`single_column_html`、`pdf` 路径。
7. 修正双栏 HTML、单栏 HTML 和 PDF 中的 DOI 显示。
8. 重新导出 PDF，并用文本抽取确认没有 `10.65079//` 残留。

## 5. 文件夹与文件命名

- 文章文件夹名：`{doi_suffix}-{short_title}`，例如 `mbam05-GERD-LBN-Mendelian-Randomization`。
- 双栏 HTML：`two-column-{short_title}.html`。
- 单栏 HTML：`single-column-{short_title}.html`。
- PDF 仅用户明确要求时生成或显式展示：`10.65079/mbamNN.pdf`。
- DOI 斜杠在文件系统中表现为路径分隔符；例如 DOI `10.65079/mbam06` 对应 PDF 路径 `10.65079/mbam06.pdf`。
- 若用户明确要求用标题命名下载文件，使用下划线连接标题词，避免空格、斜杠和标点；默认仍优先 DOI 安全名。
- 浏览器或 PDF.js 自带 Download 按 PDF URL basename 或服务器 `Content-Disposition` 命名；上传/发布时必须使用 DOI 路径 PDF，不能使用 `two-column-{short_title}.pdf` 作为客户下载文件。
- `short_title` 是本篇文章唯一内容命名根，贯穿 HTML、PDF、图床目录、验证目录和递增表。

## 6. 必用脚本

### 校验递增表

```bash
python3 scripts/sequence_manager.py validate \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --root "/Users/jikunren/Documents/期刊排版"
```

### 查看下一篇候选 DOI 和页码

```bash
python3 scripts/sequence_manager.py next \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --short-title "Example-Short-Title" \
  --page-count 7
```

### 写入新文章

```bash
python3 scripts/sequence_manager.py assign \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --short-title "Example-Short-Title" \
  --page-count 7 \
  --write
```

### 激活待分配文章

```bash
python3 scripts/sequence_manager.py activate \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --short-title "WAA-Anorectal-Scoping-Review" \
  --doi-suffix mbam04 \
  --page-count 10 \
  --write
```

### 更新页数并顺延后续文章

```bash
python3 scripts/sequence_manager.py update-pages \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --doi-suffix mbam05 \
  --page-count 6 \
  --write
```

## 7. 原子写入规则

- 写入递增表必须先写 `.tmp` 文件。
- `.tmp` 必须能被 JSON parser 重新读取。
- 验证通过后再替换正式文件。
- 禁止留下多个可见副本、手工 copy、`final.json`、`v2.json`。
- 写入后立即运行 `validate`。
