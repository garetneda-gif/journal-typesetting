# 第2步：收集图片 URL

## 2.1 列出检测到的图片

**输出格式**：

```
检测到 4 张图片：
1. Figure 1 - The flowchart of the study
2. Figure 2 - Venny Plot
3. Figure 3 - Comprehensive analysis of gene expression signatures
4. Figure 4 - Enrichment analysis of key biological pathways
```

## 2.2 提供清晰的 URL 配置选项

```javascript
question(questions=[{
  header: "图片URL配置",
  question: "文档中共有 4 张图片，请选择URL配置方式",
  options: [
    {
      label: "使用默认URL格式（推荐）",
      description: "https://medbam.org/assets/Ferroptosis-Cervical-Cancer（此前确定的简短标题）/Figure 1.png（注意：有空格）"
    },
    {
      label: "自定义基础路径",
      description: "指定基础URL，图片文件名保持为 Figure 1.png, Figure 2.png 等"
    },
    {
      label: "逐一输入每张图片URL",
      description: "完全自定义每张图片的URL"
    }
  ]
}])
```

## 2.3 根据用户选择收集 URL

**选项1：默认格式**

```
自动生成：
- https://medbam.org/assets/Ferroptosis-Cervical-Cancer（此前确定的简短标题）/Figure 1.png
……
```

**选项2：自定义基础路径**

```javascript
question(questions=[{
  header: "基础URL",
  question: "请输入图片基础URL（末尾不要加/）",
  options: [
    {label: "https://your-cdn.com/papers/2024", description: "示例格式"},
    {label: "自定义", description: "输入其他URL"}
  ]
}])

// 然后自动生成：
// {base_url}/Figure 1.png
// {base_url}/Figure 2.png
// ...
```

**选项3：逐一输入**

```
依次询问每张图片的完整URL（显示图片说明作为参考）
```

## CP 2 检查点

- [ ] 所有图片都有 URL
- [ ] URL 格式正确（包含协议、扩展名）
- [ ] 没有明显错误（如双斜杠、缺少扩展名等）
