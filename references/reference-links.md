# 参考文献链接生成指南

本文档说明如何为参考文献添加元数据链接（PubMed | Google Scholar | Crossref）。

## 链接类型

### 1. PubMed 链接

**URL格式**: `https://pubmed.ncbi.nlm.nih.gov/{PMID}/`

**获取方法**:
1. 使用 NCBI E-utilities API 通过标题搜索
2. API端点: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
3. 参数: `db=pubmed&term={title}[Title]&retmode=json`

**示例**:
```
原始参考文献: Ferlay J, et al. Estimates of worldwide burden of cancer in 2008...
搜索查询: Estimates of worldwide burden of cancer in 2008[Title]
返回PMID: 21351269
最终URL: https://pubmed.ncbi.nlm.nih.gov/21351269/
```

**特殊处理**:
- 如果搜索返回多个结果，比较标题相似度（>80%才使用）
- 如果没有找到匹配，不添加PubMed链接
- 中文参考文献可能没有PubMed记录

### 2. Google Scholar 链接

**URL格式**: `https://scholar.google.com/scholar?q={encoded_title}`

**生成方法**:
1. 提取参考文献标题
2. URL编码标题
3. 构造搜索URL

**示例**:
```
标题: Estimates of worldwide burden of cancer in 2008
编码后: Estimates+of+worldwide+burden+of+cancer+in+2008
URL: https://scholar.google.com/scholar?q=Estimates+of+worldwide+burden+of+cancer+in+2008
```

**注意**: 
- Google Scholar链接总是可以生成（搜索链接）
- 不需要验证，因为是搜索而非直接链接
- 中文标题也支持

### 3. Crossref/DOI 链接

**URL格式**: `https://doi.org/{DOI}`

**获取方法**:

**方式A - 参考文献中已有DOI**:
1. 使用正则表达式提取: `10\.\d{4,}/[^\s]+`
2. 直接构造URL

**方式B - 通过Crossref API搜索**:
1. API端点: `https://api.crossref.org/works`
2. 参数: `?query.title={title}&rows=1`
3. 从返回结果中提取DOI

**示例**:
```
参考文献中DOI: 10.1002/ijc.25516
最终URL: https://doi.org/10.1002/ijc.25516
```

## 链接验证协议

### HTTP响应处理

| 响应码 | 分类 | 处理 |
|--------|------|------|
| 200 OK | 有效 | 使用链接 |
| 301/302 重定向 | 有效 | 跟随重定向，使用最终URL |
| 403 Forbidden | 无效 | 跳过此链接类型 |
| 404 Not Found | 无效 | 跳过此链接类型 |
| 429 Too Many Requests | 重试 | 等待2秒后重试一次 |
| 超时(>5秒) | 无效 | 跳过此链接类型 |

### 速率限制

- 最大并发请求: 3个
- 请求批次间隔: 500ms
- User-Agent: `MedBA-Journal-Typesetter/1.0`

## HTML输出格式

```html
<div style="margin-bottom:2mm;padding-left:0;text-indent:0;font-size:8pt;line-height:1.3;">
  [1] Surname AB, Surname CD, Surname EF, et al. Article title. J Abbrev. Year;Volume(Issue):Pages.<br>
  <a href="https://pubmed.ncbi.nlm.nih.gov/12345678/" target="_blank" style="color:#005a8c;text-decoration:none;">PubMed</a> | 
  <a href="https://scholar.google.com/scholar?q=Article+Title" target="_blank" style="color:#005a8c;text-decoration:none;">Google Scholar</a> | 
  <a href="https://doi.org/10.xxxx/xxxxx" target="_blank" style="color:#005a8c;text-decoration:none;">Crossref</a>
</div>
```

## 参考文献正文格式规范（MANDATORY）

参考文献正文不得直接沿用 Word 原稿中的混杂格式。添加 PubMed / Google Scholar / Crossref 链接前，必须先把每条参考文献统一为期刊 Vancouver 风格。此步骤是正文规范化，不是简单给原文追加链接。

**统一格式：**

```text
[n] Authors. Title. Journal. Year;Volume(Issue):Pages/article-number.
```

**标准示例：**

```text
[1] Gaffney DK, Hashibe M, Kepka D, Maurer KA, Werner TL. Too many women are dying from cervix cancer: problems and solutions. Gynecol Oncol. 2018;151(3):547-554.
[2] Goodman A. HPV testing as a screen for cervical cancer. BMJ. 2015;350:h2372.
[3] Dennis G Jr, Sherman BT, Hosack DA, et al. DAVID: database for annotation, visualization, and integrated discovery. Genome Biol. 2003;4(9):R60.
```

**作者格式：**

- 作者写作 `Surname Initials`，多个作者用逗号分隔。
- 达到原稿或期刊规则要求使用 `et al.` 时，全篇保持同一策略；本刊统一采用“超过 3 位作者时列前 3 位后加 `et al.`，3 位及以下全部列出”。
- 不得同一列表中混用 `Lastname F.`, `Lastname F`, `Lastname, F.` 等不同作者格式。
- 不得保留 APA 风格作者格式、`&`、`and` 夹在作者列表中、作者名倒置错误或首字母中间点混排。

**题名格式：**

- 题名使用 sentence case；仅首词、专有名词、缩写和标准术语保留大写。
- 不得把原稿中的随机 Title Case、全大写或大小写混排直接带入终稿。
- 删除非题名内容和装饰符号，如 `☆`、`[J]`、多余句点、数据库导出标记；保留基因符号、数据库名和标准缩写的规范大小写。

**期刊名格式：**

- 期刊名必须全篇一致使用规范缩写或目标期刊指定写法。
- 常见缩写示例：`BMJ`、`Nat Rev Gastroenterol Hepatol`、`JAMA Netw Open`、`Int J Epidemiol`。
- 不得出现 `Bmj`、`Nature reviews Gastroenterology & hepatology` 这类大小写或全称/缩写混杂。
- 优先使用 PubMed/NLM 或 Crossref 给出的期刊缩写；无法确认时使用全篇一致的期刊通用缩写，不要同一列表内混用全称和缩写。

**年份卷页格式：**

- 使用 `Year;Volume(Issue):Pages.`，如 `2020;324(24):2565-2574.`；无期号时使用 `Year;Volume:Pages.`。
- 缺卷、期、页码或文章号时，必须先查询 PubMed、Crossref、DOI resolver 或出版社页面补齐；不能把原稿的缺失字段原样带入终稿。
- 电子期刊没有传统页码时，使用文章号或电子页码作为页码位，如 `2015;350:h2372.`、`2016;27(4):e43.`、`2003;4(9):R60.`、`2020;20(1):587.`。
- 若来源只可高置信确认年份和卷号，无法确认页码/文章号，则保留最完整可核验信息并在最终报告列明该条“无法补齐页码/文章号”的原因。

**DOI 与正文关系：**

- DOI 不属于双栏 PDF 版 References 正文的必填展示字段；单栏版可通过 Crossref 链接承载 DOI。
- 若目标期刊或用户明确要求 DOI 入正文，统一写作 `doi: 10.xxxx/xxxxx.`，不得混用 `DOI:`、`https://doi.org/...` 和裸 DOI 多种格式。
- 禁止臆造 DOI/PMID；只有标题、年份、首作者和期刊能高置信匹配时才写入 DOI/PubMed 链接。

**双栏/单栏一致性：**

- 双栏版和单栏版的 References 正文必须逐条一致。
- 单栏连续版仅在同一条 Vancouver 正文后追加 `PubMed | Google Scholar | Crossref` 链接。
- 本地预览文件若存在，也必须同步同一套参考文献正文，避免预览版与终稿不一致。
- 双栏分页版拆分 References 后必须保留编号严格递增且连续，不得出现 `[22] [21] [20] [23]` 这类重排错误。
- 验证 References 时必须同时检查 DOM 和可视区：每条参考文献不仅要存在于 HTML 中，还必须通过 Playwright 截图或元素边界测量确认没有被分页容器、`overflow:hidden` 或页脚裁切隐藏。

**禁止：**

- ❌ 直接输出 Word 原文参考文献。
- ❌ 同一 References 中作者格式、题名大小写、期刊缩写风格、年份卷页标点不一致。
- ❌ 在双栏版和单栏版使用不同参考文献正文。
- ❌ 把缺页码、缺卷号、错误年份或错误期刊名当作“原文如此”直接保留。
- ❌ 低置信 Crossref/PubMed 命中后仍强行补 DOI、PMID 或页码。

## 参考文献规范化流程（MANDATORY）

1. 从原稿提取参考文献总数和原始文本，保留编号顺序。
2. 对每条参考文献抽取标题、首作者、年份、期刊、卷期页、DOI。
3. 优先用 DOI 或 PubMed 精确匹配；无 DOI 时用标题 + 首作者 + 年份在 PubMed/Crossref 检索。
4. 只有标题相似度 >= 80%、年份一致或可解释、首作者/期刊基本一致时，才使用检索结果补全 DOI、PMID、期刊缩写、卷期页码或文章号。
5. 将正文统一改写为 Vancouver：作者、题名、期刊缩写、年份卷期页、句点。
6. 对双栏、单栏、本地预览全部写入同一套正文；单栏再追加可用链接。
7. 双栏分页后检查每条 References 的编号顺序和可见性，确认编号连续递增且每条真实显示在页面可视区内。
8. 最终报告必须记录：参考文献总数、已补齐页码/文章号的条目、Google Scholar/PubMed/Crossref 链接数、跳过 DOI/PMID 的原因、References 编号连续性和可见性检查结果。

## 缺失链接处理

只显示可用的链接，缺失的不显示分隔符:

```html
<!-- 只有PubMed和Google Scholar -->
<a href="...">PubMed</a> | <a href="...">Google Scholar</a>

<!-- 只有Google Scholar -->
<a href="...">Google Scholar</a>

<!-- 只有Crossref -->
<a href="...">Crossref</a>
```

## 中文参考文献

- PubMed: 中文文献通常无记录，跳过
- Google Scholar: 使用中文标题搜索，正常生成
- Crossref: 如有DOI则使用，否则跳过
---

## 🔧 详细实现逻辑（从 SKILL.md 第5步提取）

以下内容从 SKILL.md 步骤5完整提取，提供参考文献链接生成的具体实现细节。

### 步骤5.1：提取已有 DOI（本地处理）

```python
import re

def extract_doi(reference_text):
    """从参考文献中提取DOI"""
    doi_pattern = r'10\.\d{4,}/[^\s\]\)]+'
    match = re.search(doi_pattern, reference_text)
    return match.group(0) if match else None

# 示例
ref = "Dixon S, et al. Cell, 2012,149(5). DOI:10.1016/j.cell.2012.03.042."
doi = extract_doi(ref)  # "10.1016/j.cell.2012.03.042"
```

**已有 DOI 的参考文献**：

- ✅ 直接生成 Crossref 链接：`https://doi.org/{DOI}`
- ✅ 无需 MCP 验证

### 步骤5.2：PubMed 查询（使用 MCP）

**仅当 `mcp_pubmed_available == True` 时执行**

**策略 A：有 DOI 的文献**

```python
# 通过DOI搜索（精确度高）
result = pubmed_search_pubmed_advanced(
    term=doi,  # 使用DOI作为搜索词
    num_results=1
)
```

**策略 B：无 DOI 的文献**

```python
# 通过标题+作者搜索
result = pubmed_search_pubmed_advanced(
    title=extracted_title,
    author=first_author,  # 可选
    num_results=3  # 返回多个结果进行匹配验证
)

# 验证匹配度
for article in result:
    similarity = calculate_title_similarity(extracted_title, article['title'])
    if similarity > 0.8:  # 80%相似度阈值
        pmid = article['pmid']
        break
```

**超时/失败处理**：

- ⏱️ 超时（>10秒）→ 记录警告，跳过该文献的 PubMed 链接
- ❌ 无结果 → 跳过 PubMed 链接
- ⚠️ 低置信度匹配 → 跳过，不添加链接

### 步骤5.3：Crossref 查询（使用 MCP）

**仅当 `mcp_crossref_available == True` 且文献无 DOI 时执行**

```python
# 通过标题搜索DOI
result = crossref_search_works_by_query(
    query=extracted_title,
    limit=3  # 限制返回结果数
)

# 验证匹配度
for work in result.get("message", {}).get("items", []):
    title_match = calculate_title_similarity(extracted_title, work.get('title', [''])[0])
    year_match = check_year_consistency(reference_year, work.get('published-print', {}).get('date-parts', [[None]])[0][0])
  
    if title_match > 0.8 and year_match:
        doi = work['DOI']
        break
```

**硬约束**：

- ❌ 禁止臆造 DOI/PMID
- ❌ 低置信度匹配（<80%）必须跳过
- 📝 每次 MCP 调用失败必须记录日志

### 步骤5.4：生成 Google Scholar 链接（总是执行）

```python
import urllib.parse

def generate_scholar_link(reference_text):
    """生成Google Scholar搜索链接"""
    # 提取标题或使用全文
    title = extract_title(reference_text) or reference_text[:100]
    encoded = urllib.parse.quote(title)
    return f"https://scholar.google.com/scholar?q={encoded}"
```

**无需验证，总是可以生成**

### 链接输出格式

#### 双栏分页版（纯 Vancouver 正文，无元数据行）

```html
<!-- 有 DOI 的参考文献；双栏正文仍保持纯 Vancouver 文本 -->
<div>[1] Ferlay J, Shin HR, Bray F, Forman D, Mathers C, Parkin DM. Estimates of worldwide burden of cancer in 2008: GLOBOCAN 2008. Int J Cancer. 2010;127(12):2893-2917.</div>

<!-- 电子文章号 -->
<div>[2] Goodman A. HPV testing as a screen for cervical cancer. BMJ. 2015;350:h2372.</div>
```

**规则：**
- ✅ 双栏版 References 正文只输出统一后的 Vancouver 文本，优先保证 PDF 排版稳定。
- ✅ 有 DOI 的条目不需要在双栏正文重复写 DOI；DOI 通过单栏 Crossref 链接承载。
- ❌ 双栏版不添加 PubMed/Scholar/Crossref 元数据行。
- ❌ 不把未核验 DOI、PMID 或检索链接塞入双栏正文。

#### 单栏连续版（同一 Vancouver 正文 + 元数据行）

```html
<div style="margin-bottom:2.5mm;padding-left:0;text-indent:0;">
  [1] Ferlay J, Shin HR, Bray F, Forman D, Mathers C, Parkin DM. Estimates of worldwide burden of cancer in 2008: GLOBOCAN 2008. Int J Cancer. 2010;127(12):2893-2917.<br>
  <a href="https://pubmed.ncbi.nlm.nih.gov/21351269/" target="_blank" style="color:#005a8c;text-decoration:none;">PubMed</a> |
  <a href="https://scholar.google.com/scholar?q=Ferlay+GLOBOCAN+cancer+2008" target="_blank" style="color:#005a8c;text-decoration:none;">Google Scholar</a> |
  <a href="https://doi.org/10.1002/ijc.25516" target="_blank" style="color:#005a8c;text-decoration:none;">Crossref</a>
</div>
```

**规则：**
- ✅ 单栏版参考文献正文与双栏版逐条一致。
- ✅ 元数据链接（PubMed | Google Scholar | Crossref）在下一行显示。
- ✅ 只显示可用的链接，缺失的不显示

### 第5.5步：链接批量验证（使用 verify_links. Py 脚本）

#### 脚本位置

`scripts/verify_links.py`

#### 使用场景

- 批量验证生成的所有参考文献链接是否可访问
- 调试链接验证失败问题
- 手动验证特定 DOI 或 PMID

#### 命令示例

```bash
# 验证特定PubMed ID是否有效
python scripts/verify_links.py --test-pubmed 21351269

# 验证特定DOI是否有效
python scripts/verify_links.py --test-doi "10.1002/ijc.25516"

# 通过标题搜索PubMed获取PMID
python scripts/verify_links.py --search-pubmed "Estimates of worldwide burden of cancer"

# 生成Google Scholar搜索URL
python scripts/verify_links.py --generate-scholar "Ferroptosis cell death mechanisms"

# 以JSON格式输出（便于程序处理）
python scripts/verify_links.py --test-pubmed 21351269 --json
```

#### 输出格式

```
PubMed 21351269: VALID (valid, HTTP 200)
URL: https://pubmed.ncbi.nlm.nih.gov/21351269/

DOI 10.1002/ijc.25516: VALID (valid, HTTP 200)
URL: https://doi.org/10.1002/ijc.25516
Title: Estimates of worldwide burden of cancer in 2008

Found PMID: 21351269
URL: https://pubmed.ncbi.nlm.nih.gov/21351269/

Google Scholar URL: https://scholar.google.com/scholar?q=Ferroptosis+cell+death+mechanisms
```

#### 批量验证所有生成的链接：

```python
# 示例：批量验证所有PubMed链接
for pmid in collected_pmids:
    result = bash(command=f"python scripts/verify_links.py --test-pubmed {pmid} --json")
    data = json.loads(result)
    if not data[0]["valid"]:
        print(f"⚠️ PubMed {pmid} 验证失败: {data[0]['status']}")
```
