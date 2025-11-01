"""
Doc-Researcher 使用示例和说明

这个实现基于论文:
"Doc-Researcher: A Unified System for Multimodal Document Parsing and Deep Research"
"""

from doc_researcher import (
    DocResearcher, 
    MultimodalParser,
    RetrievalSystem,
    Granularity
)


def example_1_basic_usage():
    """示例1: 基础使用"""
    print("\n" + "="*60)
    print("示例1: 基础文档研究")
    print("="*60)
    
    # 1. 创建Doc-Researcher系统
    researcher = DocResearcher(
        max_iterations=3,           # 最大迭代次数
        sufficiency_threshold=0.7   # 信息充分性阈值
    )
    
    # 2. 添加文档
    documents = [
        "research_paper_1.pdf",
        "technical_report.pdf",
        "market_analysis.pdf"
    ]
    researcher.add_documents(documents)
    
    # 3. 执行研究查询
    query = "这些文档中讨论的主要AI技术有哪些?"
    report = researcher.research(query)
    
    print("\n研究报告:")
    print(report)


def example_2_multi_turn_conversation():
    """示例2: 多轮对话研究"""
    print("\n" + "="*60)
    print("示例2: 多轮对话研究")
    print("="*60)
    
    researcher = DocResearcher()
    
    # 添加文档
    researcher.add_documents(["insurance_policy_1.pdf", "insurance_policy_2.pdf"])
    
    # 第一轮查询
    query1 = "这两份保险的保费是多少?"
    report1 = researcher.research(query1)
    print(f"\n查询1: {query1}")
    print(f"回答1: {report1}")
    
    # 第二轮查询(基于对话历史)
    query2 = "如果选择非面板医院,自付费用会有什么变化?"
    report2 = researcher.research(query2)
    print(f"\n查询2: {query2}")
    print(f"回答2: {report2}")


def example_3_document_parsing():
    """示例3: 文档解析"""
    print("\n" + "="*60)
    print("示例3: 多模态文档解析")
    print("="*60)
    
    # 创建解析器
    parser = MultimodalParser(max_chunk_length=512)
    
    # 解析文档
    document = parser.parse_document("example.pdf", "doc_001")
    
    # 查看解析结果
    print(f"\n文档ID: {document.doc_id}")
    print(f"标题: {document.title}")
    print(f"页面数: {len(document.pages)}")
    print(f"块数量: {len(document.chunks)}")
    print(f"布局元素数: {len(document.layout_elements)}")
    
    # 查看第一个块的内容
    if document.chunks:
        chunk = document.chunks[0]
        print(f"\n第一个块:")
        print(f"  - 块ID: {chunk.chunk_id}")
        print(f"  - 页面: {chunk.page_id}")
        print(f"  - 内容预览: {chunk.content[:100]}...")
        print(f"  - 布局元素数: {len(chunk.layout_elements)}")


def example_4_retrieval_system():
    """示例4: 检索系统"""
    print("\n" + "="*60)
    print("示例4: 多模态检索")
    print("="*60)
    
    # 创建检索系统
    retrieval = RetrievalSystem(paradigm="hybrid")
    
    # 解析并索引文档
    parser = MultimodalParser()
    doc = parser.parse_document("paper.pdf", "paper_001")
    retrieval.index_document(doc)
    
    # 执行不同粒度的检索
    query = "深度学习模型的性能评估"
    
    # 块级别检索
    chunk_results = retrieval.retrieve(query, Granularity.CHUNK, top_k=5)
    print(f"\n块级别检索结果: {len(chunk_results)} 个")
    
    # 页面级别检索
    page_results = retrieval.retrieve(query, Granularity.PAGE, top_k=5)
    print(f"页面级别检索结果: {len(page_results)} 个")
    
    # 摘要级别检索
    summary_results = retrieval.retrieve(query, Granularity.SUMMARY, top_k=5)
    print(f"摘要级别检索结果: {len(summary_results)} 个")


def example_5_complex_research():
    """示例5: 复杂研究场景"""
    print("\n" + "="*60)
    print("示例5: 复杂多文档研究")
    print("="*60)
    
    researcher = DocResearcher(
        max_iterations=5,
        sufficiency_threshold=0.75
    )
    
    # 添加多个领域的文档
    documents = [
        # 学术论文
        "transformer_paper.pdf",
        "bert_paper.pdf",
        "gpt_paper.pdf",
        # 技术报告
        "ai_market_report_2024.pdf",
        "nlp_benchmark_report.pdf",
        # 产品文档
        "product_spec_v1.pdf",
        "product_spec_v2.pdf"
    ]
    researcher.add_documents(documents)
    
    # 执行复杂的多跳推理查询
    query = """
    比较Transformer、BERT和GPT三种架构的性能差异,
    并分析它们在实际产品中的应用情况和市场表现。
    """
    
    report = researcher.research(query)
    print("\n复杂研究报告:")
    print(report)


def architecture_overview():
    """系统架构说明"""
    print("\n" + "="*60)
    print("Doc-Researcher 系统架构")
    print("="*60)
    
    overview = """
    
    ┌─────────────────────────────────────────────────────────────┐
    │                    Doc-Researcher 系统                       │
    └─────────────────────────────────────────────────────────────┘
    
    【离线阶段: 深度文档解析和索引】
    
    1. MultimodalParser (多模态解析器)
       ├── 布局感知解析 (使用 MinerU)
       ├── 视觉元素转文本 (使用 VLM)
       │   ├── 图片 → 描述
       │   ├── 表格 → 结构化文本
       │   └── 公式 → LaTeX
       └── 智能分块
           ├── 布局感知分块
           └── 多粒度表示 (chunk/page/full/summary)
    
    2. RetrievalSystem (检索系统)
       ├── 文本检索 (Text-only)
       ├── 视觉检索 (Vision-only)
       └── 混合检索 (Hybrid)
    
    【在线阶段: 深度研究工作流】
    
    3. PlannerAgent (规划器)
       ├── 文档过滤 (基于摘要)
       ├── 粒度选择 (chunk/page/full/summary)
       └── 子查询生成
    
    4. SearcherAgent (搜索器)
       └── 执行多模态检索
    
    5. RefinerAgent (精炼器)
       ├── 去重
       ├── 相关性过滤
       ├── 重新排序
       └── 信息充分性评估
    
    6. ReporterAgent (报告生成器)
       ├── 证据组织
       ├── 答案合成
       └── 引用标注
    
    【迭代循环】
    
    while 信息不充分 and 未达到最大迭代次数:
        搜索 → 精炼 → 评估 → (生成新查询)
    
    """
    print(overview)


def key_features():
    """关键特性说明"""
    print("\n" + "="*60)
    print("核心特性")
    print("="*60)
    
    features = """
    
    【1. 深度多模态解析】
    ✓ 保留布局结构和视觉语义
    ✓ 处理文本、表格、图片、公式
    ✓ 多粒度表示(块/页面/全文/摘要)
    ✓ 精确的位置定位(边界框坐标)
    
    【2. 系统化检索架构】
    ✓ 支持三种检索范式:
      - Text-only: 轻量级,适合文本密集型文档
      - Vision-only: 无需解析,保留视觉完整性
      - Hybrid: 结合两者优势
    ✓ 自适应粒度选择
    ✓ 多查询聚合和重排序
    
    【3. 深度研究工作流】
    ✓ 智能查询规划
    ✓ 迭代搜索-精炼循环
    ✓ 渐进式证据积累
    ✓ 信息充分性评估
    ✓ 多轮对话支持
    
    【4. M4DocBench 评估】
    ✓ Multi-modal: 跨模态证据
    ✓ Multi-hop: 多跳推理
    ✓ Multi-document: 多文档综合
    ✓ Multi-turn: 多轮交互
    
    """
    print(features)


def performance_tips():
    """性能优化建议"""
    print("\n" + "="*60)
    print("性能优化建议")
    print("="*60)
    
    tips = """
    
    【解析阶段优化】
    1. 一次性预处理: 将视觉元素转换为文本,避免重复处理
    2. 批量处理: 批量调用VLM API以提高效率
    3. 缓存策略: 缓存解析结果,避免重复解析
    
    【检索阶段优化】
    1. 向量索引: 使用FAISS、Milvus等向量数据库
    2. 混合检索: 结合稀疏(BM25)和密集(embedding)检索
    3. 量化压缩: 对嵌入向量进行量化以减少存储
    4. GPU加速: 使用GPU进行批量嵌入计算
    
    【研究阶段优化】
    1. 早停策略: 信息充分时提前终止迭代
    2. 并行处理: 并行执行多个子查询
    3. 增量更新: 增量式添加新证据,避免重复处理
    4. 上下文管理: 智能截断长对话历史
    
    【成本控制】
    1. 深度解析 vs 解析免费的权衡:
       - 深度解析: 高质量但慢(~2.5小时/304文档)
       - 解析免费: 快速但质量较低(~9-39分钟)
    2. 向量存储优化:
       - 密集向量: 高质量,低存储(1024-2048维)
       - 多向量: 超高质量,高存储(需要特殊支持)
    3. LLM调用优化:
       - 批量处理减少API调用
       - 使用较小模型处理简单任务
       - 缓存常见查询结果
    
    """
    print(tips)


def comparison_with_baselines():
    """与基线系统的对比"""
    print("\n" + "="*60)
    print("与现有系统的对比")
    print("="*60)
    
    comparison = """
    
    ┌──────────────────┬─────────┬──────────┬─────────┬──────────┐
    │     系统         │  解析   │   检索   │  迭代   │  准确率  │
    ├──────────────────┼─────────┼──────────┼─────────┼──────────┤
    │ Direct (无RAG)   │   -     │    -     │   -     │  5-10%   │
    │ Long-context     │ Shallow │    -     │   -     │  9-32%   │
    │ MDocAgent        │ Shallow │  Hybrid  │   ✗     │  15.8%   │
    │ M3DocRAG         │  Free   │  Vision  │   ✗     │  7.0%    │
    │ ColQwen-gen      │  Free   │  Vision  │   ✗     │  5.7%    │
    │ Doc-Researcher   │  Deep   │  Hybrid  │   ✓     │  50.6%   │
    └──────────────────┴─────────┴──────────┴─────────┴──────────┘
    
    【关键发现】
    
    1. 深度解析的重要性:
       - Shallow解析: 34-39% 准确率
       - Deep解析: 42-50% 准确率
       - 提升 +11.4%
    
    2. 迭代工作流的价值:
       - 单轮检索: 15.8% (MDocAgent)
       - 迭代搜索: 50.6% (Doc-Researcher)
       - 提升 3.4倍
    
    3. 混合检索的优势:
       - Text-only: 39-45%
       - Vision-only: 36-43%
       - Hybrid: 42-50%
       - 提升 3-5%
    
    4. 规划器的作用:
       - 有规划器: 47.5%
       - 无规划器: 39.2%
       - 提升 8.3%
    
    """
    print(comparison)


if __name__ == "__main__":
    print("="*60)
    print("Doc-Researcher 系统演示")
    print("基于论文: Doc-Researcher: A Unified System for")
    print("          Multimodal Document Parsing and Deep Research")
    print("="*60)
    
    # 显示系统架构
    architecture_overview()
    
    # 显示核心特性
    key_features()
    
    # 显示性能对比
    comparison_with_baselines()
    
    # 显示优化建议
    performance_tips()
    
    print("\n" + "="*60)
    print("运行示例")
    print("="*60)
    
    # 运行基础示例
    example_1_basic_usage()
    
    # 可以取消注释以运行其他示例:
    # example_2_multi_turn_conversation()
    # example_3_document_parsing()
    # example_4_retrieval_system()
    # example_5_complex_research()
