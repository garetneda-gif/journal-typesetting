---
name: journal-typesetting
description: |
  将Word学术论文转换为MedBA Medicine期刊HTML格式。支持双栏分页(PDF下载)和单栏连续(在线预览)两种输出。
  自动为参考文献添加验证后的元数据链接(PubMed | Google Scholar | Crossref)。
  使用场景：当用户提供Word格式的学术论文并要求排版为期刊HTML格式时使用。
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

## 概述

1. 本技能将 Word 格式的学术论文转换为 MedBA Medicine 期刊规定的 HTML 格式，生成两个版本：

   1. **双栏分页版** - 供 PDF 下载，A4 分页，双栏布局
   2. **单栏连续版** - 供在线预览，连续滚动，包含参考文献元数据链接
2. 期刊默认配置

   - **期刊名称**: MedBA Medicine
   - **Logo URL**: https://medbam.org/assets/logo.png
   - **DOI 前缀**: 10.65079/xxx
   - **网址**: https://medbam.org
   - **主题色**: #005a8c
3. 资源文件

   | 目录        | 文件                            | 说明                                                 |
   | ----------- | ------------------------------- | ---------------------------------------------------- |
   | 根目录      | `SKILL.md`                    | 工作流骨架（本文档）                                 |
   | Assets/     | `template-two-column.html`    | **双栏分页 HTML 模板**（含分页修复）           |
   |             | `template-single-column.html` | **单栏连续 HTML 模板**（连续滚动）             |
   | Scripts/    | `verify_links.py`             | 参考文献链接验证工具                                 |
   |             | `html_generator.py`           | HTML 生成核心模块（内部）                            |
   |             | `style_validator.py`          | 样式一致性验证器                                     |
   | References/ | `html-structure.md`           | HTML 结构和 CSS 类说明                               |
   |             | `reference-links.md`          | 参考文献链接生成指南                                 |
   |             | `style-mapping.md`            | 样式映射表（元素与CSS对应关系）                      |
   |             | `pagination-rules.md`         | 分页规则、CP3 强制布局验证（含 Playwright 截图与几何验证） |
   |             | `typesetting-rules.md`        | 正文排版细节规则（图注、缩进、Back Matter 等）       |
   |             | `troubleshooting.md`          | 常见问题排查 + 大文件写入规则                        |
   |             | `dependency-check.md`         | 依赖检查完整流程                                     |
   |             | `docx-parsing.md`             | Word 文档解析与简短标题确定                          |
   |             | `image-urls.md`               | 图片 URL 收集流程                                    |
   |             | `validation-checklist.md`     | 最终验证检查项                                       |

> 大文件写入规则（HTML > 30KB 时禁止 write 工具）参见 references/troubleshooting.md § 大文件写入规则

---

## 工作流程总览

```
[预检] 确认前置条件 → [步骤0] 依赖检查 → [步骤1] 解析文档 → [步骤2] 收集图片URL →
[步骤3] 生成双栏HTML → [步骤4] 生成单栏HTML → [步骤5] 添加参考文献链接 →
[步骤6] 输出文件 → [步骤7] 强制验证 ✅
```

---

## 检查点系统

| 检查点         | 位置    | 验证内容                                          | 失败操作                         |
| -------------- | ------- | ------------------------------------------------- | -------------------------------- |
| **CP 0** | 步骤0后 | MCP 可用性                                        | 询问用户：继续 (fallback) 或中止 |
| **CP 1** | 步骤1后 | 标题、作者、摘要已提取                            | 重新解析或手动输入               |
| **CP 2** | 步骤2后 | 所有图片 URL 格式正确                             | 重新收集                         |
| **CP 3** | 步骤3后 | 双栏 HTML 无溢出/留白，且并排图图注底部对齐（必须通过 Playwright 截图与几何验证） | 调整分页重新生成 |
| **CP 4** | 步骤5后 | 参考文献链接数量符合预期                          | 记录警告但继续                   |
| **CP 5** | 步骤7   | 通过各项检查                                      | 阻止交付                         |

---

## 第0步：依赖检查（MANDATORY - 阻塞性）

> 完整依赖检查流程（docx skill 阻塞性检查、MCP 可用性检查、降级策略）参见 references/dependency-check.md

---

## 第1步：解析 Word 文档并确定简短标题

> 完整解析流程（元素识别方法、简短标题规则、用户确认交互）参见 references/docx-parsing.md

- 关键词（`Keywords:`）提取后默认统一规范为小写输出，并使用分号加空格分隔；仅保留专有名词、基因符号或缩写原样确有必要时才例外，并在交付前复核一致性
- 确认简短标题时，必须把最终标题以单独一行的可复制文本明确展示给用户，便于手动复制到文件夹名、图片路径或其他外部系统

---

## 第2步：收集图片 URL

> 完整图片 URL 收集流程（列出图片、URL 配置选项、根据选择收集）参见 references/image-urls.md

---

## 第3步：生成双栏分页 HTML

参考模板: `assets/template-two-column.html`

### 样式一致性规则 (MANDATORY - 最高优先级)

**核心原则：100%复制模板样式，杜绝随机性**

- ❌ 禁止推测或生成 CSS / 禁止美化样式 / 禁止修改模板
- ⚠️ 正文行距统一为 1.4，行距取值范围 1.0–1.9，严禁 ≥2.0
- ✅ 完全复制 `<style>` 标签（模板第7-280行）
- ✅ 严格使用模板 class / 保留所有 inline style

> 完整样式规则和 CSS 变量清单参见 references/style-mapping.md

### 分页规则

> 分页核心原则、人机协同流程、失败根因分析、内容分析、分割策略、验证检查点参见 references/pagination-rules.md

- 双栏 HTML 生成后，**必须**先执行 Playwright 截图验证与几何测量；若发现底部未对齐、页面溢出或非最后页留白超阈值，必须修复后重跑，未通过 CP3 不得继续后续步骤

### 步骤3.1-3.3：分页规划与页面创建

- **步骤3.1**：内容分析和分页规划 → references/pagination-rules.md § 内容分析和分页规划
- **步骤3.2**：手动创建每个页面（禁止追加模式，一次性生成完整 HTML）→ references/pagination-rules.md § 手动创建每个页面
- **步骤3.3**：内容分割策略（每页约600-800词纯文字或300-400词含图表）→ references/pagination-rules.md § 内容分割策略

### 步骤3.4：正文排版细节规则（MANDATORY）

> 所有排版细节规则（图注句点、图注对齐、URL 处理、引号标点、封面间距、段落缩进、Back Matter、左栏对齐、MathJax 公式、参考文献缩进、表格跨栏/续表、蛇形布局）参见 references/typesetting-rules.md

- 首页摘要区 `Keywords:` 后的关键词列表统一使用“分号分隔 + 默认小写”的展示规则，避免同一篇文章中出现大小写和分隔符混排

> HTML 结构和 CSS 类说明参见 references/html-structure.md

### 输出文件

`two-column-{short-title}.html`

---

## 第4步：生成单栏连续 HTML

参考模板: `assets/template-single-column.html`

### 样式一致性规则 (MANDATORY)

**与第3步相同，必须100%复制模板样式**

- ✅ 完全复制 `<style>` 标签（模板第7-124行）
- ✅ 使用模板 inline style
- ✅ 图片并排布局使用模板第251-260行的 CSS

> 样式规则参见 references/style-mapping.md

### 特点

- 单栏布局，**连续滚动，绝对不分页**
- 支持 `single-page-pdf` 类用于长页 PDF 生成
- **禁止任何分页符、page-break 或分页 CSS**

### 输出文件

`single-column-{short-title}.html`

---

## 第5步：添加参考文献链接（双栏+单栏均执行）

### 验证模式选择

| 模式      | DOI 提取 | PubMed  | Crossref     | Google Scholar | 耗时    | MCP 调用 |
| --------- | -------- | ------- | ------------ | -------------- | ------- | -------- |
| 快速      | 本地     | ❌      | ❌           | 总是           | <10秒   | 0次      |
| 标准      | 本地     | ❌      | 无 DOI 时    | 总是           | 30-60秒 | ~15次    |
| 完整      | 本地     | 全部    | 无 DOI 时    | 总是           | 2-5分钟 | ~40次    |

### 执行策略（严格遵守优先级）

```
优先级1: DOI提取（本地，0 MCP调用）→ 优先级2: PubMed查询 → 优先级3: Crossref查询（仅无DOI时）→ 优先级4: Google Scholar（总是生成）
```

- ❌ 禁止臆造 DOI/PMID
- ❌ 低置信度匹配（<80%）必须跳过
- ⚠️ PubMed MCP 连续 2 次超时（>10s）→ 自动切换标准模式

> 完整实现逻辑（DOI提取正则、PubMed策略、Crossref查询、Scholar链接生成、verify_links.py用法）参见 references/reference-links.md

### CP 4 检查点

- [ ] Google Scholar 链接 = 参考文献总数
- [ ] PubMed 链接 >= 0（记录实际数量）
- [ ] Crossref 链接 >= DOI 提取数量
- [ ] 已尝试验证所有文献（有记录）

---

## 第6步：输出最终文件

### 输出目录

`/Users/jikunren/Documents/期刊排版/{简短标题}/`

### 输出结构

```
/Users/jikunren/Documents/期刊排版/Ferroptosis-Cervical-Cancer/
├── screenshot/
│   ├── two-column-page-01.png
│   ├── two-column-page-03-issue-before.png
│   ├── two-column-page-03-issue-after.png
│   └── single-column-preview.png
├── two-column-Ferroptosis-Cervical-Cancer.html
└── single-column-Ferroptosis-Cervical-Cancer.html
```

---

## 第7步：最终验证（BLOCKING - 门控机制）

> 完整验证流程（源文件比对验证、比对输出格式、其他检查项）参见 references/validation-checklist.md

- 强制复核 `Keywords:` 行：双栏版与单栏版的关键词内容一致，使用分号分隔，普通词默认小写，语义性缩写按需保留原样
- 强制附带 Playwright 验证结果：至少包含存放于输出目录 `screenshot/` 下的逐页截图、溢出/留白几何报告，以及并排图片图注底部对齐测量结果
