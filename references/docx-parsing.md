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
| 关键词   | "Keywords: "开头的行                        |
| 正文章节 | 编号标题（1 INTRODUCTION, 2 METHODS 等）    |
| 图片     | 图片对象或 `[Figure N]` 占位符            |
| 表格     | Word 表格对象                               |
| 参考文献 | "REFERENCES"后的编号列表                    |

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

## CP 1 检查点

- [ ] 标题已提取
- [ ] 作者已提取
- [ ] 摘要已提取
- [ ] 图片数量已统计
- [ ] 参考文献已提取
