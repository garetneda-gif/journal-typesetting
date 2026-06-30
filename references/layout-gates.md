# 布局门控与检查点

本文件是 CP0-CP5、双栏几何验证、S 型灌版、截图和文本裁切检查的索引入口。深分页算法仍在 `references/pagination-rules.md`，正文细节仍在 `references/typesetting-rules.md`。

## 1. 检查点索引

| 检查点 | 位置 | 阻塞条件 | 主要工具 |
|---|---|---|---|
| CP0 | 依赖检查后 | docx skill、MCP 或必要本地工具不可用 | `references/dependency-check.md` |
| CP1 | 解析文档后 | 标题、作者、摘要、简短标题未确认 | `references/docx-parsing.md` |
| CP2 | 图片上传后 | 最终 HTML 引用本地图片、图床 URL 不通 | `references/image-urls.md` |
| CP3 | 双栏 HTML 后 | 溢出、留白、S 型失败、吞字、图表裁切 | `scripts/validate_two_column_layout.mjs` |
| CP4 | 参考文献后 | 链接缺失、Vancouver 格式不一致、编号不可见 | `scripts/verify_links.py` |
| CP5 | 最终交付前 | 样式、DOI、页码、可见文件、单栏双栏同步失败 | `scripts/style_validator.py` + audit scripts |

任一阻塞检查失败时，不得交付；必须修复后重跑对应检查。

## 2. CP3 双栏几何验证摘要

双栏 HTML 生成或修改后，必须运行：

```bash
node scripts/validate_two_column_layout.mjs /path/to/two-column.html --out /path/to/.screenshot
```

输出目录必须包含：

- 逐页截图。
- `two-column-strict-metrics.json`。

JSON 至少应包含：

- `page_count`
- `overflow_px`
- `overflow_x_px`
- `whitespace_px`
- `left_bottom_gap_px`
- `right_bottom_gap_px`
- `bottom_delta_px`
- `footer_page_number_right_aligned`
- `s_flow`
- `first_page_intro_flow`

若脚本输出 BLOCK 项，必须清零后才能进入下一步。

## 3. S 型灌版规则

- 双栏正文必须按 DOM 顺序先填满左栏，再填右栏。
- 不得为了让小节标题左右同高而改成“左上 → 右上 → 左下 → 右下”的横向网格。
- 标题对齐与 S 型冲突时，保留 S 型。
- 禁止插入空 `div`、spacer、透明块、绝对定位块或手工 `<br>` 来下压某栏。
- 宽表、并排图、Back Matter 和参考文献可以独立控制，但必须附带 Playwright 顶部、底部、宽度和溢出测量。

## 4. 截图与 rect 检查规则

用户指出或截图疑似“吞字、裁字、少半句、内容被遮挡”时：

1. 用 Playwright 打开磁盘上的当前 HTML。
2. 定位对应段落、标题或图注的 `textContent` / `innerText`。
3. 用 `getClientRects()` 检查每个文字 rect 是否超出所属双栏 flow、`.page-content` 或页脚裁切线。
4. 检查是否被 `overflow:hidden`、固定高度、页脚、图片或表格遮挡。
5. 保存当前页整页截图作为证据。
6. 若 DOM/rect 完整但用户浏览器显示不同，提示刷新或重新打开当前 HTML。
7. 若 rect 越界或尾句缺失，调整分页/高度后重跑 CP3。

## 5. 必须重跑 CP3 的场景

以下任一修改后都必须重跑 Playwright 截图和几何验证：

- 双栏分页。
- 首页位置、栏宽、段间距、行距。
- 表格、图片、图注。
- 参考文献分页。
- 正文段落缩进。
- 摘要区右侧宽度或对齐。
- 页脚 URL 或页码。
- 任何用户截图指出的版面异常。

## 6. 版面通过标准

- `overflow_px = 0`。
- `overflow_x_px = 0`。
- 非最后页 `whitespace_px < 30px`。
- 左右栏底部差达标。
- 页脚 URL 居中，页码独立右对齐。
- 正文和摘要两端对齐，禁用自动断字。
- 正文连续段落首段不缩进，后续段落缩进。
- 图表标题、正文和图注完整可见。
- References 编号连续递增，每条在可视区域真实可见。
