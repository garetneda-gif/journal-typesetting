# 第1步：解析 Word 文档并确定简短标题

## 1.1 解析 Word 文档

使用 `skill('docx')` 加载 docx 技能，然后读取 Word 文档内容，提取以下结构化信息：

| 元素     | 识别方法                                    |
| -------- | ------------------------------------------- |
| 标题     | 第一个"Title"样式段落或前3段中最大字号      |
| 作者     | 标题后、单位前的逗号分隔姓名                |
| 单位     | 带上标编号的机构名称列表                    |
| 通讯作者 | 包含"Corresponding author: "或 Email 的段落 |
| 摘要     | "Abstract"标签后的结构化内容                |
| 关键词   | "Keywords: "开头的行；提取后默认规范为小写  |
| 正文章节 | 编号标题（1 INTRODUCTION, 2 METHODS 等）    |
| 图片     | 图片对象或 `[Figure N]` 占位符            |
| 表格     | Word 表格对象                               |
| 参考文献 | "REFERENCES"后的编号列表                    |

## 1.1.1 文章主标题规范化（MANDATORY）

- 提取标题后，必须转换为 sentence case 再用于 HTML 生成
- 规则：仅大写首词首字母和专有名词（基因符号、数据库名、疾病缩写等），其余词小写
- 冒号后首词大写（AMA 风格），破折号后不大写
- 若原标题为全大写，必须向用户确认专有名词后再转换，禁止盲目处理
- 完整规则和例外清单参见 typesetting-rules.md § 文章主标题大小写规则

## 1.1.2 关键词规范化（MANDATORY）

- 提取 `Keywords:` 行后，按分号或逗号拆分关键词，清理首尾空格，再以 `关键词1; 关键词2; 关键词3` 的格式重新拼接输出
- 默认将每个关键词规范为小写
- 双栏 HTML 与单栏 HTML 必须使用完全一致的关键词字符串
- 仅在专有名词、标准基因符号、数据库缩写等大小写具有明确语义时保留原样；若无法确认，默认使用小写
- 禁止出现同一行内部分关键词首字母大写、部分全小写的混排

**目标格式示例：**

`Keywords: erlotinib; adverse events; FAERS; lung cancer; pancreatic cancer`

## 1.2 确定简短标题

**简化规则：**

| 规则     | 要求                                               |
| -------- | -------------------------------------------------- |
| 最大长度 | ≤ 50 字符                                         |
| 简化方法 | 提取核心关键词（疾病+研究主题+类型）               |
| 禁止字符 | 不要使用 `/ \ : * ? " < >`                        |
| 格式     | 使用连字符分隔，如 `Ferroptosis-Cervical-Cancer` |

**示例：**

| 原标题                                                                                                                    | 简化后                       |
| ------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Based on transcriptome analysis of novel prognosis and targeted therapy-related genes with ferroptosis in cervical cancer | Ferroptosis-Cervical-Cancer  |
| A comprehensive review of machine learning approaches in cardiovascular disease prediction                                | ML-Cardiovascular-Prediction |

## 1.3 用户确认

```javascript
question(questions=[{
  header: "简短标题",
  question: "请确认用于文件夹和图片URL的简短标题",
  options: [
    {label: "Ferroptosis-Cervical-Cancer", description: "推荐的简短标题（基于关键词提取）"},
    {label: "自定义", description: "手动输入其他名称"}
  ]
}])
```

**展示要求（MANDATORY）**：

- 在用户确认简短标题时，除了给出选项，还必须把推荐或当前使用的简短标题单独展示为可复制文本
- 优先使用单独代码行或代码块展示，避免把标题埋在说明句里
- 若用户选择自定义标题，确认后也必须再次单独展示最终标题

**推荐展示格式：**

```text
请确认简短标题。可直接复制：

Ferroptosis-Cervical-Cancer
```

## CP 1 检查点

- [ ] 标题已提取并转换为 sentence case（仅首词和专有名词大写）
- [ ] 作者已提取
- [ ] 摘要已提取
- [ ] 关键词已提取并规范为目标格式（分号分隔，普通词小写）
- [ ] 简短标题已向用户以可复制文本明确展示
- [ ] 图片数量已统计
- [ ] 参考文献已提取
