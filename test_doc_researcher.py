"""
Doc-Researcher 测试脚本
展示系统各组件的工作流程
"""

import sys
sys.path.append('/home/claude')

from doc_researcher import (
    DocResearcher,
    MultimodalParser,
    RetrievalSystem,
    LayoutElement,
    LayoutType,
    BoundingBox,
    Granularity
)


def test_bounding_box():
    """测试边界框功能"""
    print("\n" + "="*60)
    print("测试1: 边界框计算")
    print("="*60)
    
    bbox1 = BoundingBox(0, 0, 100, 100)
    bbox2 = BoundingBox(50, 50, 150, 150)
    
    print(f"边界框1: ({bbox1.x1}, {bbox1.y1}) - ({bbox1.x2}, {bbox1.y2})")
    print(f"边界框2: ({bbox2.x1}, {bbox2.y1}) - ({bbox2.x2}, {bbox2.y2})")
    print(f"边界框1面积: {bbox1.area()}")
    print(f"边界框2面积: {bbox2.area()}")
    print(f"重叠率: {bbox1.overlap(bbox2):.2%}")


def test_layout_element():
    """测试布局元素"""
    print("\n" + "="*60)
    print("测试2: 布局元素")
    print("="*60)
    
    # 创建不同类型的布局元素
    text_element = LayoutElement(
        doc_id="test_doc",
        page_id=1,
        sequence_id=1,
        element_type=LayoutType.TEXT,
        bbox=BoundingBox(50, 100, 500, 200),
        content="这是一段文本内容，讨论了深度学习模型的架构设计。"
    )
    
    table_element = LayoutElement(
        doc_id="test_doc",
        page_id=1,
        sequence_id=2,
        element_type=LayoutType.TABLE,
        bbox=BoundingBox(50, 250, 500, 400),
        content="[粗粒度] 表格展示了实验结果。\n[细粒度] 包含准确率、召回率等指标。",
        raw_content="| 方法 | 准确率 | 召回率 |\n|------|--------|--------|\n| A    | 0.85   | 0.82   |"
    )
    
    figure_element = LayoutElement(
        doc_id="test_doc",
        page_id=1,
        sequence_id=3,
        element_type=LayoutType.FIGURE,
        bbox=BoundingBox(50, 450, 500, 650),
        content="[粗粒度] 系统架构图。\n[细粒度] 包含5个主要模块，从输入到输出的流程。"
    )
    
    elements = [text_element, table_element, figure_element]
    
    for elem in elements:
        print(f"\n元素类型: {elem.element_type.value}")
        print(f"页面: {elem.page_id}, 序列: {elem.sequence_id}")
        print(f"位置: {elem.bbox.x1},{elem.bbox.y1} - {elem.bbox.x2},{elem.bbox.y2}")
        print(f"内容: {elem.content[:50]}...")


def test_chunking():
    """测试文档分块"""
    print("\n" + "="*60)
    print("测试3: 智能分块")
    print("="*60)
    
    parser = MultimodalParser(max_chunk_length=200)
    
    # 模拟布局元素
    elements = [
        LayoutElement(
            doc_id="test", page_id=1, sequence_id=i,
            element_type=LayoutType.TEXT,
            bbox=BoundingBox(50, 100*i, 500, 100*(i+1)),
            content=f"这是第{i+1}段文本。" * 20  # 生成较长的文本
        )
        for i in range(5)
    ]
    
    chunks = parser._create_layout_aware_chunks(elements, "test_doc")
    
    print(f"原始元素数: {len(elements)}")
    print(f"生成块数: {len(chunks)}")
    
    for chunk in chunks:
        print(f"\n块 {chunk.chunk_id}:")
        print(f"  - 页面: {chunk.page_id}")
        print(f"  - 包含元素: {len(chunk.layout_elements)}")
        print(f"  - 内容长度: {len(chunk.content)} 字符")
        print(f"  - 内容预览: {chunk.content[:50]}...")


def test_retrieval_granularity():
    """测试多粒度检索"""
    print("\n" + "="*60)
    print("测试4: 多粒度检索")
    print("="*60)
    
    # 创建检索系统
    retrieval = RetrievalSystem(paradigm="hybrid")
    
    # 创建模拟文档
    parser = MultimodalParser()
    doc = parser.parse_document("test.pdf", "test_doc")
    
    # 索引文档
    retrieval.index_document(doc)
    
    print(f"索引的条目数: {len(retrieval.index)}")
    
    # 展示不同类型的索引
    for key, item in list(retrieval.index.items())[:5]:
        print(f"\n索引键: {key}")
        print(f"  - 类型: {item['type']}")
        print(f"  - 文档ID: {item['doc_id']}")
        print(f"  - 内容长度: {len(item['content'])} 字符")
    
    # 测试检索
    query = "深度学习"
    
    for granularity in Granularity:
        results = retrieval.retrieve(query, granularity, top_k=2)
        print(f"\n{granularity.value} 粒度检索: {len(results)} 个结果")
        for result in results:
            print(f"  - 相关性: {result['score']:.2f}")


def test_agents_workflow():
    """测试智能体工作流"""
    print("\n" + "="*60)
    print("测试5: 智能体协作流程")
    print("="*60)
    
    from doc_researcher import (
        PlannerAgent,
        SearcherAgent,
        RefinerAgent,
        ReporterAgent
    )
    
    # 创建模拟环境
    retrieval = RetrievalSystem()
    parser = MultimodalParser()
    
    # 创建几个文档
    docs = {}
    for i in range(3):
        doc = parser.parse_document(f"doc{i}.pdf", f"doc_{i}")
        retrieval.index_document(doc)
        docs[f"doc_{i}"] = doc
    
    # 创建智能体
    planner = PlannerAgent()
    searcher = SearcherAgent(retrieval)
    refiner = RefinerAgent()
    reporter = ReporterAgent()
    
    # 测试查询
    query = "比较这些文档的主要发现"
    history = []
    
    print(f"\n查询: {query}\n")
    
    # 步骤1: 规划
    print("【步骤1: 规划】")
    plan = planner.plan(query, history, docs)
    print(f"- 过滤后文档数: {len(plan['relevant_docs'])}")
    print(f"- 选择的粒度: {plan['granularity'].value}")
    print(f"- 生成的子查询数: {len(plan['subqueries'])}")
    
    # 步骤2: 搜索
    print("\n【步骤2: 搜索】")
    results = searcher.search(
        plan['subqueries'],
        plan['granularity'],
        plan['relevant_docs']
    )
    print(f"- 检索到 {len(results)} 个结果")
    
    # 步骤3: 精炼
    print("\n【步骤3: 精炼】")
    refined = refiner.refine(results, query)
    print(f"- 精炼后剩余 {len(refined)} 个结果")
    sufficiency = refiner.evaluate_sufficiency(refined, query)
    print(f"- 信息充分性: {sufficiency:.2%}")
    
    # 步骤4: 生成报告
    print("\n【步骤4: 生成报告】")
    report = reporter.generate_report(query, refined, history)
    print(f"- 报告长度: {len(report)} 字符")
    print(f"\n生成的报告:\n{'-'*60}\n{report[:300]}...")


def test_end_to_end():
    """端到端测试"""
    print("\n" + "="*60)
    print("测试6: 端到端深度研究")
    print("="*60)
    
    # 创建系统
    researcher = DocResearcher(
        max_iterations=2,
        sufficiency_threshold=0.5
    )
    
    # 添加文档
    print("\n【阶段1: 添加文档】")
    docs = ["paper1.pdf", "paper2.pdf"]
    researcher.add_documents(docs)
    print(f"已添加 {len(docs)} 个文档")
    
    # 执行研究
    print("\n【阶段2: 执行研究】")
    queries = [
        "这些论文的主要贡献是什么?",
        "实验结果如何?"
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        report = researcher.research(query)
        print(f"报告长度: {len(report)} 字符")
        print(f"对话历史长度: {len(researcher.conversation_history)}")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Doc-Researcher 系统测试套件")
    print("="*60)
    
    tests = [
        test_bounding_box,
        test_layout_element,
        test_chunking,
        test_retrieval_granularity,
        test_agents_workflow,
        test_end_to_end
    ]
    
    for i, test in enumerate(tests, 1):
        try:
            test()
            print(f"\n✅ 测试 {i} 通过")
        except Exception as e:
            print(f"\n❌ 测试 {i} 失败: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
