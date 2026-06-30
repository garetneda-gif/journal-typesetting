# 正文排版细节规则（MANDATORY）

> 结构说明：本文件是正文与文本细节规则的权威来源。DOI/page 与命名规则见 `sequence-and-output.md`；输出隐藏与文件夹整理见 `output-hygiene.md`；双栏几何门控见 `layout-gates.md`。


> 从 SKILL.md 步骤3.4 提取的所有排版细节规则

---

## 图注与表注句点规则（MANDATORY）

- **图注（Figure N）和表注（Table N）后面不加句点**
- ❌ 错误示例：`Figure 2. Venny Plot`、`Table 1. Patient Demographics`
- ✅ 正确示例：`Figure 2 Venny Plot`、`Table 1 Patient Demographics`
- 适用范围：所有 `.fig-caption`、`.table-caption` 元素，以及正文内对图表的编号引用标签

## 图注对齐规则（MANDATORY）

- **并排图片（side-by-side-figures）必须使用 CSS Grid 布局**，确保图注底部对齐
- 布局原理：`display: grid` + `grid-template-columns: 1fr 1fr`，`figure` 设为 `display: contents`，`img` 固定 `grid-row: 1`（底部对齐 `align-self: end`），`figcaption` 固定 `grid-row: 2`（底部对齐 `align-self: end`）
- **禁止使用 `display: flex`**：flex 布局下不同高度的图片会导致图注起始位置不一致
- 所有图注统一 `text-align: justify`（两端对齐）
- 单独图片的图注也统一使用 justify
- Figure/Table 标签样式必须一致：`Figure N` 与 `Table N` 标签均使用同一主题色 `#005a8c` 和加粗；标签后不加句点，图注/表注正文按英文句子正常使用句末标点。
- 图注/表注必须完整可见：不得被图片高度、页脚、固定高度容器或 `overflow:hidden` 裁切；调整图片高度后必须用截图确认图注仍显示到句末。
- 关键大图必须纸质可读：跨栏大图优先接近内容区全宽展示。不得仅靠 `max-height` 把大图压成肉眼难以阅读的小图；必要时独立成图页或重排前后正文。

## 正文 URL 处理规则（MANDATORY）

- **正文中出现的所有 URL 必须包裹 `<a>` 标签**（`<a href="..." target="_blank">URL</a>`），禁止裸文本 URL
- 原因：`<a>` 标签已有 `overflow-wrap: anywhere; word-break: break-word;` 样式，允许 URL 在任意位置断行，避免 `text-align: justify` 在窄栏中产生巨大词间空白
- **全文正文和摘要必须禁用自动断字**：`.two-column`、`.abstract-box`、普通正文段落必须设置 `hyphens: none; -webkit-hyphens: none;`，禁止浏览器自动在普通英文单词处加入行尾短横线
- `overflow-wrap: anywhere` 仅允许用于 `<a>`、DOI、URL 或极长不可分字符串；不得对普通正文整体启用任意断词来消除 justify 空白
- 适用范围：所有正文段落中的数据库链接、工具网址等

## 默认 Logo 规则（MANDATORY）

- 双栏版和单栏版首页默认使用 `https://medbam.org/assets/logo.png` 红色 MedBA logo。
- 遵循图床根目录命名规范，不要为同一 logo 另起自定义文件名。
- 不要在输出 HTML 中引用项目本地 logo 图片；必须使用上述图床 URL，除非用户明确要求离线版本。

## 文章图片图床规则（MANDATORY）

- 最终双栏版和单栏版 HTML 不得引用项目本地图片；禁止 `src="assets/..."`、`src="./assets/..."`、绝对磁盘路径和 `file://...` 图片引用。
- 每篇文章必须在图床 `/assets/{简短标题}/` 下建立独立目录，目录名与第1步确认的简短标题一致。
- Figure 图片文件名遵循图号命名：`Figure 1.png`、`Figure 2.png`、`Figure 3.jpg`；保留源文件实际扩展名，不要散放在图床根目录，不要使用临时文件名。
- HTML 使用公开 URL，并对空格进行 URL 编码：`https://medbam.org/assets/{简短标题}/Figure%201.png`。
- 上传后必须验证 HTTP 200、远程可读权限、远程哈希或尺寸与本地源图一致；未验证通过不得交付。

## 文章主标题大小写规则（MANDATORY）

- **封面主标题（`#article-title`）必须使用 sentence case**：仅大写首词首字母和专有名词，其余词全部小写
- 适用范围：仅限封面上的文章大标题，不涉及章节标题（`h1.section-title`，已有 `text-transform: uppercase`）
- 冒号后首词大写（遵循 AMA 风格），破折号后不大写
- 若原始 Word 标题为全大写（ALL CAPS），**必须人工确认专有名词后再转换**，禁止盲目自动转换

**保留大写的例外情况：**

| 类别 | 示例 |
|------|------|
| 标准基因/蛋白符号 | TP53, BRCA1, EGFR, TGFB1, TIMP1, HIF-1α |
| 数据库/工具名 | TCGA, GEO, KEGG, FAERS, STRING |
| 学术缩写 | miRNA, lncRNA, ceRNA, ssGSEA, LASSO |
| 疾病专有缩写 | ccRCC, NSCLC, HCC |
| 化学/药物缩写 | TKI, PD-L1 |

**示例：**

- ✅ `Identification of TGFB1 and TIMP1 as diagnostic biomarkers in ccRCC through bioinformatics analysis`
- ❌ `Identification of TGFB1 and TIMP1 as Diagnostic Biomarkers in ccRCC Through Bioinformatics Analysis`（Title Case，错误）
- ❌ `IDENTIFICATION OF TGFB1 AND TIMP1 AS DIAGNOSTIC BIOMARKERS IN CCRCC THROUGH BIOINFORMATICS ANALYSIS`（全大写，错误）

## 关键词大小写规则（MANDATORY）

- 首页摘要区 `Keywords:` 标签保留模板写法，后续关键词统一使用逗号加空格分隔
- 每个关键词组的首个单词首字母大写；组内后续普通单词小写，不得把每个关键词组整体做 Title Case
- 双栏版与单栏版必须保持完全一致的关键词文本，不得一处小写、一处 Title Case 或分隔符混排
- 仅在大小写本身承载学术语义时保留原样，例如标准基因符号、数据库缩写、专有名词
- 该规则必须同步双栏、单栏和本地预览，例如 `Cervical cancer, Microarray, Bioinformatics analysis, Differentially expressed mRNAs`
- 若原始 Word 文档的关键词存在大小写混排，生成 HTML 前先完成规范化，再写入模板

**示例：**

- ✅ `Keywords: Cervical cancer, Microarray, Bioinformatics analysis, Differentially expressed mRNAs`
- ✅ `Keywords: Erlotinib, Adverse events, FAERS, Lung cancer, Pancreatic cancer`
- ❌ `Keywords: Cervical Cancer, Microarray, Bioinformatics Analysis, Differentially Expressed mRNAs`
- ❌ `Keywords: erlotinib; adverse events; FAERS; lung cancer; pancreatic cancer`
- ⚠️ 例外场景：`Keywords: TCGA, HIF-1 signaling, TP53`

## 生物医学正文规范（MANDATORY）

- 标准基因符号和蛋白/基因名在正文叙述中按生物医学常规斜体处理，例如 `<em>RRM2</em>`、`<em>TOP2A</em>`；图内文字、数据库原始表头和非正文元数据按来源保留。
- 统计学 `p` 值中的 `p` 使用斜体，格式如 `Logrank <em>p</em>=0.029`；同篇文章内不得混用 `p=...`、`P = ...`、`PValue` 等正文展示格式。表格列名可按原数据保留但需全表一致。
- 正文、摘要、图注和表注中的图表交叉引用必须加粗：`Figure N` / `Table N` 及带字母后缀的 `Figure 1G` 等统一写作 `<strong>Figure N</strong>` / `<strong>Table N</strong>`。多个项目并列时优先逗号，如 `(<strong>Figure 1G</strong>, <strong>Table 2</strong>)`；避免 `(Figure 1G)(Table 2)` 或同篇内分号/逗号混用。
- 学术叙述中避免 `X's team research`、`X team showed` 等口语或中式表达；改为 `X et al. showed/reported/found...`，或去掉作者名直接写研究结论并保留文献引用。
- 连续的短句若表达同一逻辑、且用户指出“合成一段”，应合并为同一段落；合并后重新检查首段/后续段落缩进和分页。

## 摘要标签规则（MANDATORY）

- 摘要正文必须使用四段标准标签：`Background:`、`Methods:`、`Results:`、`Conclusion:`。
- 若原始 Word 使用 `Objective:`、`Aim:`、`Purpose:` 或类似标签，生成前必须规范为 `Background:`；不得在终稿中保留 `Objective:`。
- 双栏版和单栏版摘要标签、冒号、冒号后空格和粗体范围必须完全一致。
- 标签只加粗标签本身和冒号，不得把整段摘要都加粗。

**示例：**

- ✅ `<strong>Background:</strong> Clinical studies indicate ...`
- ❌ `<strong>Objective:</strong> Clinical studies indicate ...`
- ❌ `<strong>Background: Clinical studies indicate ...</strong>`

## 正文文献引用格式规则（MANDATORY）

- 正文文献引用必须统一为方括号格式：`[1]`、`[1,2]`、`[10,11,23]`。
- 引用前可见为一个空格：正确视觉为 `word [1]`，错误为 `word[1]`。
- HTML 输出时必须把正文引用与前一个词绑定为不可断单元，例如 `word<span class="nowrap-cite">&nbsp;[1]</span>`；CSS 必须包含 `.nowrap-cite { white-space: nowrap; }` 或等效规则。
- 引用不得成为视觉行首。若栏宽过窄，应让 `word [1]` 整体自然移到下一行；禁止把 `[1]` 单独留在下一行，也禁止通过拆分/截断前一个英文单词、自动断字、手工 `<br>` 或绝对定位来规避。
- 引用不可断不能牺牲整体美观：若 `word [n]` 绑定后造成某一行词间距异常拉大（例如一行内单词之间出现明显大空洞），必须调整排版而不是接受。优先顺序：轻微调整栏宽/栏距、字号、`word-spacing`、句式顺序、段落承接或页内分页；不得通过拆词、截断单词、自动断字、手工 `<br>`、空白块或绝对定位解决。
- 引用后的英文标点紧跟右方括号：正确为 `word [1].`，错误为 `word [1] .`。句末标点不得放在引用前，正确为 `issues [13].`，错误为 `issues. [13].`。
- 不得保留 Word 导出的上标数字、裸数字引用或孤立数字，如 `<sup>1</sup>`、`condition 1.`、`disease 10,11,23`。
- 范围引用按原文含义保留为逗号分隔或短横范围；不要把多个引用拆成普通正文数字。
- 适用范围：摘要、正文段落、图注、表注中的内文引用；不适用于 References 列表自身的行首编号 `[1]`、`[2]`。

**失败条件：**

- 正文或摘要中残留 `<sup>1</sup>` 这类文献引用上标（作者单位上标除外）。
- 浏览器可见正文出现 `word[1]` 粘连。
- 浏览器可见正文出现 `word 1.`、`word 10,11.` 等裸数字引用。
- Playwright 截图或 DOM Range 检查发现正文/摘要/图表注中的 `[n]`、`[n,m]`、`[10,11,23]` 位于视觉行首，且左侧同一行没有前置正文词。
- 正文出现 `issues. [13].`、`word<br>[1]`、拆词截断、自动断字或手工换行来处理引用换行。
- 为避免引用行首而造成明显夸张词距，截图中可见一行被两端对齐拉散，影响期刊版面美观。

## 摘要区右侧对齐规则（MANDATORY）

- 首页摘要区（`abstract-box` 或同等摘要容器）内所有摘要段落必须使用两端对齐，右侧边缘不得呈明显参差。
- 必须保留段落最后一行自然结束；要求是正文行右侧对齐，不是把每个段落最后一行强行拉满。
- 若摘要区因窄栏、长词、URL 或专业缩写导致 justify 产生异常大词距，优先微调栏宽、字号、字距、句段切分，或只对 URL/DOI 启用换行控制，而不是改回左对齐。
- 禁止对摘要区启用自动断字；不得出现大量行尾短横线。

**CSS 要求：**

```css
.abstract-box,
.abstract-box p {
  text-align: justify;
  text-align-last: left;
  hyphens: none;
  -webkit-hyphens: none;
}

.abstract-box a,
.abstract-box .doi,
.abstract-box .url {
  overflow-wrap: anywhere;
  word-break: break-word;
}
```

**失败条件：**

- 摘要段落计算样式不是 `text-align: justify`
- 摘要段落或正文容器计算样式为 `hyphens: auto` / `-webkit-hyphens: auto`
- 摘要区右侧形成肉眼可见的锯齿边缘
- 普通英文单词被自动插入行尾短横线，或页面出现大量短横线断行
- 为了消除参差而把摘要改成左对齐或居中对齐

## 引号标点规则（MANDATORY）

- **标点符号（逗号、句号）必须放在关闭引号的外面**，不可包含在引号内
- ❌ 错误：`&ldquo;response to hypoxia,&rdquo;`（逗号在引号内）
- ✅ 正确：`&ldquo;response to hypoxia&rdquo;,`（逗号在引号外）
- 适用范围：所有使用 `&ldquo;…&rdquo;` 的学术术语引用

## ORIGINAL ARTICLE 样式

- `ORIGINAL ARTICLE` 所在的 `<div>` 必须使用底部边框线样式：

  ```html
  <div style="font-family:Arial,Helvetica,sans-serif;font-size:10pt;font-weight:bold;letter-spacing:0.06em;text-transform:uppercase;margin-top:2mm;color:#000;border-bottom:1.5pt solid #000;padding-bottom:1mm;display:inline-block;">ORIGINAL ARTICLE</div>
  ```

## 封面间距规则

- 封面间距规则：`ORIGINAL ARTICLE`(mb:8mm) → 标题(mb:5mm) → 作者(mb:7mm) → front-matter(无mb)
- 封面左栏3区块（按顺序）：Affiliations → Correspondence → Funding information，左栏 `border-right: 0.5pt solid #000`
- abstract-box padding 统一为 `4mm`（上下左右均为 `padding:4mm 7mm`）
- body `line-height` 统一为 `1.4`
- 页眉日期格式必须标准化为 `Received: YYYY-MM-DD, Revised: YYYY-MM-DD, Accepted: YYYY-MM-DD`，使用英文逗号分隔，DOI 前用 4em 间距

## 页脚 URL 与页码规则（MANDATORY）

- 双栏分页版页脚必须保留模板结构：`<div class="page-footer">https://medbam.org<span class="page-num">N</span></div>`。
- `.page-num` 必须作为 `.page-footer` 的子元素独立右对齐；CSS 选择器必须是 `.page-footer .page-num`，不得写成 `.page-footer.page-num`。
- 浏览器可见页脚中，URL 保持居中，页码贴右侧；不得出现 `https://medbam.org3`、`https://medbam.org 3` 这类页码跟 URL 拼接的视觉结果。
- Playwright 几何报告必须包含 `footer_page_number_right_aligned` 和 `footer_page_number_appended_to_url`；前者必须为 `true`，后者必须为 `false`。

## 首页 Introduction 双栏行数规则（MANDATORY）

- 首页底部或封面页底部的 Introduction 双栏区必须左右基线对齐，不能出现一栏顶端或底端明显错位。
- 左右两列渲染后的视觉行数必须相等；因此该区域左右列行数之和必须为偶数。
- 验证时必须以浏览器实际渲染为准，用 Playwright/DOM Range 统计视觉行数，不能只按源码换行或字符数估算。
- 若总行数为奇数或左右列行数不等，必须通过以下方式修正：轻微调整栏宽、字号、字距、段落切分点或整体上下位置。不得接受“差一行”的结果，不得启用自动断字来凑行数。
- 首页 Introduction 优先使用固定高度连续 column flow（`column-count:2; column-fill:auto`），使正文按 DOM 顺序先填左栏再填右栏；不得手工把一句或一段拆成左右栏来制造视觉对齐。
- 用户要求首页 Introduction “整体下移/上移”时，只调整该块的 `margin-top` 或等效纵向位置。必须用 Playwright 扫描候选值，确认 `overflow_px = 0`、页脚视觉安全距离 >= 24px、左右栏底部差 <= 2px 后再落地。

**通过标准：**

- 左列行数 = 右列行数
- 左右列第一行基线齐平
- 左右列最后一行基线齐平
- 两列底部到页脚线距离一致，视觉误差不超过 2px
- 首页 Introduction 不压页脚线，不出现底部可见大空白；底部到页脚线视觉安全距离必须 >= 24px，几何报告必须包含 `first_page_intro_flow` 或等效左右栏测量。

## 段落缩进规则（MANDATORY）

- 适用范围：正文内容区的普通正文段落；不适用于摘要、图注、表注、公式、Back Matter 单行说明、参考文献。
- **连续正文段落组必须遵循：首段不缩进，后续段落缩进。**
- “连续正文段落组”指由标题、图、表、公式、跨栏块、分页拆分等边界分隔出来的一组相邻正文段落；每组第一个正文段使用 `class="no-indent"`、`class="first-paragraph"` 或等效 `text-indent:0`。
- 同一段落组内第二段及以后各段使用默认 `<p>`，保持正常首行缩进（`text-indent:1em`）。
- 同一章节或子节跨栏、跨页延续时，仍按逻辑段落组判断：该组第一段不缩进，第二段及以后缩进；例如首页 Introduction 右栏若是同一章节的第二段，必须缩进。
- **每章节（一级标题 `h1.section-title`）后的第一段：顶格（`text-indent:0`）**。
- **每子节（二级标题 `h2.subsection-title`）后的第一段同样顶格**。
- 图、表、公式或跨栏元素之后若重新开始一个新的正文段落组，该组第一段也必须顶格；若只是同一个逻辑段落跨页续排，应保持原段落的缩进状态，不额外添加新缩进。
- ❌ **禁止将 `class="no-indent"` 用于非首段**（常见错误：对连续正文段落批量加 `no-indent`）。
- ❌ **禁止连续多段正文全部顶格**；除非每段都是列表项、Back Matter 单行说明或其他非正文段落。

```html
<!-- ✅ 正确示例 -->
<h1 class="section-title">1 INTRODUCTION</h1>
<p class="no-indent">第一段顶格，无缩进...</p>
<p>第二段正常缩进...</p>
<p>第三段正常缩进...</p>

<h2 class="subsection-title">2.1 Data Source</h2>
<p class="no-indent">子节第一段顶格...</p>
<p>子节第二段正常缩进...</p>

<figure>...</figure>
<p class="no-indent">图后重新开始的正文段落组首段顶格...</p>
<p>图后同组第二段正常缩进...</p>
```

## Back Matter 标准规范（MANDATORY）

**固定顺序9节（含 REFERENCES），全部必须保留标题（即使内容为空）**：

| # | 标题                    | 处理规则                                                                                                                                            |
| - | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | ACKNOWLEDGMENTS         | 从原文提取；无则写 "The authors have no acknowledgements to declare."                                                                               |
| 2 | DATA SHARING STATEMENT  | **固定文本，不从原文提取**："The data included in this study are available on the request from the corresponding author or the first author." |
| 3 | FUNDING                 | 从原文提取；无则写 "Not applicable."                                                                                                                |
| 4 | CONFLICTS OF INTEREST   | **固定文本**："The authors declare that they have no conflicts of interest."                                                                  |
| 5 | ETHICS                  | **固定文本**："Not applicable."                                                                                                               |
| 6 | CONSENT FOR PUBLICATION | **固定文本**："The authors confirm that the work described has not been published before."                                                    |
| 7 | ORCID                   | 有 ORCID 的作者写 `姓名: ORCID号`；若全部无 ORCID，仅写一个 `Not available.`，句末必须有句号                                                                                          |
| 8 | AUTHOR CONTRIBUTION     | 从原文提取；无则留空段落（仍保留标题）                                                                                                              |
| 9 | REFERENCES              | 参考文献列表                                                                                                                                        |

**Back Matter 句末标点规则：**

- Back Matter 中的兜底短句必须带句号，例如 `Not applicable.`、`Not available.`。
- ORCID 若全部无 ORCID，固定写作 `Not available.`，不得写成 `Not available`。
- 真实 ORCID 列表（如 `Author Name: 0000-0000-0000-0000`）按条目展示，不强制在 ORCID 号码后加句号。

**最后一页 References 留白规则：**

- 最后一页因参考文献数量不可控，不要求底部贴齐，也不要求左右栏底部对齐。
- 最后一页必须保持 References 的正常字号、行距、段距且不使用悬挂缩进；不得通过放大 `line-height`、`margin-bottom`、字距、空白段落或透明内容来填满页面。
- 若最后一页存在大留白，应接受自然留白；只有文本溢出、页脚遮挡、页码位置错误、References 行距异常或格式错误时才修复。

**标题名称禁止变体（禁止旧名 → 正确名）**：

| 禁止使用                           | 正确名称               |
| ---------------------------------- | ---------------------- |
| ACKNOWLEDGEMENTS                   | ACKNOWLEDGMENTS        |
| CONFLICT OF INTEREST               | CONFLICTS OF INTEREST  |
| ETHICS STATEMENTS                  | ETHICS                 |
| AVAILABILITY OF DATA AND MATERIALS | DATA SHARING STATEMENT |

**双栏格式 HTML**（`h1.section-title`）：

```html
<h1 class="section-title">ACKNOWLEDGMENTS</h1>
<p class="no-indent">...</p>
```

**单栏格式 HTML**（inline style h1）：

```html
<h1 style="column-span:all;font-family:Arial,Helvetica,sans-serif;font-size:11pt;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;text-align:left;margin-top:12mm;margin-bottom:6mm;border-top:0;padding-top:0;">ACKNOWLEDGMENTS</h1>
<p class="no-indent">...</p>
```

注：所有 back matter 节标题统一使用 `margin-top:12mm;margin-bottom:6mm`，不区分首节和其余节。

**分页规则（双栏）**：

- Back matter 8节优先放在同一页（Conclusion 后）
- 若放不下，允许从任意节标题处开新页
- 节标题不可出现在页底孤行，必须连同段落一起移至下页

## 双栏左栏末行对齐规则（MANDATORY）

双栏布局中，左栏最后一行若内容不足整行宽度，**必须**使用 `text-align-last: justify` 强制两端对齐，避免右侧出现大段空白。

**CSS 实现（必须写入 `.column-left` 或对应左栏样式）**：

```css
/* 双栏左栏末行强制两端对齐 */
.column-left p {
  text-align: justify;
  text-align-last: justify;
}
```

- **适用范围**：双栏分页版（`template-two-column.html`）左栏**强制启用**
- **浏览器兼容**：所有现代浏览器均支持 `text-align-last`

## MathJax SVG 数学公式排版规则（MANDATORY）

所有数学公式**必须**使用 MathJax 库渲染为 SVG 格式，禁止使用 MathML 原生标签、CSS hack（如 `border-top` 模拟根号横线）或 `<sup>` 标签模拟上标。

**MathJax SVG 优势**：

- 跨浏览器一致渲染（包括旧版浏览器）
- 高质量矢量输出，缩放不失真
- 支持完整 LaTeX 语法
- 自动处理符号间距和对齐

**引入 MathJax（必须添加到 `<head>` 区域）**：

```html
<script>
MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
```

**LaTeX 语法速查**：

| 语法            | 用途                 | 示例                      |
| --------------- | -------------------- | ------------------------- |
| `\( ... \)`   | 行内公式             | `\( x^2 + y^2 = z^2 \)` |
| `\[ ... \]`   | 块级公式（居中显示） | `\[ E = mc^2 \]`        |
| `^{}`         | 上标                 | `x^{2}` → x²          |
| `_{}`         | 下标                 | `x_{1}` → x₁          |
| `\frac{a}{b}` | 分数                 | `\frac{1}{2}` → ½     |
| `\sqrt{}`     | 根号                 | `\sqrt{x}` → √x       |
| `\sqrt[n]{}`  | n次根号              | `\sqrt[3]{x}` → ∛x    |
| `\sum`        | 求和符号             | `\sum_{i=1}^{n}`        |
| `\int`        | 积分符号             | `\int_{0}^{\infty}`     |
| `\lim`        | 极限                 | `\lim_{x \to 0}`        |
| `\overline{}` | 上划线               | `\overline{x}` → x̄   |
| `\text{}`     | 公式内普通文本       | `\text{其中}`           |

**完整示例 — 二次公式**：

行内写法：

```html
<p>二次方程的解为 \( x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \)</p>
```

块级写法：

```html
\[
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\]
```

**注意事项**：

- MathJax 脚本必须放在 `<head>` 中，且配置对象必须在脚本引入之前定义
- 使用 `async` 属性异步加载，不阻塞页面渲染
- SVG 输出可直接导出为高清图片（右键另存）
- 复杂公式可使用在线 LaTeX 编辑器预览后复制

## 参考文献缩进规则

- **正文段落**：不使用悬挂缩进，仅使用首行缩进（见上方段落缩进规则）
- **参考文献区域（`.references div`）**：❌ **不使用悬挂缩进**，所有行齐左对齐
  - 正确：`.references div { margin-bottom: 2mm; }`（无 `padding-left` 或 `text-indent`）
  - ❌ 禁止：`padding-left: 1.27cm; text-indent: -1.27cm;`（会导致 PubMed 链接行双重缩进）

## 表格跨栏规则（仅适用于双栏模板）

> 此规则**仅适用于 `template-two-column.html`（双栏分页版）**，单栏模板无需处理表格跨栏。

- **≤ 3 列的表格**：不跨栏，使用 `class="table-wrapper no-span"`（在单栏内显示）
- **> 3 列的表格**：跨栏，使用 `class="table-wrapper"`（默认，column-span:all）

```html
<!-- ✅ ≤3列：不跨栏（双栏模板） -->
<div class="table-wrapper no-span" id="tbl-1">
  <table>...</table>   <!-- 3列或更少 -->
</div>

<!-- ✅ >3列：跨栏（双栏模板） -->
<div class="table-wrapper" id="tbl-2">
  <table>...</table>   <!-- 4列或更多 -->
</div>
```

## 表格跨页续表规则（双栏分页版）

当表格行数过多无法在一页内完整显示时，需跨页分割并遵循以下规则：

| 规则     | 说明                                                        |
| -------- | ----------------------------------------------------------- |
| 前页底线 | 细线 `border-bottom: 0.75pt solid #000`（表示表格未结束） |
| 续页顶线 | 粗线 `border-top: 1.5pt solid #000`（标识续表起始）       |
| 续页表题 | 保留 Table N (Continued)，不重复完整表题                    |
| 续页表头 | 重复 `<thead>` 横表头（含单位注），保证每页可独立阅读     |
| 表号     | 不重复，仅在首页出现完整表题                                |
| 表身     | 列对齐一致，不插入正文，栏线齐                              |

**HTML 示例：**

```html
<!-- 前页：Table N Part 1 -->
<table style="font-size:7pt;line-height:1.3;border-bottom:0.75pt solid #000;">
    <thead><tr><th>...</th></tr></thead>
    <tbody><!-- 前半部分行 --></tbody>
</table>

<!-- 续页：Table N Part 2 -->
<div class="table-caption"><span class="tbl-label">Table N</span> (Continued)</div>
<table style="font-size:7pt;line-height:1.3;border-top:1.5pt solid #000;">
    <thead><tr><th>...</th></tr></thead>
    <tbody><!-- 后半部分行 --></tbody>
</table>
```

**线宽规范：粗线 1.5pt，细线 0.75pt**

## 表格视觉比例与填空禁令（MANDATORY）

- 正文表格必须保持期刊三线表的自然比例：表头、正文行和表题不能被明显拉高；不得用异常 `line-height`、大 `td/th` padding、空白行或透明内容填补页底空白。
- 表头大小写和列对齐必须统一：普通英文表头使用一致的首字母大写或期刊指定写法；数值列默认居中或按小数点/单位一致对齐；同一表内不得一列左偏、一列居中混乱。
- 表格必须按视觉阅读顺序递增：`Table 1`、`Table 2`、`Table 3` 等不得乱序。DOM 中存在但视觉上被挪到前后页、页脚下方或裁切区，均视为失败。
- 2-3 行的小表若并排导致拥挤、标题压缩或左右栏不齐，可改为跨栏横向三线表；跨栏后仍必须保留正常表题、自然行高和编号顺序，并用 Playwright 确认 `overflow_px = 0`、表注完整可见。
- 小表格或 2-3 行表格尤其不得承担整页填空任务。若页底有空白，优先调整内容分页、正文段间距、块间距或 S 型灌版；表格 padding 只能在视觉正常范围内微调。
- 表格行高或单元格 padding 调整后，必须查看截图并记录 Playwright 几何结果；若用户能肉眼指出“拉得太大/夸张”，必须回退表格拉伸，改用其他方式平衡页面。
- 表格仍必须只保留三线表：顶线、表头下线、底线；不得因为调整高度而添加额外横线、竖线、斑马纹或网格。

## 布局模式：强制 S 型灌版（MANDATORY）

- **✅ 强制使用 S 型布局**：页面内容必须按 DOM 顺序先填满左栏（左上 → 左下），再填右栏（右上 → 右下）。这条规则优先级高于章节标题、图片和表格的局部摆放偏好。
- **✅ 固定高度双栏容器必须使用 `column-fill:auto`**，让浏览器顺序填充栏位；禁止使用会把内容上下均衡到两栏的 `column-fill:balance` 作为正文分页主策略。
- **✅ 正文文字优先使用连续流**：普通正文、章节标题、小节标题应尽量放入同一个固定高度 column 容器中，避免手工左右栏切分。只有并排图、跨栏宽表、Back Matter、参考文献等结构化块确实需要独立控制时，才允许显式左右栏。
- **✅ 显式左右栏必须实测对齐**：若使用 `.column-left/.column-right`、CSS grid 或类似容器，必须输出宽度、顶部和底部差值。宽度差 > 1px、顶部差 > 4px 或底部差 > 13px 时 CP3 失败；首页 Introduction 底部差 > 2px 时 CP3 失败。
- **✅ S 型优先于小节标题对齐**：用户要求 `3.1` 与 `3.2`、Back Matter 标题或两栏标题“左右对齐”时，不能把正文改成横向阅读网格。若标题同高与 S 型连续灌版冲突，必须优先保持 S 型，再通过页内容量、跨栏表格、块间距或下一页承接来处理底部。
- **❌ 禁止标题截断**：`h1.section-title`、`h2.subsection-title` 不得因为是新章节而提前跳到右栏顶部；若左栏仍有空间，标题和后续正文必须继续留在左栏。
- **❌ 禁止图表截断 S 流**：图片、表格可以按模板跨栏或续表，但不得导致后续章节提前进入右栏、左栏留大空白，或出现“左栏未满、右栏已开始新章节”的布局。
- **❌ 禁止手工用空白、spacer、透明块、绝对定位、`break-before: column`、`break-after: column`、额外 wrapper 或人为拆页来制造章节右栏起始效果。**
- **❌ 禁止在多栏正文流内放空 `div` 下压某一栏**：这会制造隐藏横向溢出或第三列。需要微调 Back Matter 标题时，只能给目标标题/目标块添加局部 class 与 margin，并用 computed style 和几何指标确认规则确实生效。
- **⚠️ 跨栏图表页例外必须补验**：跨栏 Figure/Table、宽表、整版图页会让自动 `s_flow` 检测跳过部分栏判断；此时必须逐页查看截图，确认不存在图注缺失、页底大空白、正文衔接断裂、References 条目隐藏等问题。

## 四文件同步规则（MANDATORY）

每次修改正文、摘要、关键词、图表、图注、References、分页或样式后，必须同步以下文件（若存在）：

- 双栏正式版：`two-column-{short-title}.html`
- 双栏本地预览：`two-column-{short-title}-local-preview.html`
- 单栏正式版：`single-column-{short-title}.html`
- 单栏本地预览：`single-column-{short-title}-local-preview.html`

同步后必须做残留文本扫描，确认旧写法没有只残留在某一个版本中；尤其检查关键词大小写、正文 Figure/Table 交叉引用是否加粗、Figure/Table 标点、基因斜体、`p` 值、References 正文和图注句末标点。

**CSS 基线：**

```css
.page-content.two-column {
  column-count: 2;
  column-gap: var(--column-gap);
  column-fill: auto;
  height: var(--content-height);
}
```

**失败条件：**

- 右栏出现新标题时，左栏底部仍有可容纳正文的明显空白
- 章节标题、图片或表格导致 DOM 顺序后的内容跳过左栏直接进入右栏
- 页面视觉顺序变成“左上 → 右上 → 左下 → 右下”的横向排布，而不是“左上 → 左下 → 右上 → 右下”的 S 型排布
- 通过手工断行、空白块、异常表格高度或绝对定位制造的“对齐”
- 为了让两栏标题同高而把连续正文拆成左右两个独立栏，导致左栏未填满或右栏提前开始

## 图片尺寸调整安全规则（MANDATORY）

- 调整 Figure 大小时必须做小步扫描或二分搜索，不得凭肉眼一次性拉大或缩小。
- 每次调整必须记录：原始 `max-height`/宽度、候选值、失败值、最终值、失败原因（如 `overflow_px > 0`、图注被裁、页脚遮挡、左右栏底部差变大）。
- 最终只能采用同时满足以下条件的最大安全尺寸：`overflow_px = 0`、`overflow_x_px = 0`、图注完整可见、页底留白未超过阈值、左右栏底部对齐未被破坏。
- 若用户指出“图片调大以减少底部留白”，先扫描图片尺寸上限；若最大安全尺寸仍无法消除留白，再调整内容分页或块间距，不得继续放大到溢出。

**封面页底部 Introduction 特例（仅限首页，必须实测）**：

封面页底部迷你双栏区（通常只有1-2段 Introduction 内容）必须特别处理，否则两栏底部容易不齐。该特例只允许用于首页 Introduction 的等行与页脚安全距离处理，不能扩展为普通正文的章节截断方式：

1. 给封面页的这个 `h1` 加 `style="column-span:all;"` 内联覆盖（只覆盖这一处）
2. 正文使用固定高度连续 flow（`column-count:2; column-fill:auto; height:...`），让浏览器按 DOM 顺序先左栏后右栏
3. 若需调整视觉位置，只改整块 `margin-top`、容器高度、字号或栏距，并用 Playwright 扫描候选值
4. 禁止用 `column-fill:balance`、手工断句、空白块或绝对定位制造等高

```html
<div class="two-column" style="margin-top:6mm;">
    <h1 class="section-title" style="column-span:all;">1 INTRODUCTION</h1>
    <div class="first-page-introduction-flow" style="column-count:2;column-fill:auto;height:44mm;">
        <p class="no-indent">正文按 DOM 顺序连续流入左栏，然后进入右栏...</p>
        <p>同一逻辑段落组的后续段落保持缩进...</p>
    </div>
</div>
```

> 判断规则和根因分析详见 pagination-rules.md § CP 3检查点：验证无溢出/留白、S 型灌版、摘要对齐、Introduction 等行且图注底部对齐

## 参考文献续页规则（MANDATORY）

- References 跨页时不得自动输出 `REFERENCES (CONTINUED)` 或类似续页标题，除非用户或目标期刊模板明确要求。
- 参考文献续页直接接上一页的序号继续排版，保持同一 `.references` 样式和编号顺序。
- `Table N (Continued)` 只适用于同一表格跨页拆分，不得套用到 References、Back Matter 或普通章节。

> 双栏底部对齐（flush bottom）的完整工作流参见 pagination-rules.md § 8
