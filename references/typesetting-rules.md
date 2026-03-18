# 正文排版细节规则（MANDATORY）

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

## 正文 URL 处理规则（MANDATORY）

- **正文中出现的所有 URL 必须包裹 `<a>` 标签**（`<a href="..." target="_blank">URL</a>`），禁止裸文本 URL
- 原因：`<a>` 标签已有 `overflow-wrap: anywhere; word-break: break-word;` 样式，允许 URL 在任意位置断行，避免 `text-align: justify` 在窄栏中产生巨大词间空白
- **双栏 `.two-column` 必须设置** `overflow-wrap: anywhere; hyphens: auto; -webkit-hyphens: auto;`，允许在音节处断词，进一步消除 justify 空白
- 适用范围：所有正文段落中的数据库链接、工具网址等

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

- 首页摘要区 `Keywords:` 标签保留模板写法，后续关键词统一使用分号加空格分隔
- 普通主题词统一使用小写
- 双栏版与单栏版必须保持完全一致的关键词文本，不得一处小写、一处 Title Case
- 仅在大小写本身承载学术语义时保留原样，例如标准基因符号、数据库缩写、专有名词
- 若原始 Word 文档的关键词存在大小写混排，生成 HTML 前先完成规范化，再写入模板

**示例：**

- ✅ `Keywords: erlotinib; adverse events; FAERS; lung cancer; pancreatic cancer`
- ❌ `Keywords: Erlotinib, Adverse Events, FAERS, Lung Cancer, Pancreatic Cancer`
- ⚠️ 例外场景：`Keywords: tcga; hif-1 signaling; TP53`

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

## 段落缩进规则

- **每章节（一级标题 h1.section-title）后的第一段：顶格（text-indent:0）**，使用 `class="no-indent"` 或 `class="first-paragraph"`
- 同一章节内的第二段及以后各段：正常首行缩进（`text-indent:1em`，即默认 `<p>`）
- **每子节（二级标题 h2.subsection-title）后的第一段同样顶格**
- ❌ **禁止将 `class="no-indent"` 用于非首段**（常见错误：对连续段落批量加 `no-indent`）

```html
<!-- ✅ 正确示例 -->
<h1 class="section-title">1 INTRODUCTION</h1>
<p class="no-indent">第一段顶格，无缩进...</p>
<p>第二段正常缩进...</p>
<p>第三段正常缩进...</p>

<h2 class="subsection-title">2.1 Data Source</h2>
<p class="no-indent">子节第一段顶格...</p>
<p>子节第二段正常缩进...</p>
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
| 7 | ORCID                   | 有 ORCID 的作者写 `姓名: ORCID号`；若全部无 ORCID，仅写一个 `Not available` 即可                                                                                          |
| 8 | AUTHOR CONTRIBUTION     | 从原文提取；无则留空段落（仍保留标题）                                                                                                              |
| 9 | REFERENCES              | 参考文献列表                                                                                                                                        |

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

## 参考文献悬挂缩进规则

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

## 布局模式：强制蛇形（MANDATORY）

- **✅ 强制使用（蛇形布局）**：`h1.section-title` 无 `column-span`，内容连续蛇形流动，适合学术论文线性阅读。**所有排版必须使用蛇形布局，禁止切换为其他布局。**
- **❌ 禁止使用（跨栏标题布局）**：禁止将 `column-span:all` 应用于 `h1.section-title`，禁止使用 `column-fill:auto`，禁止以任何形式切换为跨栏标题布局。

**封面页底部特例（蛇形布局时必须处理）**：

封面页底部迷你双栏区（通常只有1-2段 Introduction 内容）在蛇形模式下必须特别处理，否则两栏底部不齐：

1. 给封面页的这个 `h1` 加 `style="column-span:all;"` 内联覆盖（只覆盖这一处）
2. 将长段拆为两段（在语义切分点），让 CSS balance 各自放一栏

```html
<div class="two-column" style="margin-top:6mm;">
    <h1 class="section-title" style="column-span:all;">1 INTRODUCTION</h1>
    <p class="no-indent">第一组句子（约5行）...</p>   <!-- → 左栏 -->
    <p>第二组句子（约5行）...</p>                     <!-- → 右栏 -->
</div>
```

> 判断规则和根因分析详见 pagination-rules.md § 蛇形双栏布局 § 封面页底部特例处理

> 双栏底部对齐（flush bottom）的完整工作流参见 pagination-rules.md § 8
