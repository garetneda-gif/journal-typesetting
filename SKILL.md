---
name: journal-typesetting
description: |
  将Word学术论文转换为MedBA Medicine期刊HTML格式。支持双栏分页(PDF下载)和单栏连续(在线预览)两种输出。
  自动为参考文献添加验证后的元数据链接(PubMed | Google Scholar | Crossref)。
  使用场景：当用户提供生物科学的学术论文及其附件并要求排版为期刊HTML格式时使用。
  触发词：生物期刊排版，生物排版，MedBA排版
mcp:
  pubmed:
    command: npx
    args: ["@cyanheads/pubmed-mcp-server"]
  crossref:
    command: npx
    args: ["-y", "@botanicastudios/crossref-mcp"]
---
# 期刊排版技能 (Journal Typesetting)

## 目的

把 Word 学术论文排成 MedBA Medicine 的两套 HTML：

1. **双栏分页版**：A4 分页，用于 PDF 下载。
2. **单栏连续版**：连续滚动，用于在线预览，包含参考文献元数据链接。

`SKILL.md` 只做工作流调度。深规则在 `references/`，重复且可验证的检查交给 `scripts/`。

## 期刊默认配置

- **期刊名称**：MedBA Medicine
- **Logo**：`https://medbam.org/assets/logo.png`
- **网址**：`https://medbam.org`
- **主题色**：`#005a8c`
- **DOI 前缀**：`10.65079`
- **递增表**：`/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json`
- **文章图床**：`https://medbam.org/assets/{short_title}/Figure%20N.ext`
- **SFTP 上传**：`editor1@47.239.5.114:22`，配置见 `references/image-urls.md`

## 最高优先级不变量

执行时先满足这些约束，再考虑美观微调：

- 双栏、单栏和 PDF 的正文细节必须同步；修一个版本时同步检查另一个版本。
- 最终 HTML 禁止引用本地图片、`file://`、`./assets` 或项目相对图片路径。
- DOI、页码、文章顺序和文件夹名必须由递增表维护，不得凭记忆分配。
- DOI 必须严格写作 `10.65079/mbamNN`，禁止双斜杠、漏斜杠或大小写不一致。
- 文件夹名必须是 `{doi_suffix}-{short_title}`；文件名必须是 `two-column-{short_title}.html` 和 `single-column-{short_title}.html`。
- 可见文件默认只展示双栏 HTML 和单栏 HTML；PDF 只有用户明确要求时才显式展示。
- PDF 文件统一使用 DOI 路径名：`10.65079/mbamNN.pdf`；不再采用 `two-column-{short_title}.pdf`。
- `Keywords:` 使用逗号加空格分隔；每个关键词组只大写首个单词首字母，组内普通词小写，专有名词/基因符号/缩写保留规范大小写。
- 正文、摘要、图注和表注里的 `Figure N` / `Table N` 交叉引用必须加粗。
- 正文引用 `[n]` 必须与前一个词不可断绑定，不能成为视觉行首。
- 全文两端对齐，禁用自动断字；不得用拆词、短横线截断、spacer、绝对定位或手工换行解决分页问题。
- 双栏正文必须 S 型灌版：先填满左栏，再填右栏。
- CP3、CP4 或最终验证失败时，不得交付。

## 资源索引

| 类型 | 文件 | 用途 |
|---|---|---|
| 模板 | `assets/template-two-column.html` | 双栏分页 HTML 模板 |
| 模板 | `assets/template-single-column.html` | 单栏连续 HTML 模板 |
| 脚本 | `scripts/sequence_manager.py` | DOI/page/递增表维护 |
| 脚本 | `scripts/audit_visible_outputs.py` | 可见文件审计 |
| 脚本 | `scripts/audit_doi_pages.py` | DOI 与页码输出一致性审计 |
| 脚本 | `scripts/style_validator.py` | 样式一致性验证 |
| 脚本 | `scripts/validate_two_column_layout.mjs` | 双栏 Playwright 几何验证 |
| 脚本 | `scripts/verify_links.py` | 参考文献链接验证 |
| 参考 | `references/dependency-check.md` | 第0步依赖检查 |
| 参考 | `references/docx-parsing.md` | Word 解析、标题和短标题 |
| 参考 | `references/image-urls.md` | 图片上传和 URL 验证 |
| 参考 | `references/sequence-and-output.md` | DOI/page/命名/递增表规则 |
| 参考 | `references/output-hygiene.md` | 源文件归档和可见文件规则 |
| 参考 | `references/layout-gates.md` | CP0-CP5、S 型和截图门控 |
| 参考 | `references/pagination-rules.md` | 双栏分页深规则 |
| 参考 | `references/typesetting-rules.md` | 正文、关键词、图表、引用细节 |
| 参考 | `references/style-mapping.md` | CSS 和模板样式映射 |
| 参考 | `references/reference-links.md` | 参考文献 Vancouver 与链接规则 |
| 参考 | `references/validation-checklist.md` | 最终交付 checklist |
| 参考 | `references/troubleshooting.md` | 常见问题与大文件写入规则 |

> HTML 大于 30KB 时，按 `references/troubleshooting.md` 的大文件写入规则处理，避免工具写入截断。

## 必读文件与必跑脚本

| 步骤 | 必读 reference | 必跑或优先脚本 |
|---|---|---|
| 第0步 依赖检查 | `dependency-check.md` | 依赖检查命令 |
| 第1步 解析文档 | `docx-parsing.md`, `sequence-and-output.md` | `sequence_manager.py validate` |
| 第2步 上传图片 | `image-urls.md` | SFTP + HTTP 验证 |
| 第3步 双栏 HTML | `pagination-rules.md`, `layout-gates.md`, `typesetting-rules.md`, `style-mapping.md` | `validate_two_column_layout.mjs`, `style_validator.py` |
| 第4步 单栏 HTML | `typesetting-rules.md`, `style-mapping.md` | `style_validator.py` |
| 第5步 参考文献 | `reference-links.md` | `verify_links.py` |
| 第6步 输出治理 | `sequence-and-output.md`, `output-hygiene.md` | `sequence_manager.py`, `audit_visible_outputs.py`, `audit_doi_pages.py` |
| 第7步 最终验证 | `validation-checklist.md`, `layout-gates.md` | 全部相关审计脚本 |

## 工作流程

```text
[预检] 明确输入和目标文章 → [0] 依赖检查 → [1] 解析 Word + 短标题 + 序列表 →
[2] 上传图片 → [3] 生成双栏 HTML → [4] 生成单栏 HTML →
[5] 规范参考文献并加链接 → [6] 输出治理 → [7] 最终验证
```

## 第0步：依赖检查

**目标**：确认 docx 解析、MCP、浏览器验证和本地脚本可运行。

- 读取 `references/dependency-check.md`。
- docx skill 不可用时先停下处理；不要靠猜测解析 Word。
- PubMed/Crossref MCP 不可用时，按 CP0 询问是否降级到 fallback。
- Playwright/Chrome 或 Node 运行时不可用时，不得跳过 CP3；先修依赖或明确说明阻塞。

## 第1步：解析 Word 文档并确定短标题

**目标**：得到标题、作者、摘要、正文、图表、参考文献、短标题和序列状态。

- 读取 `references/docx-parsing.md`。
- 读取 `references/sequence-and-output.md`。
- 文章主标题转换为 sentence case；专有名词、基因符号和缩写保留规范大小写。
- 摘要标签标准化为 `Background:` / `Methods:` / `Results:` / `Conclusion:`；`Objective:` 改为 `Background:`。
- 短标题确认后单独输出一行可复制文本。
- 开始排版前运行：

```bash
python3 scripts/sequence_manager.py validate \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --root "/Users/jikunren/Documents/期刊排版"
```

## 第2步：上传图片到图床

**目标**：所有正文 Figure / 图表图片进入 MedBA 图床，HTML 只引用 HTTPS URL。

- 读取 `references/image-urls.md`。
- 图床目录使用短标题：`/assets/{short_title}/`。
- 文件名使用 `Figure 1.png`、`Figure 2.jpg` 等规范形式，URL 空格写作 `%20`。
- 先用 `editor1@47.239.5.114:22` 直连上传，不得把 `medbam.org` 当 SSH 主机。
- 上传后验证 HTTP 200、权限可读、尺寸或哈希一致。

## 第3步：生成双栏分页 HTML

**目标**：生成可导出 PDF 的 A4 双栏 HTML，并通过 CP3。

- 使用 `assets/template-two-column.html`。
- 读取 `references/pagination-rules.md`、`references/layout-gates.md`、`references/typesetting-rules.md`、`references/style-mapping.md`。
- CSS 和 class 以模板为准；不要随机美化或重写模板。
- 正文表格使用三线表；图注和表注完整可见。
- 每次修改分页、图表、表格、页脚、段落缩进或参考文献分页后，都重跑：

```bash
node scripts/validate_two_column_layout.mjs /path/to/two-column.html --out /path/to/.screenshot
python3 scripts/style_validator.py /path/to/two-column.html --type two-column
```

- CP3 失败时回到分页修复，不得继续。

## 第4步：生成单栏连续 HTML

**目标**：生成在线预览用单栏连续 HTML，并与双栏终稿同步。

- 使用 `assets/template-single-column.html`。
- 读取 `references/typesetting-rules.md` 和 `references/style-mapping.md`。
- 单栏禁止分页符、`page-break` 或分页 CSS。
- 摘要、关键词、正文引用、Table/Figure 加粗、p 值斜体、表格三线表、Back Matter 标点都以双栏终稿为准同步。
- 单栏 References 保持连续版元数据链接结构，不按双栏分页版拆栏。

## 第5步：参考文献规范化与链接

**目标**：统一 Vancouver 风格，并为单栏连续版添加元数据链接。

- 读取 `references/reference-links.md`。
- 不臆造 DOI/PMID；低置信匹配跳过并记录。
- 参考文献正文统一为 Vancouver 风格；作者超过 3 位时列前 3 位后加 `et al.`。
- 双栏和单栏的参考文献正文必须一致；单栏只额外添加 PubMed / Google Scholar / Crossref 链接。
- CP4 至少确认 Google Scholar 链接数量等于参考文献总数，并记录 PubMed/Crossref 实际数量。

## 第6步：输出文件与目录治理

**目标**：只保留规范命名的可见成品，源文件和中间产物全部归档。

- 读取 `references/sequence-and-output.md` 和 `references/output-hygiene.md`。
- 若用户要求 PDF，PDF 路径命名为 `10.65079/mbamNN.pdf`；禁止再使用 `two-column-{short_title}.pdf`。
- 输出后运行：

```bash
python3 scripts/audit_visible_outputs.py "/Users/jikunren/Documents/期刊排版" --allow-pdf
python3 scripts/audit_doi_pages.py \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --root "/Users/jikunren/Documents/期刊排版" \
  --check-pdf
```

- 如果没有 PDF 交付，去掉 `--allow-pdf` 和 `--check-pdf`。

## 第7步：最终验证

**目标**：用 checklist 和脚本确认可交付。

- 读取 `references/validation-checklist.md`。
- 必须验证：
  - 双栏和单栏文件存在且命名规范。
  - DOI/page 与递增表一致。
  - 可见文件审计通过。
  - 双栏 CP3 几何验证通过。
  - 样式验证通过。
  - 单栏/双栏文本细节同步。
  - 图片全为 MedBA HTTPS 图床 URL。
  - 参考文献编号连续且链接记录完整。
- 最终报告写明：输出文件、页数、DOI、参考文献链接统计、运行过的验证命令和任何 warning。

## 常用审计命令

```bash
python3 scripts/sequence_manager.py validate \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --root "/Users/jikunren/Documents/期刊排版"

python3 scripts/audit_visible_outputs.py "/Users/jikunren/Documents/期刊排版" --allow-pdf

python3 scripts/audit_doi_pages.py \
  --sequence "/Users/jikunren/Documents/期刊排版/.sequence/medba-issue-sequence.json" \
  --root "/Users/jikunren/Documents/期刊排版" \
  --check-pdf
```
