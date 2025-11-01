"""
Doc-Researcher with LLM Integration
集成了真实LLM API调用的完整版本
"""

import sys
sys.path.append('/mnt/user-data/outputs')

from doc_researcher import (
    Granularity, LayoutType, BoundingBox, LayoutElement,
    Chunk, Document, SearchResult
)
from llm_client import LLMClient
from typing import List, Dict, Any, Optional
import json


class LLMMultimodalParser:
    """集成LLM的多模态文档解析器"""
    
    def __init__(self, llm_client: LLMClient, max_chunk_length: int = 512):
        """
        初始化解析器
        
        Args:
            llm_client: LLM客户端
            max_chunk_length: 最大块长度
        """
        self.llm = llm_client
        self.max_chunk_length = max_chunk_length
    
    def parse_document(self, doc_path: str, doc_id: str) -> Document:
        """
        解析文档
        
        Args:
            doc_path: 文档路径
            doc_id: 文档ID
            
        Returns:
            解析后的文档对象
        """
        print(f"正在解析文档: {doc_id}")
        
        # 步骤1: 提取布局元素（这里简化模拟）
        layout_elements = self._extract_layout_elements(doc_path, doc_id)
        
        # 步骤2: 使用LLM转换视觉元素为文本
        self._transcribe_visual_elements(layout_elements)
        
        # 步骤3: 创建布局感知的文档块
        chunks = self._create_layout_aware_chunks(layout_elements, doc_id)
        
        # 步骤4: 生成多粒度表示
        full_text = self._generate_full_text(layout_elements)
        summary = self.llm.generate_summary(full_text)  # 使用LLM生成摘要
        pages = self._organize_by_pages(layout_elements)
        
        return Document(
            doc_id=doc_id,
            title=f"Document {doc_id}",
            full_text=full_text,
            summary=summary,
            pages=pages,
            chunks=chunks,
            layout_elements=layout_elements
        )
    
    def _extract_layout_elements(self, doc_path: str, doc_id: str) -> List[LayoutElement]:
        """提取布局元素（模拟）"""
        elements = [
            LayoutElement(
                doc_id=doc_id,
                page_id=1,
                sequence_id=1,
                element_type=LayoutType.TEXT,
                bbox=BoundingBox(50, 100, 500, 200),
                content="这篇文档介绍了深度学习在自然语言处理中的应用，包括Transformer架构、预训练模型和微调技术。"
            ),
            LayoutElement(
                doc_id=doc_id,
                page_id=1,
                sequence_id=2,
                element_type=LayoutType.TABLE,
                bbox=BoundingBox(50, 250, 500, 400),
                content="",
                raw_content="| 模型 | 参数量 | GLUE得分 |\n|------|--------|----------|\n| BERT | 110M   | 80.5     |\n| GPT  | 117M   | 82.1     |"
            ),
            LayoutElement(
                doc_id=doc_id,
                page_id=1,
                sequence_id=3,
                element_type=LayoutType.FIGURE,
                bbox=BoundingBox(50, 450, 500, 650),
                content="",
            ),
        ]
        return elements
    
    def _transcribe_visual_elements(self, elements: List[LayoutElement]):
        """使用LLM转换视觉元素为文本"""
        for element in elements:
            if element.element_type == LayoutType.TABLE and element.raw_content:
                print(f"  - 使用LLM生成表格描述...")
                element.content = self.llm.generate_table_description(element.raw_content)
            elif element.element_type == LayoutType.FIGURE:
                print(f"  - 使用LLM生成图片描述...")
                element.content = self.llm.generate_figure_description()
            elif element.element_type == LayoutType.EQUATION:
                element.content = r"$f(x) = \sum_{i=1}^{n} w_i \cdot x_i + b$"
    
    def _create_layout_aware_chunks(self, elements: List[LayoutElement], doc_id: str) -> List[Chunk]:
        """创建布局感知的文档块"""
        chunks = []
        current_chunk_elements = []
        current_length = 0
        chunk_id = 0
        
        sorted_elements = sorted(elements, key=lambda e: (e.page_id, e.sequence_id))
        
        for element in sorted_elements:
            element_length = len(element.content)
            
            if current_length + element_length > self.max_chunk_length and current_chunk_elements:
                chunk = self._finalize_chunk(doc_id, chunk_id, current_chunk_elements)
                chunks.append(chunk)
                current_chunk_elements = []
                current_length = 0
                chunk_id += 1
            
            current_chunk_elements.append(element)
            current_length += element_length
        
        if current_chunk_elements:
            chunk = self._finalize_chunk(doc_id, chunk_id, current_chunk_elements)
            chunks.append(chunk)
        
        return chunks
    
    def _finalize_chunk(self, doc_id: str, chunk_id: int, elements: List[LayoutElement]) -> Chunk:
        """完成块的创建"""
        content = "\n".join([e.content for e in elements])
        page_id = elements[0].page_id if elements else 0
        
        return Chunk(
            doc_id=doc_id,
            chunk_id=chunk_id,
            page_id=page_id,
            content=content,
            layout_elements=elements
        )
    
    def _generate_full_text(self, elements: List[LayoutElement]) -> str:
        """生成全文"""
        return "\n\n".join([e.content for e in elements])
    
    def _organize_by_pages(self, elements: List[LayoutElement]) -> List[Dict[str, Any]]:
        """按页面组织元素"""
        pages = {}
        for element in elements:
            if element.page_id not in pages:
                pages[element.page_id] = {
                    'page_id': element.page_id,
                    'elements': []
                }
            pages[element.page_id]['elements'].append(element)
        
        return list(pages.values())


class LLMPlannerAgent:
    """集成LLM的规划器智能体"""
    
    def __init__(self, llm_client: LLMClient):
        """
        初始化规划器
        
        Args:
            llm_client: LLM客户端
        """
        self.llm = llm_client
    
    def plan(self, query: str, conversation_history: List[Dict[str, str]], 
             documents: Dict[str, Document]) -> Dict[str, Any]:
        """
        制定检索策略（使用LLM）
        
        Args:
            query: 用户查询
            conversation_history: 对话历史
            documents: 文档集合
            
        Returns:
            规划结果
        """
        print(f"\n[Planner] 分析查询: {query}")
        
        # 步骤1: 使用LLM分析查询意图
        intent = self.llm.analyze_query_intent(query)
        print(f"[Planner] 查询意图: {json.dumps(intent, ensure_ascii=False)}")
        
        # 步骤2: 文档过滤（基于摘要匹配）
        relevant_docs = self._filter_documents(query, documents)
        print(f"[Planner] 过滤后的文档: {list(relevant_docs.keys())}")
        
        # 步骤3: 选择检索粒度（基于LLM分析）
        granularity_map = {
            'chunk': Granularity.CHUNK,
            'page': Granularity.PAGE,
            'full': Granularity.FULL,
            'summary': Granularity.SUMMARY
        }
        granularity = granularity_map.get(
            intent.get('granularity', 'chunk'),
            Granularity.CHUNK
        )
        print(f"[Planner] 选择的粒度: {granularity.value}")
        
        # 步骤4: 使用LLM生成子查询
        subqueries = self.llm.generate_subqueries(query, max_subqueries=3)
        print(f"[Planner] 生成的子查询: {subqueries}")
        
        return {
            'relevant_docs': relevant_docs,
            'granularity': granularity,
            'subqueries': subqueries,
            'intent': intent
        }
    
    def _filter_documents(self, query: str, documents: Dict[str, Document]) -> Dict[str, Document]:
        """过滤相关文档"""
        relevant = {}
        query_terms = set(query.lower().split())
        
        for doc_id, doc in documents.items():
            summary_terms = set(doc.summary.lower().split())
            if query_terms & summary_terms:
                relevant[doc_id] = doc
        
        return relevant if relevant else documents


class LLMRefinerAgent:
    """集成LLM的精炼器智能体"""
    
    def __init__(self, llm_client: LLMClient):
        """
        初始化精炼器
        
        Args:
            llm_client: LLM客户端
        """
        self.llm = llm_client
    
    def refine(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """精炼搜索结果"""
        print(f"[Refiner] 精炼 {len(results)} 个结果")
        
        # 步骤1: 去重
        unique_results = self._deduplicate(results)
        
        # 步骤2: 相关性过滤
        relevant_results = self._filter_by_relevance(unique_results, query)
        
        # 步骤3: 重新排序
        reranked_results = self._rerank(relevant_results, query)
        
        print(f"[Refiner] 精炼后剩余 {len(reranked_results)} 个结果")
        return reranked_results
    
    def _deduplicate(self, results: List[SearchResult]) -> List[SearchResult]:
        """去重"""
        seen = set()
        unique = []
        
        for result in results:
            key = (result.doc_id, result.page_id, result.chunk_id)
            if key not in seen:
                seen.add(key)
                unique.append(result)
        
        return unique
    
    def _filter_by_relevance(self, results: List[SearchResult], 
                            query: str, threshold: float = 0.1) -> List[SearchResult]:
        """相关性过滤"""
        return [r for r in results if r.relevance >= threshold]
    
    def _rerank(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """重新排序"""
        return sorted(results, key=lambda x: x.relevance, reverse=True)
    
    def evaluate_sufficiency(self, results: List[SearchResult], query: str) -> float:
        """使用LLM评估信息充分性"""
        if not results:
            return 0.0
        
        # 提取内容
        contents = [r.content[:500] for r in results[:5]]
        
        # 使用LLM评估
        score = self.llm.evaluate_information_sufficiency(query, contents)
        
        return score


class LLMReporterAgent:
    """集成LLM的报告生成器智能体"""
    
    def __init__(self, llm_client: LLMClient):
        """
        初始化报告生成器
        
        Args:
            llm_client: LLM客户端
        """
        self.llm = llm_client
    
    def generate_report(self, query: str, results: List[SearchResult],
                       conversation_history: List[Dict[str, str]]) -> str:
        """使用LLM生成报告"""
        print(f"[Reporter] 使用LLM生成报告,基于 {len(results)} 个证据")
        
        # 准备证据
        evidence_list = []
        for result in results[:10]:  # 最多使用10个证据
            evidence_list.append({
                'content': result.content,
                'doc_id': result.doc_id,
                'relevance': result.relevance
            })
        
        # 使用LLM生成报告
        report = self.llm.generate_report(query, evidence_list, conversation_history)
        
        return report


class LLMDocResearcher:
    """集成LLM的Doc-Researcher主系统"""
    
    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        max_iterations: int = 5,
        sufficiency_threshold: float = 0.7
    ):
        """
        初始化Doc-Researcher系统
        
        Args:
            llm_client: LLM客户端（如果为None，会创建默认客户端）
            max_iterations: 最大迭代次数
            sufficiency_threshold: 信息充分性阈值
        """
        # 初始化LLM客户端
        self.llm = llm_client if llm_client else LLMClient()
        
        # 导入基础组件
        from doc_researcher import RetrievalSystem, SearcherAgent
        
        # 初始化组件
        self.parser = LLMMultimodalParser(self.llm)
        self.retrieval_system = RetrievalSystem(paradigm="hybrid")
        self.planner = LLMPlannerAgent(self.llm)
        self.searcher = SearcherAgent(self.retrieval_system)
        self.refiner = LLMRefinerAgent(self.llm)
        self.reporter = LLMReporterAgent(self.llm)
        
        self.max_iterations = max_iterations
        self.sufficiency_threshold = sufficiency_threshold
        
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_documents(self, doc_paths: List[str]):
        """
        添加文档到系统
        
        Args:
            doc_paths: 文档路径列表
        """
        print(f"\n正在添加 {len(doc_paths)} 个文档到系统...")
        
        for i, doc_path in enumerate(doc_paths):
            doc_id = f"doc_{i+1}"
            
            # 解析文档（会调用LLM）
            document = self.parser.parse_document(doc_path, doc_id)
            
            # 索引文档
            self.retrieval_system.index_document(document)
        
        print(f"成功添加 {len(doc_paths)} 个文档")
    
    def research(self, query: str) -> str:
        """
        执行深度研究（使用LLM）
        
        Args:
            query: 用户查询
            
        Returns:
            研究报告
        """
        print(f"\n{'='*60}")
        print(f"开始深度研究: {query}")
        print(f"{'='*60}")
        
        # 添加到对话历史
        self.conversation_history.append({
            'role': 'user',
            'content': query
        })
        
        # 步骤1: 使用LLM进行规划
        plan = self.planner.plan(
            query,
            self.conversation_history,
            self.retrieval_system.documents
        )
        
        # 步骤2: 迭代搜索-精炼循环
        all_results = []
        iteration = 0
        sufficiency = 0.0
        
        current_subqueries = plan['subqueries']
        
        while iteration < self.max_iterations and sufficiency < self.sufficiency_threshold:
            print(f"\n--- 迭代 {iteration + 1} ---")
            
            # 搜索
            results = self.searcher.search(
                current_subqueries,
                plan['granularity'],
                plan['relevant_docs']
            )
            
            # 精炼
            refined_results = self.refiner.refine(results, query)
            all_results.extend(refined_results)
            
            # 使用LLM评估充分性
            sufficiency = self.refiner.evaluate_sufficiency(all_results, query)
            print(f"信息充分性: {sufficiency:.2f}")
            
            iteration += 1
            
            # 如果需要继续，使用LLM生成新的子查询
            if sufficiency < self.sufficiency_threshold and iteration < self.max_iterations:
                print("信息不足，使用LLM生成新的搜索方向...")
                current_subqueries = self.llm.generate_subqueries(
                    f"{query} （需要更多信息）",
                    max_subqueries=2
                )
        
        # 步骤3: 使用LLM生成报告
        report = self.reporter.generate_report(
            query,
            all_results,
            self.conversation_history
        )
        
        # 添加到对话历史
        self.conversation_history.append({
            'role': 'assistant',
            'content': report
        })
        
        print(f"\n{'='*60}")
        print("研究完成")
        print(f"{'='*60}")
        
        return report


def demo_with_llm():
    """使用真实LLM API的演示"""
    print("="*60)
    print("Doc-Researcher with LLM API 演示")
    print("="*60)
    
    # 创建LLM客户端
    print("\n初始化LLM客户端...")
    llm_client = LLMClient(
        api_url="http://122.115.55.3:32800/v1/chat/completions",
        model="Qwen3_2507",
        timeout=1200
    )
    
    # 创建Doc-Researcher系统
    print("初始化Doc-Researcher系统...")
    researcher = LLMDocResearcher(
        llm_client=llm_client,
        max_iterations=3,
        sufficiency_threshold=0.6
    )
    
    # 添加文档
    print("\n添加文档...")
    doc_paths = [
        "paper1.pdf",
        "paper2.pdf",
        "report.pdf"
    ]
    researcher.add_documents(doc_paths)
    
    # 执行研究
    print("\n执行研究查询...")
    queries = [
        "这些文档讨论的主要技术是什么？",
    ]
    
    for query in queries:
        report = researcher.research(query)
        print(f"\n{'='*60}")
        print("生成的研究报告:")
        print(f"{'='*60}")
        print(report)
        print()


if __name__ == "__main__":
    # 先测试LLM客户端
    print("测试LLM客户端连接...")
    try:
        client = LLMClient()
        response = client.chat(
            messages=[{"role": "user", "content": "请说'测试成功'"}],
            max_tokens=50
        )
        print(f"✅ LLM连接成功: {response}\n")
        
        # 运行完整演示
        demo_with_llm()
        
    except Exception as e:
        print(f"❌ LLM连接失败: {e}")
        print("\n请检查:")
        print("1. API地址是否正确")
        print("2. 网络连接是否正常")
        print("3. API服务是否运行")
