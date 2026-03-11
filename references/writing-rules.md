# 大文件写入规则（全局约束）

当 HTML 文件超过30 KB 时，**禁止使用 write 工具**，必须使用 Python 分段写入：

```python
python3 << 'PYEOF'
content = '''<!DOCTYPE html>…'''
with open('/path/to/output.html', 'w', encoding='utf-8') as f:
    f.write(content)
PYEOF

# 追加模式
python3 << 'PYEOF'
content = '''…更多内容…'''
with open('/path/to/output.html', 'a', encoding='utf-8') as f:
    f.write(content)
PYEOF
```
