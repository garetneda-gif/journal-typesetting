# 分页规则参考文档

> 结构说明：本文件保留深分页算法、Playwright 示例和失败处理细节；CP0-CP5 摘要、S 型门控和截图/rect 检查入口见 `layout-gates.md`。


> 从 SKILL.md 提取的分页核心内容（核心原则、人机协同流程、失败根因分析、内容分析、HTML模板、分割策略、大图处理、验证检查点）

---

## 分页核心原则 (CRITICAL - 必须严格执行)

> **分页时绝对不能溢出；非最后页不得出现超阈值留白，且不得为消除留白破坏期刊视觉比例。**

**分页规则:**

- 封面页：不必独立成页——若封面/摘要区域底部有剩余空间，**必须**将 Introduction 等正文内容接续填入，直至页面填满，**摘要页底部绝对不允许留白**。例外：若摘要本身内容过长已占满整个摘要页，则允许 Introduction 另起新页。
- 正文页：每页约800-1000字；允许孤行（orphan）和寡行（widow），非最后页必须尽量贴近页脚安全线，不能出现可见大空白
- **禁止溢出**：内容绝不能超出页面边界
- **页底留白阈值**：非最后页 `whitespace_px < 30px` 为 PASS，`30px <= whitespace_px < 57px` 为 WARNING，`whitespace_px >= 57px` 为 FAILURE；最后一页参考文献数量不可控，可放宽
- **页脚页码规则**：页脚 URL 必须保持居中，页码必须使用 `.page-footer .page-num` 独立右对齐；不得写成 `.page-footer.page-num`，不得让可见文本拼接为 `https://medbam.org3`。
- **最后一页规则**：最后一页不要求贴底或左右栏底部对齐，但 References 必须保持正常字号、行距和段距；禁止为了贴底拉大 References 行距、段距、字距或插入空白块。
- **可见内容规则**：验证不能只检查 DOM。所有 Figure/Table 图注和 References 条目必须真实出现在页面可视区内；若元素存在于 DOM 但被 `overflow:hidden`、固定高度容器、跨栏图或页脚裁切隐藏，视为 CP3 FAILURE。
- **跨栏块规则**：含跨栏图、宽表或结构化块的页面即使自动 `s_flow` 检测被 SKIPPED，也必须人工查看逐页截图，确认图注完整、页底空白正常、后续正文衔接自然。
- **S 型优先规则**：左右栏对齐不得以牺牲 S 型阅读顺序为代价。标题、小节或 Back Matter 的左右同高要求不能覆盖“先填满左栏，再填右栏”的正文灌版规则。
- **禁止 spacer 规则**：不得在多栏正文流内插入空白块、透明块、spacer 或绝对定位块来下压某一栏；这类修法即使肉眼暂时对齐，也容易产生横向溢出、第三列或隐藏裁切，CP3 视为失败。
- **表格溢出处理**：先压缩间距（参见步骤3.4 Phase 1），压缩不够再跨页分割（参见步骤3.4 Phase 2）

**留白修复方法（首选内容重排；内容总量不足时才允许按页调整行距）：**

| 问题                           | 首选修复方式                 | 兜底方式（仅当首选无效时）                                        | 禁止方式                            |
| ------------------------------ | ------------------------------- | ---------------------------------------------------------------------- | -------------------------------------- |
| 页面留白过多（内容太少）       | 将下一页的段落/节标题移入当前页 | 全文内容总量不足时，按 § 8 的公式迭代调整行距 | 猜测行距值（未经 Playwright 实测）     |
| 页面溢出（内容太多）           | 将末尾段落移至下一页开头        | —                                                                     | 加超大 `line-height` 凑满            |
| 纯表格页留白（P5/P6 类）       | 将后续文字段落移至表格后填充    | 小幅调节块间距或正文段间距，并实测 | 用夸张 `td/th` padding、行高或空白块拉高表格 |
| 多页同时留白（数学上总量不足） | —                              | 逐页迭代行距调整（Playwright 实测 + 8.3 公式）                         | 不运行 Playwright 直接猜值             |

**禁止“硬填空”规则：**

- 不得为了让页面贴底，把三线表行高、`td/th` padding、图像高度、图注行距或段落 `line-height` 拉到肉眼明显异常。
- 表格视觉必须保留期刊三线表比例；若表格行数少，允许页面底部存在 `<30px` 安全余量，不得用单个表格承担全部填空。
- 若需要微调，优先顺序为：内容分页 → S 型连续灌版 → 段间距/块间距小幅调整 → 字号/栏宽小幅调整；表格 padding 只能做小幅视觉可接受调整。
- 小表格可由并排栏内表改为跨栏横向表来改善拥挤和底部对齐，但必须保持 Table 编号视觉顺序递增，并验证表题、表体和底线不被页脚裁切。

---

## 人机协同流程（降本增效）

**目标：减少手动逐页复核的成本，用结构化摘要替代盲审**

```
**Phase 1: AI生成初版**
生成双栏 HTML 并输出"分页摘要表"（见步骤 3.1）。

**Phase 2: 双栏分页转换**
1. 生成初版 HTML。
2. 检查分页摘要表。
3. **【前置】CP3.0 文件完整性核验**（必须在 Playwright 验证前执行）
   - 检查文件末尾是否以 `</html>` 结尾
   - 检查参考文献页是否存在（含 REFERENCES 或参考文献关键词）
   - 检查页数是否达到预期最小值（§CP3.0 有完整代码）
   - ⚠️ 任何一项失败 → **停止验证，重新生成 HTML**
4. **【验证】布局检查（CP3）**
   - **自动验证（强制）**：AI 必须优先运行 `scripts/validate_two_column_layout.mjs` 或等效 Playwright MCP 工作流逐页截图，并测量溢出/留白/图注底部对齐、页脚页码、首页 Introduction 视觉安全距离、S 型灌版和最后页 References 行距，输出报告后自行修复
   - **修改后重验（强制）**：任何影响分页、首页位置、栏宽、行距、段间距、表格、图片、图注、参考文献分布的修改，都必须回到 Playwright 截图 + 几何测量；不得只做局部肉眼确认。
   - **人工视觉复核（强制补充）**：AI 必须实际打开或查看逐页截图，重点复核每页页脚上方 30mm、左右栏底部、首页 Introduction、跨栏 Figure/Table 页、Back Matter/References 起始页、最后页 References 行距和页码位置；自动 metrics 不能替代视觉复核。
   检查点：详见下方风险标注规则。

**Phase 3: 通过playwright-mcp截图每页并修正问题页面**
1. 确认问题页面。
2. **【问题识别】分页问题处理**
   - **自动化路径**：AI 读取 Playwright 验证报告，自动定位溢出/留白页面及图注未底部对齐的图片组，按问题类型修复后重新截图验证
   - **人工反馈路径**：用户手动反馈问题（如"第 3 页溢出"），AI 根据反馈调整

**Phase 4: AI精准修复**
仅调整问题页及后续级联页。
```

**AI 必须在生成双栏 HTML 后输出分页摘要表：**

```
📄 分页摘要：
| 页码 | 内容 | 表格行数 | 预估填充率 | 风险 |
|------|------|----------|-----------|------|
| P1 | 封面 + Introduction开头 | - | ~85% | ✅ |
| P2 | Introduction续 + Methods开头 | - | 92% | ✅ |
| P3 | Methods + Table 1 (4行) | 4 | 88% | ✅ |
| P4 | Results 3.1 + Table 2 (25行) | 25 | 98% | ⚠️ 紧凑 |
| P5 | Table 2续 + 3.2 + Table 3 (15行) | 15 | 90% | ✅ |
| P6 | Table 3续 + 3.3 + Table 4 (10行) | 10 | 85% | ✅ |
| P7 | Table 4续 (28行, 压缩) | 28 | 95% | ⚠️ 已压缩 |
| ... | ... | ... | ... | ... |
```

**风险标注规则**：

- 自动验证阈值（Playwright 报告）：
  - 溢出任意值 → FAILURE（必须修复，所有页适用）
  - 留白 ≥57px → FAILURE（必须压缩，**最后一页除外**）
  - 留白 30-57px → WARNING（建议压缩，**最后一页除外**）
  - 留白 <30px → PASS（保留页脚安全距离，不再用异常表格/行距强行填满）
  - 并排图片图注底部对齐差值 > 2px → FAILURE（必须修复）
  - 并排图片图注底部对齐差值 1-2px → WARNING（建议修正后再截图）
  - 左右栏顶部差值 > 4px → FAILURE；首页 Introduction 顶部差值 > 2px → FAILURE
  - 左右栏底部差值 > 13px → FAILURE；首页 Introduction 底部差值 > 2px → FAILURE
  - 首页 Introduction 底部到页脚线视觉安全距离 < 24px → FAILURE，即使 `overflow_px = 0` 也必须修复
  - 左右栏宽度差值 > 1px → FAILURE
  - 页脚页码未贴右边界或拼到 URL 后 → FAILURE
  - S 型灌版顺序检测失败 → FAILURE
  - Figure/Table 图注被图片、页面底部或页脚裁切，或句末标点不可见 → FAILURE
  - Figure 作为正文关键图时被 `max-height` 压缩到难以纸质阅读 → FAILURE；应优先调整分页或独立图页，而不是继续压缩图片
  - References 编号不连续、不递增、重复、缺号，或任何条目在 DOM 中存在但不在页面可视区内 → FAILURE
  - **最后一页**：留白不限，参考文献数量不可控，任意留白均为 PASS；但 References 行距/段距异常拉伸 → FAILURE
- 人工验证经验值：
  - 溢出 >10mm：标注必须修复
  - 溢出 5-10mm：标注建议修复
  - 非最后页肉眼可见的大块空白：即使几何未达 FAILURE，也应优先检查是否可以自然拉入后续内容

**固定验证产物（CP3 交付前必须存在）：**

- `screenshot/two-column-strict-page-01.png` 至最后一页逐页截图。
- `screenshot/two-column-strict-metrics.json`，至少包含：
  - 顶层：`page_count`、`strict_column_result`、`failures`、`format_issues`
  - 每页：`overflow_px`、`overflow_x_px`、`whitespace_px`、`left_bottom_gap_px`、`right_bottom_gap_px`、`bottom_delta_px`、`top_delta_px`、`footer_page_number_right_aligned`、`footer_page_number_appended_to_url`、`s_flow`
  - 图表：每个 Figure/Table caption 的可见状态、底部坐标和是否被页脚/容器裁切；大图的实际渲染宽度与内容宽度比例
  - References：每条参考文献编号、所在页、可见状态、是否按编号递增连续
  - 首页：`first_page_intro_flow.footer_safety_px`、`first_page_intro_flow.bottom_delta_px`、`first_page_intro_flow.visual_safe`
  - 最后一页：`final_reference_inline_stretch`

若没有固定 JSON，或 JSON 中任一 BLOCK 指标失败，CP3 视为未完成。

---

## 分页失败的根本原因

**错误做法：让内容跨页面自动流动**

```html
<!-- ❌ 错误：多个页面共用一个连续容器 -->
<body>
    <div class="two-column">
        <!-- 内容从第1页一直延伸到第N页 -->
        <h1>INTRODUCTION</h1>
        <p>第1段...</p>
        ...
        <p>第50段...</p>  <!-- CSS会自动分页，但无法控制每页内容量 -->
    </div>
</body>
```

**问题所在：**

- CSS `column-count: 2` 会让内容在左右栏之间自动流动
- 当内容跨越多个页面时，CSS 无法控制每页包含多少内容
- 结果导致某些页面留白过多，某些页面内容溢出

**正确做法：每页独立生成，精确控制内容**

```html
<!-- ✅ 正确：每个<div class="page">独立，包含精确计算的内容 -->
<body>
    <!-- 第1页：封面 + 正文流入（封面区底部有剩余空间时，Introduction 接续填入） -->
    <div class="page">
        <div class="page-content">
            <h1>Title</h1>
            <div class="abstract">...</div>
            <!-- 封面摘要区结束后，若页面仍有空间，正文直接接续，不另起新页 -->
            <div class="two-column" style="margin-top:25mm;">
                <h1 class="section-title">1 INTRODUCTION</h1>
                <p>第1段（首段，填满剩余空间）...</p>
                <!-- 按实际剩余高度填入适量正文 -->
            </div>
        </div>
    </div>

    <!-- 第2页：INTRODUCTION续（约550词） -->
    <div class="page">
        <div class="page-header">WANG ET AL.</div>
        <div class="page-content two-column">
            <h1 class="section-title">1 INTRODUCTION (continued)</h1>
            <p>第1段续...</p>
            <p>第2段...</p>
            <p>第3段...</p>
            <p>第4段...</p>
            <!-- 内容经过计算，刚好填满页面，不溢出也不留白 -->
        </div>
        <div class="page-footer">2</div>
    </div>

    <!-- 第3页：METHODS开头 + 图片（约350词 + 2图） -->
    <div class="page">
        <div class="page-header">WANG ET AL.</div>
        <div class="page-content two-column">
            <h1 class="section-title">2 MATERIALS AND METHODS</h1>
            <h2 class="subsection-title">2.1 ...</h2>
            <p>...</p>

            <!-- 跨栏图片 -->
            <div class="side-by-side-figures">
                <figure>Figure 1</figure>
                <figure>Figure 2</figure>
            </div>

            <h2 class="subsection-title">2.2 ...</h2>
            <p>...</p>
            <!-- 同样经过精确计算 -->
        </div>
        <div class="page-footer">3</div>
    </div>

    <!-- 继续生成第4、5、6...页 -->
</body>
```

**关键区别：**

| 对比项              | 错误做法            | 正确做法                         |
| ------------------- | ---------------------- | ----------------------------------- |
| **页面结构**  | 所有内容在一个连续容器 | 每页一个独立 `<div class="page">` |
| **内容控制**  | CSS 自动分配           | 手动计算并分配每页内容              |
| **分页点**    | CSS 随机决定           | 根据字数精确规划                    |
| **留白/溢出** | 无法避免               | 可以精确控制                        |

**可以使用 CSS column，但必须满足：**

```css
/* ✅ 可以继续使用CSS column分栏 */
.two-column {
    column-count: 2;           /* 这个没问题 */
    column-gap: var(--column-gap);
    text-align: justify;
}
```

**但是 HTML 结构必须是：**

```html
<!-- ✅ 每页独立，内容经过精确计算 -->
<div class="page">
    <div class="page-content two-column">
        <!-- 这一页包含的内容必须经过字数计算 -->
        <!-- 确保既不溢出（超过252mm），也不留白（低于222mm） -->
    </div>
</div>

<div class="page">
    <div class="page-content two-column">
        <!-- 下一页的内容同样经过精确计算 -->
    </div>
</div>
```

**核心要点：**

1. **CSS `column-count: 2` 可以用** - 这不是问题所在
2. **关键是每页独立** - 每个 `<div class="page">` 必须手动创建
3. **内容必须精确计算** - 每页包含多少段落/图表必须事先规划
4. **禁止跨页连续容器** - 不能让一个 `.two-column` 容器跨越多个页面

---

## 内容分析和分页规划

### 步骤3.1：内容分析和分页规划

**在生成 HTML 之前，必须先分析内容并规划分页：**

```python
# 1. 分析内容字数
def analyze_content(markdown_text):
    """分析每个章节的字数"""
    sections = {
        'INTRODUCTION': extract_section(markdown_text, 'INTRODUCTION'),
        'METHODS': extract_section(markdown_text, 'MATERIALS'),
        'RESULTS': extract_section(markdown_text, 'RESULTS'),
        'DISCUSSION': extract_section(markdown_text, 'DISCUSSION'),
    }

    for section, text in sections.items():
        word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
        print(f"{section}: {word_count} words")

    return sections

# 2. 规划分页（考虑图表占用空间）
page_plan = {
    2: {  # 第2页
        'content': 'INTRODUCTION前3段',
        'words': 400,
        'space_used': '约180mm',  # 双栏，每栏约90mm
        'has_figures': False
    },
    3: {  # 第3页
        'content': 'INTRODUCTION后2段 + METHODS 2.1',
        'words': 350,
        'space_used': '约160mm',
        'has_figures': True,  # Figures 1-2并排占约60mm
        'figures': ['Figure 1', 'Figure 2']
    },
    # ... 继续规划每一页
}

# 3. 验证分页计划
def validate_page_plan(page_plan):
    """验证每页内容不会溢出或留白"""
    MAX_HEIGHT = 252  # mm (297 - 25 - 20)

    for page_num, plan in page_plan.items():
        text_height = plan['words'] * 0.3  # 粗略估算：每词0.3mm
        fig_height = sum([60 if 'Figure' in f else 0 for f in plan.get('figures', [])])
        total = text_height + fig_height

        if total > MAX_HEIGHT:
            raise ValueError(f"第{page_num}页内容溢出！ ({total}mm > {MAX_HEIGHT}mm)")
        elif total < MAX_HEIGHT - 30:
            print(f"⚠️ 第{page_num}页留白过多！ ({MAX_HEIGHT - total}mm空白)")
```

---

## HTML 模板和构建示例

### 步骤3.2：手动创建每个页面

**为每页手动创建独立的 `<div class="page">`**:

```python
def generate_page_2():
    """生成第2页 - INTRODUCTION前3段"""
    page_html = '''
<div class="page">
    <div class="page-header">WANG ET AL.</div>
    <div class="page-content two-column">
        <h1 class="section-title">1 INTRODUCTION</h1>
        <p>第1段内容...</p>
        <p>第2段内容...</p>
        <p>第3段内容...</p>
    </div>
    <div class="page-footer">2</div>
</div>
'''
    return page_html

def generate_page_3():
    """生成第3页 - INTRODUCTION后2段 + Figures 1-2"""
    page_html = '''
<div class="page">
    <div class="page-header">WANG ET AL.</div>
    <div class="page-content two-column">
        <p>第4段内容...</p>
        <p>第5段内容...</p>

        <!-- 并排图片 -->
        <div class="side-by-side-figures">
            <figure id="fig-1">
                <img src="..." alt="Figure 1">
                <figcaption>...</figcaption>
            </figure>
            <figure id="fig-2">
                <img src="..." alt="Figure 2">
                <figcaption>...</figcaption>
            </figure>
        </div>

        <h1 class="section-title">2 MATERIALS AND METHODS</h1>
        <h2 class="subsection-title">2.1 ...</h2>
        <p>2.1节开头内容...</p>
    </div>
    <div class="page-footer">3</div>
</div>
'''
    return page_html

# 组装所有页面
html_pages = [
    generate_cover_page(),    # 第1页
    generate_page_2(),        # 第2页
    generate_page_3(),        # 第3页
    # ... 继续生成每一页
]

final_html = html_header + '\n'.join(html_pages) + html_footer
```

**⚠️ 完整实施流程（必须按顺序执行）：**

```python
# 第一步：分析内容字数
sections = analyze_content(content)
# 输出示例：INTRODUCTION: 550 words, METHODS: 1200 words, ...

# 第二步：规划分页（根据字数和图表）
page_plan = {
    1: {'type': 'cover', 'content': 'title + abstract + metadata'},
    2: {'type': 'text', 'section': 'INTRODUCTION', 'words': 550, 'paragraphs': [1,2,3,4]},
    3: {'type': 'mixed', 'section': 'METHODS 2.1-2.2', 'words': 350, 'figures': [1,2]},
    # ... 继续规划
}

# 第三步：一次性生成完整HTML文件（⚠️ 禁止逐页追加！）
# 第四步：写入文件
# 第五步：验证分页
validate_pagination(output_file)
```

**⚠️ 常见错误和避免方法：**

| 错误                       | 表现                                 | 避免方法                                                  |
| -------------------------- | ------------------------------------ | --------------------------------------------------------- |
| **使用追加模式写入** | 多次调用 Edit/Write 工具逐页追加       | ❌ 禁止 `<br>` ✅ 一次性生成完整 HTML 字符串，然后写入     |
| **让内容跨页流动**   | 所有内容在一个 `.two-column` 容器中 | ❌ 禁止 `<br>` ✅ 每页独立的 `<div class="page">`      |
| **未精确计算字数**   | 随意分配段落到页面                   | ❌ 禁止 `<br>` ✅ 使用 `analyze_content()` 计算每段字数 |
| **图表位置随意**     | 图表与引用文字距离过远               | ❌ 禁止 `<br>` ✅ 图表放在引用段落之后的页面             |

---

## 内容分割策略

### 步骤3.3：内容分割策略

**如何决定每页包含多少内容**:

1. **计算可用高度**:

   - 页面总高度：297 mm
   - 上边距：25 mm，下边距：20 mm
   - 页眉：约12 mm，页脚：约10 mm
   - **可用内容高度：约230 mm**
1. **估算文字高度**:

   - 字体：9 pt，行高：1.35
   - 每行高度：约4.3 mm
   - 双栏，每栏约27 mm 宽
   - **每栏约53行，每页约106行**
   - 每行约10-12个英文单词
   - **每页约600-800单词（纯文字）**
3. **扣除图表空间**:

   - 小图（并排）：约60 mm
   - 大图（跨栏）：约100-120 mm
   - 表格：根据行数估算，约40-80 mm
   - **有图表的页面：文字容量减半（300-400词）**
4. **分页点选择**:

   - 优先在段落之间分页
   - 避免标题单独在页底
   - 图表尽量放在引用它的文字附近

---

## 大图处理原则

### 大图处理原则

> **大图不要单独占一整页！尽可能并排放置，节省空间。**

#### 图片并排判断标准

| 条件                 | 判断标准                           | 处理方式                      |
| -------------------- | ---------------------------------- | ----------------------------- |
| **并排条件**   | 连续出现2张图片，且单张高度 < 80 mm | 使用并排布局                  |
| **等分比例**   | 两张图片内容同等重要               | `grid-template-columns: 1fr 1fr` |
| **不等分比例** | 一张主图一张辅图（如流程图+小图）  | `grid-template-columns: 1.2fr 0.8fr` |
| **禁止并排**   | 单张高度 > 120 mm 或图片数量 >=3    | 各自独立放置                  |
| **跨栏要求**   | 所有图片必须跨越双栏               | 使用 `column-span: all`     |

#### 图片并排 CSS 规则（双栏版）

```css
/* 基础并排容器 */
.side-by-side-figures {
  column-span: all;              /* 跨双栏 */
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 4mm;                    /* 行间距0，列间距4mm */
  margin: 5mm 0;
  break-inside: avoid;
  page-break-inside: avoid;
}

.side-by-side-figures figure {
  display: contents;
}

.side-by-side-figures figure img {
  grid-row: 1;
  width: 100%;
  height: auto;
  max-height: 120mm;             /* ⚠️ 防止高度溢出：限制为页面高度的一半 */
  object-fit: contain;           /* 保持比例 */
  display: block;
  align-self: end;               /* 图片底部对齐 */
}

.side-by-side-figures figcaption {
  grid-row: 2;
  margin-top: 2mm;
  align-self: end;               /* 图注底部对齐 */
}
```

#### 单张图片 CSS 规则

```css
figure img {
  width: 100%;
  height: auto;
  max-height: 120mm;             /* ⚠️ 防止高度溢出 */
  object-fit: contain;
  display: block;
}
```

#### 图片并排 CSS 规则（单栏版）

```html
<!-- 不等分比例示例：主图占60%，辅图占40% -->
<div style="display:flex;gap:5mm;margin:5mm 0;align-items:flex-end;break-inside:avoid;">
  <figure style="flex:1.2;margin:0;display:flex;flex-direction:column;">
    <img src="..." alt="主图" style="width:100%;height:auto;display:block;">
    <figcaption>...</figcaption>
  </figure>
  <figure style="flex:0.8;margin:0;display:flex;flex-direction:column;">
    <img src="..." alt="辅图" style="width:100%;height:auto;display:block;">
    <figcaption>...</figcaption>
  </figure>
</div>
```

#### 分页控制规则

```css
/* 防止图片跨页分割 */
figure, .side-by-side-figures, .table-wrapper {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* 图片前强制分页条件（剩余空间不足时） */
@media print {
  .force-page-break-before {
    break-before: page;
    page-break-before: always;
  }
}
```

---

## Playwright 自动布局验证（MANDATORY）

### Playwright 运行时选择（MANDATORY）

本技能做 CP3 视觉/几何验证时，必须优先使用用户已安装的 Playwright 能力，而不是默认绕到 Codex bundled runtime。

**优先级：**

1. **优先使用 `$playwright` skill 的 CLI wrapper**：先检查 `command -v npx`，再使用用户 skill 中的 `scripts/playwright_cli.sh` 或系统 `playwright` 命令。
2. **需要持续调试时使用 `$playwright-interactive`**：适用于同一 HTML 反复改版、刷新、截图、测量，不要每次重启浏览器。
3. **可用时使用 in-app browser plugin**：适合检查当前浏览器可见页面；若插件拒绝 `file://`，不得判定为“无浏览器”。
4. **只有以上路径不可用时，才考虑 Codex bundled Node/Playwright runtime**；不要优先使用它，因为它可能没有 `npx`，且 Playwright 浏览器缓存可能缺失。

**环境检查顺序：**

```bash
command -v npx
command -v playwright
test -x "$HOME/.codex/skills/playwright/scripts/playwright_cli.sh" || \
test -x "/Users/jikunren/Library/Mobile Documents/com~apple~CloudDocs/SyncConfig/claude/folder_data/skills/playwright/scripts/playwright_cli.sh"
```

**`file://` 处理：**

- 若 Playwright CLI 能直接打开 `file://`，可直接验证本地 HTML。
- 若 in-app browser plugin 因 URL policy 拒绝 `file://`，必须启动只读本地 HTTP 预览服务再验证，例如：

```bash
python3 -m http.server 9876 --bind 127.0.0.1
```

然后用 `http://127.0.0.1:9876/{输出目录}/two-column-{short-title}.html` 打开同一文件。

**禁止重复犯的错误：**

- 不得因为 Codex bundled runtime 缺浏览器缓存，就说“Playwright 不可用”。
- 不得优先尝试安装 bundled Playwright Chromium，除非 `$playwright` / `$playwright-interactive` / in-app browser 都不可用。
- 不得把系统 Chrome pipe 连接超时误判为 Playwright 整体不可用；应切换到 `$playwright` wrapper 或 `127.0.0.1` 本地预览路径。
- 临时 HTTP 服务验证完成后必须关闭，避免残留后台进程。

### 验证目标

- 逐页截图，确认页面级布局与肉眼结果一致
- 几何测量每页内容区域，检测溢出与留白
- 几何测量每个 `.side-by-side-figures` 内的 `figcaption` 底边，检测是否底部对齐
- 用 Playwright/DOM Range 检查正文、摘要、图注、表注中的 `.nowrap-cite` 或方括号内文引用，确认 `[n]` / `[n,m]` 没有成为视觉行首；References 列表编号排除在外
- 逐页视觉复核不可断引用后的词距：不得出现因 `word [n]` 绑定、统计短语不可断或两端对齐导致的夸张词间距、局部大空洞或统计短语孤立行首

### 必跑顺序

1. 生成完整双栏 HTML
2. 执行 CP3.0 文件完整性核验
3. 用 Playwright 打开本地 HTML
4. 等待字体与布局稳定
5. 截取每一页截图
6. 运行几何测量脚本并输出结构化报告，报告必须包含正文引用行首检查结果和正文词距美观检查结果
7. 若任一页失败，修复 HTML 后回到第 3 步重跑
8. 只有全部通过后，才允许继续步骤4/5/6/7

### Playwright 几何测量要点

**每页必须输出以下字段：**

- `page_index`
- `overflow_px`
- `overflow_x_px`
- `whitespace_px`
- `is_last_page`
- `side_by_side_groups`
- `column_alignment`（显式左右栏容器必须测量）
- `first_page_intro_flow`（首页 Introduction 使用连续 column flow 时必须测量）
- `s_flow`
- `status`

**每个并排图片组必须输出以下字段：**

- `group_index`
- `caption_bottoms_px`
- `caption_bottom_delta_px`
- `image_bottoms_px`
- `image_bottom_delta_px`
- `status`

**每个显式左右栏容器必须输出以下字段：**

- `left_width_px` / `right_width_px` / `width_delta_px`
- `left_top_px` / `right_top_px` / `top_delta_px`
- `left_bottom_px` / `right_bottom_px` / `bottom_delta_px`
- `status`

**每个 CSS 多栏连续流区域（如正文 flow、discussion-flow、method-results-flow）必须输出以下字段：**

- `flow_selector`
- `rect_count`
- `left_rect_count` / `right_rect_count` / `outside_rect_count`
- `left_top_px` / `right_top_px` / `top_delta_px`
- `left_bottom_px` / `right_bottom_px` / `bottom_delta_px`
- `left_bottom_gap_px` / `right_bottom_gap_px`
- `s_flow_status`
- `status`

说明：不能只测 `.manual-s-grid` 或显式左右栏。含 Figure + Discussion + Back Matter 的混合页也必须测 CSS 多栏实际 rect，否则会漏掉“右栏下移/左栏悬空/底部不齐”的问题。

**首页 Introduction 连续流必须输出以下字段：**

- `column_count`
- `left_rect_count` / `right_rect_count`
- `outside_rect_count`
- `left_bottom_gap_px` / `right_bottom_gap_px`
- `bottom_delta_px`
- `right_top_gap_px`
- `status`

### Playwright `evaluate()` 示例

```javascript
() => {
  const pages = [...document.querySelectorAll('.page')];
  return pages.map((page, pageIndex) => {
    const content = page.querySelector('.page-content') || page;
    const footer = page.querySelector('.page-footer');
    const contentRect = content.getBoundingClientRect();
    const footerTop = footer ? footer.getBoundingClientRect().top : page.getBoundingClientRect().bottom;

    const measurableChildren = [...content.querySelectorAll(':scope > *')].filter((el) => {
      const style = window.getComputedStyle(el);
      return style.display !== 'none' && style.visibility !== 'hidden';
    });

    const contentBottom = measurableChildren.length
      ? Math.max(...measurableChildren.map((el) => el.getBoundingClientRect().bottom))
      : contentRect.top;

    const overflowPx = Math.max(0, contentBottom - footerTop);
    const whitespacePx = Math.max(0, footerTop - contentBottom);

    const sideBySideGroups = [...page.querySelectorAll('.side-by-side-figures')].map((group, groupIndex) => {
      const captions = [...group.querySelectorAll('figcaption')].map((el) => el.getBoundingClientRect().bottom);
      const images = [...group.querySelectorAll('img')].map((el) => el.getBoundingClientRect().bottom);
      const captionDelta = captions.length > 1 ? Math.max(...captions) - Math.min(...captions) : 0;
      const imageDelta = images.length > 1 ? Math.max(...images) - Math.min(...images) : 0;

      return {
        group_index: groupIndex + 1,
        caption_bottoms_px: captions,
        caption_bottom_delta_px: captionDelta,
        image_bottoms_px: images,
        image_bottom_delta_px: imageDelta,
        status: captionDelta > 2 ? 'FAILURE' : captionDelta > 1 ? 'WARNING' : 'PASS'
      };
    });

    const isLastPage = pageIndex === pages.length - 1;
    const pageStatus =
      overflowPx > 0
        ? 'FAILURE'
        : !isLastPage && whitespacePx >= 57
          ? 'FAILURE'
          : !isLastPage && whitespacePx >= 30
            ? 'WARNING'
            : sideBySideGroups.some((group) => group.status === 'FAILURE')
              ? 'FAILURE'
              : sideBySideGroups.some((group) => group.status === 'WARNING')
                ? 'WARNING'
                : 'PASS';

    return {
      page_index: pageIndex + 1,
      overflow_px: overflowPx,
      whitespace_px: whitespacePx,
      is_last_page: isLastPage,
      side_by_side_groups: sideBySideGroups,
      status: pageStatus
    };
  });
}
```

### 截图要求（BLOCKING）

- 所有截图统一保存在双栏、单栏 HTML 所在目录下的 `screenshot/` 文件夹中
- 若目录不存在，先创建 `screenshot/`，再写入截图
- 必须对每个 `.page` 截图，不允许只截全页长图
- 若某页失败，必须额外对失败页中对应的 `.side-by-side-figures` 或页内容区做局部截图
- 交付前必须能提供“问题前截图 + 修复后截图”对比

**推荐命名：**

- `two-column-page-01.png`
- `two-column-page-03-issue-before.png`
- `two-column-page-03-issue-after.png`
- `two-column-page-03-group-01.png`
- `single-column-preview.png`

### 失败后的修复策略

**1. 图注底部未对齐**

- 双栏版：回退到模板中的 Grid 写法，确保 `.side-by-side-figures` 使用 `display:grid`、`figure` 使用 `display:contents`、`img` 与 `figcaption` 都带 `align-self:end`
- 若仍失败：检查是否混入额外 `margin-bottom`、不同 `line-height`、或某个 `figcaption` 被包裹在额外块级元素中
- 修复后必须重跑 Playwright 几何验证，直到 `caption_bottom_delta_px <= 2`

**2. 页面溢出**

- 优先将页尾最后一个段落、表格或图片组移至下一页
- 若是表格导致，按续表规则切分，不允许简单压缩到不可读
- 溢出页修复后，必须同时复核后续级联页

**3. 非最后页留白过多**

- 优先从下一页拉入一个完整段落、一个小节标题加首段，或一个图片组
- 若属于表格页留白，优先拉入后续文字，不要盲调表格行高；小表格允许保留 `<30px` 页脚安全距离，不得把 `td/th` padding 拉到肉眼夸张
- 多页同时留白时，才允许依据实测几何结果迭代微调行距

**4. 用户指出“太高/太低/整体下移/整体上移”**

- 只调整对应页面或块的纵向位置，不改正文断点、栏宽或字距，除非实测显示会溢出。
- 必须用毫米级或 0.5mm 级扫描至少 2-3 个候选值，记录 `overflow_px`、`whitespace_px`、左右栏 `bottom_delta_px` 后选择最大安全值。
- 调整后必须重新截图该页并重跑全页几何验证，避免修首页破坏后页。

**5. 左右栏不齐**

- 先确认阅读顺序是否为 S 型；不能用手工断行或空白块把顶部/底部“摆齐”。
- 对显式左右栏容器，必须同时满足宽度差 <= 1px、顶部差 <= 4px、底部差 <= 13px；首页 Introduction 更严格，顶部差 <= 2px、底部差 <= 2px。
- 若正文文字可使用连续流，优先改为固定高度 `column-count:2; column-fill:auto`，让浏览器按 DOM 顺序先左后右；只有图表、Back Matter、参考文献等结构化块才允许显式左右栏。
- 若只需下移右栏内某个 Back Matter 标题，使用目标标题 class 的局部 `margin-top`；不得在左栏末尾或右栏开头插入空块。修改后必须检查 computed style，确认没有被 `.section-title:not(:first-child)` 等更高优先级规则覆盖。

**6. 图像尺寸用于消除留白**

- 只能通过小步扫描或二分搜索找到最大安全图像尺寸；每个候选值都必须记录 `overflow_px`、`overflow_x_px`、`whitespace_px`、图注可见性和左右栏 `bottom_delta_px`。
- 一旦候选尺寸造成溢出、图注裁切或页脚遮挡，必须回退到上一个安全值；不得因为“底部无留白”继续使用溢出值。
- 如果最大安全图像尺寸仍留白，改用内容分页、跨栏表格或块间距微调；不得把图片拉到不可读或越界。

---

## 验证检查点

### ✅ CP 3检查点：验证无溢出/留白、S 型灌版、段落缩进、摘要对齐、Introduction 等行且图注底部对齐

**关键验证项（必须全部通过，且必须基于 Playwright 截图与几何报告）：**

```python
def validate_pagination(html_file):
    """验证双栏HTML分页是否正确"""

    # 1. 检查页面数量
    page_count = html_file.count('<div class="page">')
    print(f"📄 总页数: {page_count}")

    # 2. 检查每页独立性
    pages = extract_pages(html_file)
    for i, page in enumerate(pages, 1):
        # 验证每页都有独立的page-content
        if '<div class="page-content' not in page:
            raise ValidationError(f"第{i}页缺少page-content容器")

    # 3. 验证内容分布（关键！）
    for i, page in enumerate(pages[1:], 2):  # 从第2页开始（第1页是封面）
        # 提取页面文本内容
        text_content = extract_text(page)
        word_count = len(text_content.split())

        # 检查是否有图表
        has_figures = '<figure' in page or '.side-by-side-figures' in page
        has_tables = '<table' in page

        # 验证字数范围
        if has_figures or has_tables:
            # 有图表的页面：300-500词
            if word_count < 250 or word_count > 550:
                print(f"⚠️ 第{i}页字数异常: {word_count}词（含图表，建议300-500词）")
        else:
            # 纯文字页面：600-900词
            if word_count < 500 or word_count > 950:
                print(f"⚠️ 第{i}页字数异常: {word_count}词（纯文字，建议600-900词）")

        print(f"✅ 第{i}页: {word_count}词, 图表={has_figures or has_tables}")

    # 4. 检查摘要区右侧对齐
    abstract_nodes = query_all('.abstract-box, .abstract-box p')
    for node in abstract_nodes:
        style = get_computed_style(node)
        if style.get('text-align') != 'justify':
            raise ValidationError('摘要区必须 text-align: justify，右侧不得参差')

    # 5. 检查首页 Introduction 左右栏视觉行数
    intro = query_one('.first-page-introduction, .cover-introduction')
    if intro:
        left_lines, right_lines = count_rendered_lines_by_column(intro)
        if (left_lines + right_lines) % 2 != 0 or left_lines != right_lines:
            raise ValidationError(
                f'首页 Introduction 左右栏行数不齐: left={left_lines}, right={right_lines}'
            )

    # 6. 检查正文连续段落缩进
    for i, page in enumerate(pages, 1):
        paragraph_groups = collect_body_paragraph_groups(page)
        for group in paragraph_groups:
            if group and not is_no_indent(group[0]):
                raise ValidationError(f'第{i}页正文段落组首段必须不缩进')
            for p in group[1:]:
                if is_no_indent(p):
                    raise ValidationError(f'第{i}页正文连续段落后续段落必须缩进，禁止批量 no-indent')

    # 7. 检查 S 型灌版顺序
    for i, page in enumerate(pages, 1):
        blocks = collect_flow_blocks(page)
        if not is_s_flow_order(blocks):
            raise ValidationError(
                f'第{i}页不是 S 型布局：必须先填满左栏，再填右栏，标题/图片/表格不得截断'
            )

    # 8. 检查最后一页是否留白过多
    last_page = pages[-1]
    last_page_words = len(extract_text(last_page).split())
    if last_page_words < 300 and '参考文献' not in last_page and 'REFERENCES' not in last_page:
        print(f"⚠️ 最后一页内容过少({last_page_words}词)，可能留白过多")

    return True

# 执行验证
validate_pagination('双栏分页-XXX.html')
```

**手动验证步骤（仅作为 Playwright 失败后的辅助手段）：**

1. **在浏览器中打开 HTML 文件**

   - 每页应该显示为一张完整的 A 4白色卡片
   - 页面之间有20 px 灰色间距
1. **逐页检查留白**

   ```
   ✅ 合格：非最后页页面底部空白 < 30px，且内容不压页脚
   ⚠️ 警告：非最后页页面底部空白 30-57px（建议继续压缩）
   ❌ 失败：非最后页页面底部空白 >= 57px 或任意溢出
   ```
2. **检查溢出**

   - 使用浏览器检查元素，查看 `.page-content` 高度
   - 如果内容超出 `--content-height (252mm)`，则为溢出
   - 所有内容必须完全在白色页面内
4. **验证双栏对齐**

   - 打开浏览器开发者工具
   - 检查每页的左右栏宽度、顶部和底部是否对齐
   - 显式左右栏容器宽度差必须 <= 1px，顶部差 <= 4px，底部差 <= 13px；首页 Introduction 底部差必须 <= 2px
5. **验证 S 型灌版**

   - 页面内阅读顺序必须为：左栏自上而下 → 右栏自上而下
   - 不允许因为 `h1`、`h2`、图片、表格或表题而提前切到右栏
   - 若出现“左栏还有明显空白，但右栏已经开始新章节/新小节/新图表”，CP3 失败，必须重排
6. **验证首页摘要与 Introduction**

   - 摘要区右侧必须两端对齐，不得出现明显参差
   - 首页 Introduction 左右列视觉行数必须相等；总行数必须为偶数
7. **验证正文段落缩进**

   - 正文连续段落组首段必须顶格，无首行缩进
   - 同一段落组第二段及以后必须有首行缩进
   - 不允许连续多段正文全部使用 `no-indent`

**如果验证失败：**

```python
# 失败处理流程
if validation_failed:
    # 1. 重新分析内容
    analyze_content_distribution()

    # 2. 调整分页计划
    # 例如：第3页内容过多，将部分段落移到第4页
    page_plan[3]['content'] = 'METHODS 2.1前2段 + Figure 1-2'
    page_plan[4]['content'] = 'METHODS 2.1后3段 + 2.2开头'

    # 3. 重新生成HTML
    regenerate_html(page_plan)

    # 4. 再次验证
    validate_pagination('双栏分页-XXX.html')
```

**验证通过标准：**

- [ ] HTML 文件已生成
- [ ] 文件大小合理（通常20-50 KB）
- [ ] 包含所有页面（封面+正文+参考文献）
- [ ] 每页字数在合理范围（见上述标准）
- [ ] 非最后页 `whitespace_px < 30px` 或有明确、视觉正常且不违反表格/行距上限的说明
- [ ] 无任何内容溢出页面边界
- [ ] 已完成逐页 Playwright 截图
- [ ] 已输出逐页几何报告（overflow/overflow_x/whitespace/column_alignment/first_page_intro_flow/s_flow/inline_citation_line_head/word_spacing_aesthetic）
- [ ] 摘要区计算样式为 `text-align: justify`，截图中右侧边缘无明显参差
- [ ] 正文、摘要、图注、表注中的内文引用均与前一个词不可断绑定；无 `[n]` / `[n,m]` 作为视觉行首；未用拆词、截断、自动断字、手工换行或绝对定位规避
- [ ] 不可断引用和统计短语未造成夸张词距、局部大空洞或视觉突兀的行首块；必要时已通过栏宽/栏距、字号、`word-spacing`、句式或分页微调修正
- [ ] 首页 Introduction 左右列视觉行数相等，左右列合计行数为偶数
- [ ] 正文连续段落组首段不缩进，后续段落缩进；未对连续正文批量使用 `no-indent`
- [ ] 所有正文页均为 S 型灌版：先左栏后右栏，未被标题、图片、表格截断
- [ ] 所有并排图片图注底部对齐差值 <= 2px
- [ ] 所有表格保持正常三线表比例；未通过夸张行高、padding、空白块填页底
- [ ] 在浏览器中打开显示正常
- [ ] 大表格已按步骤3.4处理（压缩或续表）
- [ ] 所有续表只在真正拆分同一表格时包含" (Continued)"标题和重复表头；参考文献续页不得自动加 `(CONTINUED)`，直接接序号
- [ ] 已输出分页摘要表（含填充率和风险标注）
- [ ] 最终回复包含关键几何数字，而不是只说“通过”
