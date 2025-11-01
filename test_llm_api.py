"""
简单测试LLM API连接
"""

import sys
sys.path.append('/mnt/user-data/outputs')

from llm_client import LLMClient


def test_basic_connection():
    """测试基本连接"""
    print("="*60)
    print("测试1: 基本连接")
    print("="*60)
    
    try:
        client = LLMClient(
            api_url="http://122.115.55.3:32800/v1/chat/completions",
            model="Qwen3_2507"
        )
        
        messages = [{"role": "user", "content": "你好，请回复'连接成功'"}]
        response = client.chat(messages, max_tokens=50)
        
        print(f"✅ 连接成功!")
        print(f"回复: {response}")
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def test_table_description():
    """测试表格描述生成"""
    print("\n" + "="*60)
    print("测试2: 表格描述生成")
    print("="*60)
    
    try:
        client = LLMClient()
        
        table_md = """| 模型 | 参数量 | 准确率 |
|------|--------|--------|
| BERT | 110M   | 85.2%  |
| GPT-3| 175B   | 92.1%  |
| T5   | 11B    | 88.5%  |"""
        
        print(f"输入表格:\n{table_md}\n")
        description = client.generate_table_description(table_md)
        print(f"生成的描述:\n{description}")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_summary_generation():
    """测试摘要生成"""
    print("\n" + "="*60)
    print("测试3: 摘要生成")
    print("="*60)
    
    try:
        client = LLMClient()
        
        text = """深度学习是机器学习的一个分支，它基于人工神经网络进行学习。
深度学习架构如深度神经网络、深度信念网络、递归神经网络和卷积神经网络
已被应用于包括计算机视觉、语音识别、自然语言处理、音频识别、社交网络过滤、
机器翻译、生物信息学和医学图像分析、材料检验和棋类游戏等领域。
这些应用中的一些已经达到了人类专家的表现水平。"""
        
        print(f"原文:\n{text}\n")
        summary = client.generate_summary(text, max_length=100)
        print(f"生成的摘要:\n{summary}")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_query_analysis():
    """测试查询分析"""
    print("\n" + "="*60)
    print("测试4: 查询意图分析")
    print("="*60)
    
    try:
        client = LLMClient()
        
        query = "比较BERT和GPT模型在文本分类任务上的性能差异"
        
        print(f"查询: {query}\n")
        intent = client.analyze_query_intent(query)
        
        import json
        print(f"意图分析结果:")
        print(json.dumps(intent, ensure_ascii=False, indent=2))
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_subquery_generation():
    """测试子查询生成"""
    print("\n" + "="*60)
    print("测试5: 子查询生成")
    print("="*60)
    
    try:
        client = LLMClient()
        
        query = "分析深度学习在医疗影像诊断中的应用效果和面临的挑战"
        
        print(f"原始查询: {query}\n")
        subqueries = client.generate_subqueries(query, max_subqueries=3)
        
        import json
        print(f"生成的子查询:")
        print(json.dumps(subqueries, ensure_ascii=False, indent=2))
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_report_generation():
    """测试报告生成"""
    print("\n" + "="*60)
    print("测试6: 报告生成")
    print("="*60)
    
    try:
        client = LLMClient()
        
        query = "深度学习的主要优势是什么？"
        evidence_list = [
            {
                'content': '深度学习能够自动学习特征表示，无需人工特征工程。',
                'doc_id': 'doc1',
                'relevance': 0.9
            },
            {
                'content': '深度神经网络可以处理大规模数据，在图像和语音识别任务中表现出色。',
                'doc_id': 'doc2',
                'relevance': 0.85
            },
            {
                'content': '深度学习模型具有强大的表达能力，可以学习复杂的非线性关系。',
                'doc_id': 'doc3',
                'relevance': 0.88
            }
        ]
        
        print(f"查询: {query}")
        print(f"证据数量: {len(evidence_list)}\n")
        
        report = client.generate_report(query, evidence_list)
        print(f"生成的报告:\n{report}")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("LLM API 完整测试套件")
    print("="*60)
    
    tests = [
        ("基本连接", test_basic_connection),
        ("表格描述生成", test_table_description),
        ("摘要生成", test_summary_generation),
        ("查询意图分析", test_query_analysis),
        ("子查询生成", test_subquery_generation),
        ("报告生成", test_report_generation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n测试出错: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n总计: {passed}/{total} 测试通过")
    
    return passed == total


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "basic":
        # 只测试基本连接
        test_basic_connection()
    else:
        # 运行所有测试
        success = run_all_tests()
        sys.exit(0 if success else 1)
