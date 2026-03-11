# 第0步：依赖检查（MANDATORY - 阻塞性）

## 硬约束：docx skill 必须可用，MCP 检查不可跳过

**检查顺序**：

```
┌─────────────────────────────────────────────────────────────┐
│ 步骤0: 依赖检查                                             │
├─────────────────────────────────────────────────────────────┤
│ 1️⃣ docx skill（阻塞性 - 必须可用）                         │
│    └─ ❌ 失败 → 立即中止，提示用户安装                      │
├─────────────────────────────────────────────────────────────┤
│ 2️⃣ PubMed MCP（非阻塞 - 记录状态）                         │
│    └─ ❌ 失败 → 降级为仅用Google Scholar                   │
├─────────────────────────────────────────────────────────────┤
│ 3️⃣ Crossref MCP（非阻塞 - 记录状态）                       │
│    └─ ❌ 失败 → 降级为仅用DOI提取+Google Scholar           │
└─────────────────────────────────────────────────────────────┘
```

## 0.1 docx skill 检查（阻塞性）

```python
# 检查docx skill是否可用
try:
    # 尝试调用docx相关功能
    result = skill('docx')
    docx_skill_available = True
    print("✅ docx skill 可用")
except Exception as e:
    docx_skill_available = False
    print(f"❌ docx skill 不可用: {e}")
    print("\n请安装docx skill后重试：")
    print("  opencode skill add docx")
    raise Exception("缺少必要依赖：docx skill")
```

**失败处理**：docx skill 是核心依赖，不可用则立即中止流程。

## 0.2 MCP 可用性检查

```python
# 测试PubMed MCP
pubmed_test_passed = False
try:
    result = pubmed_search_pubmed_key_words(key_words="test", num_results=1)
    pubmed_test_passed = True
    print("✅ PubMed MCP 可用")
except Exception as e:
    print(f"⚠️ PubMed MCP 不可用: {e}")

# 测试Crossref MCP
crossref_test_passed = False
try:
    result = crossref_search_works_by_query(query="test", limit=1)
    crossref_test_passed = True
    print("✅ Crossref MCP 可用")
except Exception as e:
    print(f"⚠️ Crossref MCP 不可用: {e}")
```

## 0.3 根据结果决定流程

| MCP 状态        | docx 状态 | 处理方式           | 参考文献策略                             |
| --------------- | --------- | ------------------ | ---------------------------------------- |
| ✅ 两者都可用   | ✅ 可用   | **完整流程** | DOI + PubMed + Crossref + Google Scholar |
| ⚠️ 仅一个可用 | ✅ 可用   | **部分流程** | DOI + 可用 MCP + Google Scholar          |
| ❌ 都不可用     | ✅ 可用   | **降级流程** | 仅 DOI 提取 + Google Scholar             |
| 任意            | ❌ 不可用 | **中止**     | 无法继续                                 |

## 0.4 MCP 不可用时的用户提示

```
⚠️ MCP服务不可用

检测结果：
- docx skill: ✅ 可用（核心功能正常）
- PubMed MCP: ❌ 不可用
- Crossref MCP: ❌ 不可用

影响：参考文献将只包含Google Scholar链接（无PubMed和Crossref链接）

选项：
1. 继续（使用fallback方案，仅Google Scholar链接）
2. 中止（我先安装MCP）

安装命令：
  claude mcp add pubmed -- npx -y @cyanheads/pubmed-mcp-server
  claude mcp add crossref -- npx -y @botanicastudios/crossref-mcp
```

## CP 0 检查点

- [ ] Docx skill 可用性已确认（阻塞性）
- [ ] PubMed MCP 状态已记录到变量
- [ ] Crossref MCP 状态已记录到变量
- [ ] 流程模式已确定（完整/部分/降级）
