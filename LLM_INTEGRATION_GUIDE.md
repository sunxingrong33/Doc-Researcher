# Doc-Researcher with LLM API - 使用说明

## 📋 文件说明

### 核心文件

1. **llm_client.py** - LLM客户端封装
   - 封装了Qwen3 API调用
   - 提供各种专业功能（表格描述、摘要生成、意图分析等）
   - 包含重试和错误处理逻辑

2. **doc_researcher_with_llm.py** - 集成LLM的完整系统
   - 继承基础Doc-Researcher功能
   - 所有需要LLM的地方都使用真实API调用
   - 包含完整的演示代码

3. **test_llm_api.py** - API测试工具
   - 测试LLM连接
   - 测试各种功能
   - 验证API是否正常工作

## 🚀 快速开始

### 步骤1: 测试API连接

```bash
# 测试基本连接
python test_llm_api.py basic

# 运行完整测试
python test_llm_api.py
```

### 步骤2: 使用LLM客户端

```python
from llm_client import LLMClient

# 创建客户端
client = LLMClient(
    api_url="http://122.115.55.3:32800/v1/chat/completions",
    model="Qwen3_2507"
)

# 简单对话
response = client.chat([
    {"role": "user", "content": "你好"}
])
print(response)

# 生成表格描述
table_md = "| 列1 | 列2 |\n|-----|-----|\n| A   | B   |"
description = client.generate_table_description(table_md)

# 生成摘要
summary = client.generate_summary("长文本...")

# 分析查询意图
intent = client.analyze_query_intent("查询内容")

# 生成子查询
subqueries = client.generate_subqueries("复杂查询")
```

### 步骤3: 使用完整系统

```python
from doc_researcher_with_llm import LLMDocResearcher, LLMClient

# 创建LLM客户端
llm_client = LLMClient()

# 创建Doc-Researcher系统
researcher = LLMDocResearcher(
    llm_client=llm_client,
    max_iterations=3,
    sufficiency_threshold=0.7
)

# 添加文档
documents = ["paper1.pdf", "report.pdf"]
researcher.add_documents(documents)

# 执行研究
report = researcher.research("这些文档的主要发现是什么？")
print(report)

# 多轮对话
report2 = researcher.research("能详细解释一下第一个发现吗？")
print(report2)
```

## 🔧 API配置

### 基本配置

```python
client = LLMClient(
    api_url="http://122.115.55.3:32800/v1/chat/completions",  # API地址
    model="Qwen3_2507",           # 模型名称
    timeout=1200,                 # 超时时间（秒）
    max_retries=3                 # 最大重试次数
)
```

### 调用参数

```python
response = client.chat(
    messages=[...],           # 消息列表
    temperature=0,            # 温度 (0-1, 0=确定性)
    top_p=1,                  # top_p采样
    max_tokens=4000,          # 最大token数
    system_prompt="..."       # 系统提示（可选）
)
```

## 📊 LLM客户端功能详解

### 1. 基础对话

```python
client = LLMClient()

# 简单问答
response = client.chat([
    {"role": "user", "content": "什么是深度学习？"}
])

# 带系统提示
response = client.chat(
    messages=[{"role": "user", "content": "介绍深度学习"}],
    system_prompt="你是一位AI专家"
)
```

### 2. 表格描述生成

```python
table_markdown = """
| 模型 | 准确率 | 速度 |
|------|--------|------|
| A    | 85%    | 快   |
| B    | 90%    | 慢   |
"""

description = client.generate_table_description(table_markdown)
# 返回格式:
# [粗粒度描述]
# 表格对比了两个模型的性能。
# [细粒度描述]
# 表格包含3列：模型、准确率、速度...
```

### 3. 图片描述生成

```python
# 基于上下文生成图片描述
description = client.generate_figure_description(
    figure_context="图1: 系统架构图"
)
```

### 4. 摘要生成

```python
long_text = """很长的文档内容..."""

summary = client.generate_summary(
    full_text=long_text,
    max_length=200  # 摘要最大长度
)
```

### 5. 查询意图分析

```python
query = "比较BERT和GPT在文本分类任务上的表现"

intent = client.analyze_query_intent(query)
# 返回:
# {
#     "intent_type": "comparison",
#     "granularity": "chunk",
#     "complexity": "medium",
#     "needs_multi_doc": true
# }
```

### 6. 子查询生成

```python
complex_query = "分析深度学习在医疗领域的应用、挑战和未来发展"

subqueries = client.generate_subqueries(
    query=complex_query,
    max_subqueries=3
)
# 返回:
# [
#     "深度学习在医疗领域的具体应用",
#     "深度学习在医疗领域面临的挑战",
#     "深度学习在医疗领域的未来发展趋势"
# ]
```

### 7. 信息充分性评估

```python
query = "深度学习的优势"
retrieved_contents = [
    "深度学习可以自动学习特征",
    "深度学习在图像识别表现出色"
]

sufficiency = client.evaluate_information_sufficiency(
    query=query,
    retrieved_contents=retrieved_contents
)
# 返回: 0.0-1.0之间的分数
```

### 8. 报告生成

```python
query = "深度学习的应用"
evidence_list = [
    {
        'content': '深度学习在计算机视觉领域应用广泛',
        'doc_id': 'doc1',
        'relevance': 0.9
    },
    # ...更多证据
]

report = client.generate_report(
    query=query,
    evidence_list=evidence_list,
    conversation_history=[...]  # 可选
)
```

## 🏗️ 完整系统架构

```
用户查询
   ↓
LLMPlannerAgent (使用LLM分析意图)
   ├── 文档过滤
   ├── 粒度选择 (基于LLM分析)
   └── 子查询生成 (使用LLM)
   ↓
迭代循环
   ├── SearcherAgent (检索)
   ├── LLMRefinerAgent (精炼)
   └── 充分性评估 (使用LLM)
   ↓
LLMReporterAgent (使用LLM生成报告)
   ↓
研究报告
```

## 💡 使用技巧

### 1. 错误处理

```python
from llm_client import LLMClient

try:
    client = LLMClient()
    response = client.chat([...])
except Exception as e:
    print(f"LLM调用失败: {e}")
    # 处理错误或使用默认值
```

### 2. 超时设置

```python
# 对于复杂任务，增加超时时间
client = LLMClient(timeout=1800)  # 30分钟

# 对于简单任务，可以缩短
client = LLMClient(timeout=300)   # 5分钟
```

### 3. 温度调节

```python
# 确定性任务（摘要、分析）
response = client.chat(messages, temperature=0)

# 创意性任务（生成描述）
response = client.chat(messages, temperature=0.7)
```

### 4. Token限制

```python
# 短回答
response = client.chat(messages, max_tokens=500)

# 长报告
response = client.chat(messages, max_tokens=2000)
```

## 📈 性能优化

### 1. 批量处理

```python
# 不好 - 串行处理
for doc in documents:
    summary = client.generate_summary(doc)

# 好 - 批量准备后处理
summaries = []
for doc in documents:
    summaries.append(client.generate_summary(doc))
```

### 2. 缓存结果

```python
import json

# 缓存摘要
cache = {}
def get_summary_cached(text):
    text_hash = hash(text)
    if text_hash not in cache:
        cache[text_hash] = client.generate_summary(text)
    return cache[text_hash]
```

### 3. 并行调用

```python
from concurrent.futures import ThreadPoolExecutor

def process_document(doc):
    return client.generate_summary(doc)

with ThreadPoolExecutor(max_workers=3) as executor:
    summaries = list(executor.map(process_document, documents))
```

## 🐛 常见问题

### Q1: API连接失败

```
错误: requests.exceptions.ConnectionError
```

**解决方案:**
1. 检查API地址是否正确
2. 确认网络连接
3. 验证API服务是否运行
4. 尝试手动curl测试

```bash
curl -X POST http://122.115.55.3:32800/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3_2507",
    "messages": [{"role": "user", "content": "测试"}],
    "max_tokens": 50
  }'
```

### Q2: 超时错误

```
错误: requests.exceptions.Timeout
```

**解决方案:**
1. 增加timeout参数
2. 减少max_tokens
3. 简化查询

### Q3: JSON解析错误

```
错误: json.JSONDecodeError
```

**解决方案:**
1. 检查API返回格式
2. 使用更明确的提示词
3. 添加额外的错误处理

### Q4: 内容被截断

**解决方案:**
```python
# 增加max_tokens
response = client.chat(messages, max_tokens=4000)
```

## 📝 最佳实践

### 1. 提示词工程

```python
# 好的提示词
system_prompt = """你是一位专业的文档分析专家。
要求:
1. 提供准确的分析
2. 使用结构化格式
3. 保持客观中立"""

# 不好的提示词
system_prompt = "分析文档"
```

### 2. 错误恢复

```python
def safe_llm_call(func, *args, default=None, **kwargs):
    """安全的LLM调用，带默认值"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"LLM调用失败: {e}")
        return default

# 使用
summary = safe_llm_call(
    client.generate_summary,
    text,
    default="摘要生成失败"
)
```

### 3. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在LLM调用前后记录
logger.info(f"调用LLM: {query}")
response = client.chat(messages)
logger.info(f"LLM响应长度: {len(response)}")
```

## 🔍 调试技巧

### 1. 打印中间结果

```python
# 查看LLM实际发送的内容
print(f"发送给LLM的消息: {messages}")

# 查看原始响应
response = client.chat(messages)
print(f"LLM原始响应: {response}")
```

### 2. 使用测试模式

```python
# 创建测试客户端
test_client = LLMClient(timeout=60)  # 短超时用于测试

# 简单测试
try:
    response = test_client.chat([
        {"role": "user", "content": "测试"}
    ], max_tokens=10)
    print("✅ API正常工作")
except Exception as e:
    print(f"❌ API异常: {e}")
```

## 📚 示例代码

完整的使用示例请参考:
- `test_llm_api.py` - API测试示例
- `doc_researcher_with_llm.py` - 完整系统示例

## 🎯 下一步

1. 运行测试验证API连接
2. 尝试基本的LLM调用
3. 使用完整的Doc-Researcher系统
4. 根据需要调整参数和提示词

---

**需要帮助?** 
- 查看测试脚本获取更多示例
- 检查API文档了解更多参数
- 调整提示词以获得更好的结果
