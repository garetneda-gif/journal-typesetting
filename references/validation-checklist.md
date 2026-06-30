# 第7步：最终验证（BLOCKING - 门控机制）

> 结构说明：本文件只作为最终交付 checklist。DOI/page 审计使用 `scripts/audit_doi_pages.py`，可见文件审计使用 `scripts/audit_visible_outputs.py`，递增表维护使用 `scripts/sequence_manager.py`。


## 强制检查项-源文件比对验证

**此步骤必须重新读取源 DOCX 文件，逐项比对确保没有内容丢失或新增：**

```
验证流程：
1. 重新读取源DOCX文件（使用docx skill）
2. 提取关键计数并与HTML对比：
   ├─ 各章节段落数（逐章对比）
   ├─ 每个表格的行数（逐表对比）
   ├─ 参考文献总条数
   ├─ 图片总数
   └─ back matter各小节（Acknowledgments, Author Contribution等）
3. 差异项标红报告
4. 如有差异 → 阻止交付，修复后重新验证
```

**比对输出格式示例：**

```
📋 源文件比对结果：
| 内容项 | 源DOCX | 双栏HTML | 单栏HTML | 状态 |
|--------|--------|----------|----------|------|
| Introduction段落数 | 5 | 5 | 5 | ✅ |
| Methods段落数 | 8 | 8 | 8 | ✅ |
| Table 2行数 | 26 | 26 | 26 | ✅ |
| Table 3行数 | 21 | 21 | 21 | ✅ |
| 参考文献条数 | 33 | 33 | 33 | ✅ |
| 图片数 | 0 | 0 | 0 | ✅ |
| back matter小节 | 6 | 6 | 6 | ✅ |
→ ✅ 全部一致，可交付
```

## 其他检查项

| 检查项            | 通过标准               | 失败处理                    |
| ----------------- | ---------------------- | --------------------------- |
| PubMed 链接       | 已尝试验证（有记录）   | WARN: 未执行 PubMed 验证    |
| Crossref 链接     | 链接数 >= DOI 提取数   | WARN: Crossref 链接少于预期 |
| References Vancouver 正文 | 参考文献正文统一为 Vancouver：`[n] Authors. Title. Journal. Year;Volume(Issue):Pages/article-number.`；作者超过 3 位时列前 3 位后加 `et al.`，3 位及以下全部列出；不得残留 APA 作者格式、`&`、随机 Title Case、期刊全称/缩写混用、`Year, Volume(Issue):Pages` 逗号格式、`[J]`、装饰符号或原稿 DOI 大小写混排 | BLOCK: 先规范化参考文献正文再继续 |
| References 元数据完整性 | 每条参考文献均已尝试用 PubMed/Crossref/DOI/出版社页面补齐卷、期、页码或文章号；电子文章号按页码位保留，如 `h2372`、`e43`、`R60`；无法高置信补齐的条目在报告中列明原因 | BLOCK: 补齐可核验元数据或记录无法补齐原因 |
| References 双栏/单栏一致 | 双栏、单栏和本地预览（若存在）参考文献正文逐条一致；单栏只追加 PubMed / Google Scholar / Crossref 链接，不使用另一套正文 | BLOCK: 同步 References 正文后重验 |
| References 编号与可见性 | 双栏分页后 References 编号必须严格递增且连续；每条参考文献必须通过 Playwright 元素边界或截图确认真实可见，不得只存在 DOM 但被 `overflow:hidden`、固定高度页面或页脚裁切隐藏 | BLOCK: 重新拆分 References 并重跑截图/metrics |
| 图片 URL 可访问性 | 所有正文图片均验证 200 状态；不得只随机抽查 | BLOCK: 上传/修复不可访问图片 |
| 图床 SFTP 上传链路 | 必须优先按 `references/image-urls.md` 的 MedBA SFTP profile 直连 `editor1@47.239.5.114:22`，上传到 `/assets/{简短标题}/`；不得使用 `medbam.org:22`，不得依赖 `medbam.org` keychain；只有直连失败并记录实际 stderr 后才允许 zip/手动上传 fallback | BLOCK: 使用正确 SFTP profile 重新上传并记录结果 |
| 文章图片图床引用 | 双栏版与单栏版所有正文图片均使用 `https://medbam.org/assets/{简短标题}/...`；不得出现本地 `assets/...`、`./assets/...`、绝对磁盘路径或 `file://...` 图片引用；上传后哈希或尺寸与本地源图一致 | BLOCK: 上传图片到图床并替换 HTML 引用 |
| 摘要标签 | 双栏版与单栏版摘要均使用 `Background:` / `Methods:` / `Results:` / `Conclusion:`；不得出现 `Objective:`、`Aim:`、`Purpose:` 等未规范标签；标签本身加粗，正文不整体加粗 | BLOCK: 规范摘要标签后重生成 |
| 正文文献引用 | 正文引用统一为 `[n]` / `[n,m]`，可见引用前有空格、标点紧跟右方括号；HTML 必须用 `nowrap-cite`/`&nbsp;` 将正文引用绑定到前一个词；不得残留 Word 上标引用、裸数字引用、`word[1]` 粘连或 `issues. [13].` | BLOCK: 转换引用格式后重生成 |
| 正文引用行首检查 | 双栏版和单栏版均需用 Playwright 截图或 DOM Range 检查确认：正文、摘要、图注、表注中的 `[n]` / `[n,m]` 不作为视觉行首出现；同一渲染行左侧必须有前置正文词；References 列表编号不纳入此项 | BLOCK: 用不可断空格/nowrap 绑定引用与前词，禁止拆词、截断、自动断字、手工 `<br>` 或绝对定位，重生成并重跑截图 |
| 正文引用词距美观 | 双栏版和单栏版绑定 `word [n]` 后逐页截图无明显夸张词距、局部大空洞或“一个单词一大格”的两端对齐；统计短语如 `OR = ...`、`95% CI = ...` 不孤立到行首造成视觉突兀 | BLOCK: 小幅调整栏宽/栏距或内容宽度、字号、`word-spacing`、句式顺序、段落承接或分页位置；禁止拆词、截断、自动断字、手工 `<br>`、spacer 或绝对定位 |
| References 正文格式 | 参考文献正文统一 Vancouver 风格：`[n] Authors. Title. Journal. Year;Volume(Issue):Pages/article-number.`；作者格式、题名大小写、期刊缩写和年份卷期页标点全篇一致；双栏/单栏一致；缺页码不能原样留空 | BLOCK: 统一参考文献格式并补齐可核验元数据后重生成 |
| Playwright 运行时路径 | CP3 必须优先使用 `$playwright` wrapper / 系统 `playwright` / `$playwright-interactive` / in-app browser；若使用临时 HTTP 预览替代 `file://`，需记录端口并在完成后关闭；不得优先使用 Codex bundled runtime | BLOCK: 切换到正确运行时并重跑 |
| Playwright 截图验证 | 输出目录下存在 `screenshot/`，每页均有 `two-column-strict-page-XX.png` 截图；任何分页/位置/栏宽/行距/表格/图片/图注/References 修改后都已重跑截图；AI 必须实际查看逐页截图，重点复核页脚上方 30mm、首页 Introduction、左右栏底部、跨栏 Figure/Table 页、Back Matter/References 起始页、最后页 References 行距和页码位置 | BLOCK: 缺少截图证据或未做视觉复核 |
| Playwright 固定 metrics | 输出目录下存在 `screenshot/two-column-strict-metrics.json`，且包含 `page_count`、`overflow_px`、`overflow_x_px`、`whitespace_px`、`left_bottom_gap_px`、`right_bottom_gap_px`、`bottom_delta_px`、`footer_page_number_right_aligned`、`s_flow`、`first_page_intro_flow`、`final_reference_inline_stretch`；还应包含 CSS 多栏 flow 的 rect 统计、Figure/Table caption 可见性、References 编号连续性和可见性、正文引用行首检查结果、正文词距美观检查结果 | BLOCK: 运行 `scripts/validate_two_column_layout.mjs` 或等效脚本补齐固定 JSON |
| Playwright 几何验证 | 非最后页无溢出；`overflow_x_px=0`；`whitespace_px < 30px` 为 PASS、30-57px 为 WARNING、>=57px 为 BLOCK；并排图图注底部差值 <= 2px；CSS 多栏 flow 和显式左右栏的宽度/顶部/底部差值达标；首页 Introduction 底部到页脚线视觉安全距离 >= 24px 且底部差 <= 2px | BLOCK: 返回修复后重跑 |
| Figure/Table 图注完整性 | Figure/Table 标签颜色和加粗一致；标签后不加句点，图注正文句末标点完整；所有图注/表注在截图中完整可见且未被图片、页脚或容器裁切 | BLOCK: 调整图片高度/分页/图注后重跑 |
| Figure 可读性与尺寸扫描 | 关键大图不得被 `max-height` 压缩到纸质不可读；跨栏大图应接近内容区全宽显示；放大/缩小时必须记录原值、候选值、最终值，并选择 `overflow_px=0`、图注完整、页脚安全的最大安全值 | BLOCK: 重新扫描图像尺寸、安排图页和正文分页 |
| 页脚 URL 与页码 | URL 居中，页码作为 `.page-footer .page-num` 独立右对齐；`footer_page_number_right_aligned=true` 且 `footer_page_number_appended_to_url=false`；不得出现 `medbam.org3` 可见拼接 | BLOCK: 修正页脚 DOM/CSS 后重跑截图和 metrics |
| 续页页眉 | 双栏续页页眉使用第一作者姓氏加 `et al.`，如 `Wang et al.`；不得写成 `A AND B` 或列出多位作者姓名 | BLOCK: 修正 `.page-header` 后重跑截图和 metrics |
| S 型灌版顺序 | 每页正文按 DOM 顺序先填满左栏再填右栏；正文优先使用固定高度连续 column flow；标题、图片、表格、Back Matter、参考文献不得让右栏提前开始；不得为了 `3.1/3.2` 或 Back Matter 标题左右同高改成横向网格；显式左右栏只允许用于首页、Back Matter、References 等确需独立控制的结构，且必须附带左右栏测量 | BLOCK: 返回重排页面 |
| 禁止 spacer 伪对齐 | 不存在空 `div`、透明块、绝对定位块、手工断行、`break-before:column` 或异常 wrapper 用于下压某栏；Back Matter 微调只能用目标标题/块的局部 class 和 margin，并确认 computed style 生效 | BLOCK: 删除 spacer/伪对齐结构，改用 S 型重排或局部 margin 后重跑 |
| 全文两端对齐且禁自动断字 | 正文与摘要 `text-align: justify`；普通正文容器 `hyphens:none` / `-webkit-hyphens:none`；无大量行尾短横线 | BLOCK: 修正 CSS 与换行策略 |
| 正文段落缩进 | 正文连续段落组首段不缩进，后续段落缩进；不得连续多段正文批量 `no-indent` | BLOCK: 返回修正缩进 |
| Back Matter 句末标点 | 兜底短句必须带句号，例如 `Not applicable.`、`Not available.`；ORCID 无信息固定为 `Not available.` | BLOCK: 返回修正标点 |
| 表格视觉比例 | 三线表保持自然比例；不得使用夸张行高、`td/th` padding、空白行或透明内容填补页底 | BLOCK: 回退表格拉伸并重排页面 |
| 表格视觉顺序与跨栏 | Table 编号按视觉阅读顺序递增；小表可改为跨栏横向三线表解决拥挤，但不得乱序、不得被裁切、不得破坏 S 型正文流 | BLOCK: 重排表格位置/跨栏方式并重跑截图 |
| 表格表头与列对齐 | 表头大小写统一；数值列居中或按小数点/单位一致对齐；同一表内不得出现明显列对齐混乱 | BLOCK: 统一表格样式后重跑截图 |
| 首页 Introduction | 使用 Playwright 验证左右栏顶部/底部、页脚视觉安全距离和 S 型顺序；整体上下移动需毫米级扫描后取安全值；底部到页脚线必须 >=24px，左右底部差 <=2px | BLOCK: 重新扫描并修复 |
| 最后一页 References | 最后一页留白和左右栏底部对齐豁免；References 必须保持正常字号、行距、段距且不使用悬挂缩进；不得通过拉大行距/段距或空白块贴底 | BLOCK: 回退异常拉伸，接受自然留白 |
| References 续页 | 参考文献跨页直接接序号，不自动添加 `REFERENCES (CONTINUED)`；`(Continued)` 仅用于真正续表 | BLOCK: 删除错误续页标题 |
| 红色 MedBA logo | 双栏版与单栏版首页均使用 `https://medbam.org/assets/logo.png`，遵循图床根目录命名规范；除非用户明确另给 logo；不得使用项目本地图片 | BLOCK: 替换 logo 资产与引用 |
| Article title 格式 | 双栏/单栏一致，采用 sentence case（仅首词和专有名词大写） | BLOCK: 返回修正标题格式 |
| Keywords 格式     | 双栏/单栏/本地预览一致，使用逗号加空格分隔；默认普通单词小写，除第一个关键词开头可大写外不得使用 Title Case，缩写和专有名词按语义保留；若用户或期刊明确要求每组关键词首词首字母大写，则按指定覆盖默认规则 | BLOCK: 返回修正关键词格式   |
| 生物医学正文细节 | 正文基因符号斜体；统计学 `<em>p</em>` 值斜体；英文图表并列引用使用逗号；避免 `X's team research` 等口语表达，改为 `X et al. showed/reported...` | BLOCK: 修正文案和 HTML 标记后同步全版本 |
| 四文件同步 | 影响正文、摘要、关键词、图表、图注、References、分页或样式的修改，必须同步双栏正式版、双栏 local preview、单栏正式版、单栏 local preview（若存在），并做残留文本扫描 | BLOCK: 同步所有版本后重验 |

## 最终交付报告（MANDATORY）

推荐 CP3 命令（优先使用已可用的 `$playwright` wrapper；若本机 Node 无法直接加载 Playwright，可设置 `NODE_PATH` 指向可用的 `node_modules`，并用系统 Chrome 路径兜底）：

```bash
NODE_PATH="/path/to/node_modules" \
CHROME_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
node "/Users/jikunren/Library/Mobile Documents/com~apple~CloudDocs/SyncConfig/claude/folder_data/skills/journal-typesetting/scripts/validate_two_column_layout.mjs" \
  "/path/to/two-column-short-title.html" \
  --out "/path/to/output/screenshot"
```

交付时必须给出结构化验证摘要，不得只说“已通过”：

```
CP3: PASS
Playwright runtime: $playwright wrapper / system playwright / playwright-interactive / in-app browser + 127.0.0.1 preview（写明实际使用项）
Metrics JSON: screenshot/two-column-strict-metrics.json
Page geometry:
- P1 overflow=0px, whitespace=..., first_page_intro bottom_delta=...
- P2 overflow=0px, whitespace=..., column top_delta=..., bottom_delta=...
- ...
Footer page number: right_aligned=true, appended_to_url=false
Figures: caption_bottom_delta max=...
Figures: caption visible PASS, large figure readability PASS
S-flow: PASS
Final page references: normal line-height, final-page whitespace accepted
Style validator: PASS（若有术语类 warning，说明原因）
Image URLs: HTTP 200 + hash/size verified
References: Vancouver PASS, sequence visible PASS, references=..., Google Scholar=..., PubMed=..., Crossref=..., missing page/article-number unresolved=0（或列出无法补齐条目）
```

若存在 WARNING，必须说明为什么接受或继续修复；不能把 WARNING 当 PASS 交付。
