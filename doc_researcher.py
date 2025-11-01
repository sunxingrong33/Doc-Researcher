"""
Doc-Researcher: 多模态文档解析和深度研究系统
基于论文 "Doc-Researcher: A Unified System for Multimodal Document Parsing and Deep Research"
"""

import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import re


class Granularity(Enum):
    """检索粒度枚举"""
    CHUNK = "chunk"      # 块级别
    PAGE = "page"        # 页面级别
    FULL = "full"        # 全文
    SUMMARY = "summary"  # 摘要


class LayoutType(Enum):
    """布局元素类型"""
    TEXT = "text"
    TABLE = "table"
    FIGURE = "figure"
    EQUATION = "equation"


@dataclass
class BoundingBox:
    """边界框"""
    x1: float
    y1: float
    x2: float
    y2: float
    
    def area(self) -> float:
        """计算面积"""
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    def overlap(self, other: 'BoundingBox') -> float:
        """计算与另一个边界框的重叠率"""
        x_left = max(self.x1, other.x1)
        y_top = max(self.y1, other.y1)
        x_right = min(self.x2, other.x2)
        y_bottom = min(self.y2, other.y2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection = (x_right - x_left) * (y_bottom - y_top)
        union = self.area() + other.area() - intersection
        return intersection / union if union > 0 else 0.0


@dataclass
class LayoutElement:
    """布局元素"""
    doc_id: str
    page_id: int
    sequence_id: int
    element_type: LayoutType
    bbox: BoundingBox
    content: str  # 文本内容或描述
    raw_content: Optional[str] = None  # 原始内容(如LaTeX、Markdown表格等)


@dataclass
class Chunk:
    """文档块"""
    doc_id: str
    chunk_id: int
    page_id: int
    content: str
    layout_elements: List[LayoutElement] = field(default_factory=list)
    embedding: Optional[List[float]] = None


@dataclass
class Document:
    """文档"""
    doc_id: str
    title: str
    full_text: str
    summary: str
    pages: List[Dict[str, Any]]  # 页面信息
    chunks: List[Chunk]
    layout_elements: List[LayoutElement]


class MultimodalParser:
    """多模态文档解析器"""
    
    def __init__(self, max_chunk_length: int = 512):
        """
        初始化解析器
        
        Args:
            max_chunk_length: 最大块长度
        """
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
        
        # 步骤1: 使用MinerU进行布局感知解析(这里简化模拟)
        layout_elements = self._extract_layout_elements(doc_path, doc_id)
        
        # 步骤2: 转换视觉元素为文本
        self._transcribe_visual_elements(layout_elements)
        
        # 步骤3: 创建布局感知的文档块
        chunks = self._create_layout_aware_chunks(layout_elements, doc_id)
        
        # 步骤4: 生成多粒度表示
        full_text = self._generate_full_text(layout_elements)
        summary = self._generate_summary(full_text)
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
        """
        提取布局元素(模拟MinerU的功能)
        
        Args:
            doc_path: 文档路径
            doc_id: 文档ID
            
        Returns:
            布局元素列表
        """
        # 这里简化模拟,实际应该调用MinerU API
        # 示例数据
        elements = [
            LayoutElement(
                doc_id=doc_id,
                page_id=1,
                sequence_id=1,
                element_type=LayoutType.TEXT,
                bbox=BoundingBox(50, 100, 500, 200),
                content="这是文档的标题和引言部分..."
            ),
            LayoutElement(
                doc_id=doc_id,
                page_id=1,
                sequence_id=2,
                element_type=LayoutType.TABLE,
                bbox=BoundingBox(50, 250, 500, 400),
                content="",  # 将由VLM生成描述
                raw_content="| 列1 | 列2 |\n|-----|-----|\n| A   | B   |"
            ),
            LayoutElement(
                doc_id=doc_id,
                page_id=1,
                sequence_id=3,
                element_type=LayoutType.FIGURE,
                bbox=BoundingBox(50, 450, 500, 650),
                content="",  # 将由VLM生成描述
            ),
        ]
        
        return elements
    
    def _transcribe_visual_elements(self, elements: List[LayoutElement]):
        """
        转换视觉元素为文本(使用VLM生成描述)
        
        Args:
            elements: 布局元素列表
        """
        for element in elements:
            if element.element_type == LayoutType.TABLE:
                # 生成表格描述(粗粒度和细粒度)
                element.content = self._generate_table_description(element)
            elif element.element_type == LayoutType.FIGURE:
                # 生成图片描述
                element.content = self._generate_figure_description(element)
            elif element.element_type == LayoutType.EQUATION:
                # 转换为LaTeX格式(使用UniMERNet)
                element.content = self._convert_equation_to_latex(element)
    
    def _generate_table_description(self, element: LayoutElement) -> str:
        """生成表格描述(模拟Qwen2.5-VL)"""
        coarse = "这个表格展示了实验结果的对比数据。"
        fine = "表格包含3列和5行,显示了不同方法的性能指标,包括准确率、召回率和F1分数。"
        return f"[粗粒度] {coarse}\n[细粒度] {fine}"
    
    def _generate_figure_description(self, element: LayoutElement) -> str:
        """生成图片描述(模拟Qwen2.5-VL)"""
        coarse = "这是一个展示系统架构的流程图。"
        fine = "图中包含5个主要模块,从左到右依次是输入处理、特征提取、模型推理、结果整合和输出生成。"
        return f"[粗粒度] {coarse}\n[细粒度] {fine}"
    
    def _convert_equation_to_latex(self, element: LayoutElement) -> str:
        """转换公式为LaTeX格式(模拟UniMERNet)"""
        return r"$f(x) = \sum_{i=1}^{n} w_i \cdot x_i + b$"
    
    def _create_layout_aware_chunks(self, elements: List[LayoutElement], doc_id: str) -> List[Chunk]:
        """
        创建布局感知的文档块
        
        Args:
            elements: 布局元素列表
            doc_id: 文档ID
            
        Returns:
            文档块列表
        """
        chunks = []
        current_chunk_elements = []
        current_length = 0
        chunk_id = 0
        
        # 按页面和序列ID排序
        sorted_elements = sorted(elements, key=lambda e: (e.page_id, e.sequence_id))
        
        for element in sorted_elements:
            element_length = len(element.content)
            
            # 检查是否需要创建新块
            if current_length + element_length > self.max_chunk_length and current_chunk_elements:
                # 创建当前块
                chunk = self._finalize_chunk(
                    doc_id, chunk_id, current_chunk_elements
                )
                chunks.append(chunk)
                
                # 重置
                current_chunk_elements = []
                current_length = 0
                chunk_id += 1
            
            current_chunk_elements.append(element)
            current_length += element_length
        
        # 处理最后一个块
        if current_chunk_elements:
            chunk = self._finalize_chunk(
                doc_id, chunk_id, current_chunk_elements
            )
            chunks.append(chunk)
        
        return chunks
    
    def _finalize_chunk(self, doc_id: str, chunk_id: int, 
                       elements: List[LayoutElement]) -> Chunk:
        """
        完成块的创建
        
        Args:
            doc_id: 文档ID
            chunk_id: 块ID
            elements: 布局元素列表
            
        Returns:
            文档块
        """
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
    
    def _generate_summary(self, full_text: str) -> str:
        """生成摘要(使用LLM)"""
        # 这里简化,实际应该调用LLM API
        return f"这篇文档讨论了...主要内容包括...(全文长度: {len(full_text)} 字符)"
    
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


class RetrievalSystem:
    """多模态检索系统"""
    
    def __init__(self, paradigm: str = "hybrid"):
        """
        初始化检索系统
        
        Args:
            paradigm: 检索范式 ("text", "vision", "hybrid")
        """
        self.paradigm = paradigm
        self.documents: Dict[str, Document] = {}
        self.index = {}  # 简化的索引
    
    def index_document(self, document: Document):
        """
        索引文档
        
        Args:
            document: 文档对象
        """
        self.documents[document.doc_id] = document
        
        # 索引不同粒度的内容
        self._index_chunks(document)
        self._index_pages(document)
        self._index_full_text(document)
        self._index_summary(document)
    
    def _index_chunks(self, document: Document):
        """索引文档块"""
        for chunk in document.chunks:
            key = f"{document.doc_id}_chunk_{chunk.chunk_id}"
            self.index[key] = {
                'type': 'chunk',
                'content': chunk.content,
                'doc_id': document.doc_id,
                'chunk_id': chunk.chunk_id,
                'page_id': chunk.page_id,
                'layout_elements': chunk.layout_elements
            }
    
    def _index_pages(self, document: Document):
        """索引页面"""
        for page in document.pages:
            key = f"{document.doc_id}_page_{page['page_id']}"
            content = "\n".join([e.content for e in page['elements']])
            self.index[key] = {
                'type': 'page',
                'content': content,
                'doc_id': document.doc_id,
                'page_id': page['page_id'],
                'elements': page['elements']
            }
    
    def _index_full_text(self, document: Document):
        """索引全文"""
        key = f"{document.doc_id}_full"
        self.index[key] = {
            'type': 'full',
            'content': document.full_text,
            'doc_id': document.doc_id
        }
    
    def _index_summary(self, document: Document):
        """索引摘要"""
        key = f"{document.doc_id}_summary"
        self.index[key] = {
            'type': 'summary',
            'content': document.summary,
            'doc_id': document.doc_id
        }
    
    def retrieve(self, query: str, granularity: Granularity, 
                top_k: int = 10) -> List[Dict[str, Any]]:
        """
        检索
        
        Args:
            query: 查询
            granularity: 检索粒度
            top_k: 返回前k个结果
            
        Returns:
            检索结果列表
        """
        results = []
        
        # 简化的相似度计算(实际应该使用向量相似度)
        for key, item in self.index.items():
            if item['type'] == granularity.value:
                score = self._compute_similarity(query, item['content'])
                results.append({
                    'key': key,
                    'score': score,
                    'item': item
                })
        
        # 排序并返回top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def _compute_similarity(self, query: str, content: str) -> float:
        """
        计算相似度(简化版本,实际应该使用嵌入向量)
        
        Args:
            query: 查询
            content: 内容
            
        Returns:
            相似度分数
        """
        # 简单的关键词匹配
        query_terms = set(query.lower().split())
        content_terms = set(content.lower().split())
        intersection = query_terms & content_terms
        
        if not query_terms:
            return 0.0
        
        return len(intersection) / len(query_terms)


@dataclass
class SearchResult:
    """搜索结果"""
    relevance: float
    content: str
    doc_id: str
    page_id: Optional[int] = None
    chunk_id: Optional[int] = None
    layout_elements: List[LayoutElement] = field(default_factory=list)


class PlannerAgent:
    """规划器智能体"""
    
    def plan(self, query: str, conversation_history: List[Dict[str, str]], 
             documents: Dict[str, Document]) -> Dict[str, Any]:
        """
        制定检索策略
        
        Args:
            query: 用户查询
            conversation_history: 对话历史
            documents: 文档集合
            
        Returns:
            规划结果,包括文档过滤、粒度选择、子查询
        """
        print(f"\n[Planner] 分析查询: {query}")
        
        # 步骤1: 文档过滤(基于摘要匹配)
        relevant_docs = self._filter_documents(query, documents)
        print(f"[Planner] 过滤后的文档: {[d for d in relevant_docs.keys()]}")
        
        # 步骤2: 选择检索粒度
        granularity = self._select_granularity(query, conversation_history)
        print(f"[Planner] 选择的粒度: {granularity.value}")
        
        # 步骤3: 生成子查询
        subqueries = self._generate_subqueries(query, conversation_history)
        print(f"[Planner] 生成的子查询: {subqueries}")
        
        return {
            'relevant_docs': relevant_docs,
            'granularity': granularity,
            'subqueries': subqueries
        }
    
    def _filter_documents(self, query: str, 
                         documents: Dict[str, Document]) -> Dict[str, Document]:
        """
        过滤相关文档
        
        Args:
            query: 查询
            documents: 文档集合
            
        Returns:
            相关文档
        """
        relevant = {}
        query_terms = set(query.lower().split())
        
        for doc_id, doc in documents.items():
            summary_terms = set(doc.summary.lower().split())
            # 简单的关键词匹配
            if query_terms & summary_terms:
                relevant[doc_id] = doc
        
        # 如果没有匹配的,返回所有文档
        return relevant if relevant else documents
    
    def _select_granularity(self, query: str, 
                           history: List[Dict[str, str]]) -> Granularity:
        """
        选择检索粒度
        
        Args:
            query: 查询
            history: 对话历史
            
        Returns:
            选择的粒度
        """
        # 简化的规则:
        # - 如果查询包含"总结"、"概述"等,使用summary
        # - 如果查询包含"比较"、"对比"等,使用chunk
        # - 如果查询包含"全部"、"完整"等,使用full
        # - 默认使用chunk
        
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ["总结", "概述", "摘要", "summarize"]):
            return Granularity.SUMMARY
        elif any(kw in query_lower for kw in ["全部", "完整", "整个", "full"]):
            return Granularity.FULL
        elif any(kw in query_lower for kw in ["页面", "page"]):
            return Granularity.PAGE
        else:
            return Granularity.CHUNK
    
    def _generate_subqueries(self, query: str, 
                            history: List[Dict[str, str]]) -> List[str]:
        """
        生成子查询
        
        Args:
            query: 原始查询
            history: 对话历史
            
        Returns:
            子查询列表
        """
        # 简化版本:将复杂查询分解为子查询
        subqueries = [query]
        
        # 如果查询包含"和"、"以及"等连接词,进行分解
        if "和" in query or "以及" in query or "还有" in query:
            parts = re.split(r'[和以及还有]', query)
            subqueries = [p.strip() for p in parts if p.strip()]
        
        return subqueries


class SearcherAgent:
    """搜索器智能体"""
    
    def __init__(self, retrieval_system: RetrievalSystem):
        """
        初始化搜索器
        
        Args:
            retrieval_system: 检索系统
        """
        self.retrieval_system = retrieval_system
    
    def search(self, subqueries: List[str], granularity: Granularity,
               relevant_docs: Dict[str, Document], top_k: int = 10) -> List[SearchResult]:
        """
        执行搜索
        
        Args:
            subqueries: 子查询列表
            granularity: 检索粒度
            relevant_docs: 相关文档
            top_k: 每个查询返回的结果数
            
        Returns:
            搜索结果列表
        """
        all_results = []
        
        for subquery in subqueries:
            print(f"[Searcher] 搜索子查询: {subquery}")
            results = self.retrieval_system.retrieve(subquery, granularity, top_k)
            
            # 转换为SearchResult对象
            for result in results:
                item = result['item']
                search_result = SearchResult(
                    relevance=result['score'],
                    content=item['content'],
                    doc_id=item['doc_id'],
                    page_id=item.get('page_id'),
                    chunk_id=item.get('chunk_id'),
                    layout_elements=item.get('layout_elements', [])
                )
                all_results.append(search_result)
        
        return all_results


class RefinerAgent:
    """精炼器智能体"""
    
    def refine(self, results: List[SearchResult], query: str) -> List[SearchResult]:
        """
        精炼搜索结果
        
        Args:
            results: 原始搜索结果
            query: 原始查询
            
        Returns:
            精炼后的结果
        """
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
        # 简化版本:按相关性排序
        return sorted(results, key=lambda x: x.relevance, reverse=True)
    
    def evaluate_sufficiency(self, results: List[SearchResult], 
                           query: str) -> float:
        """
        评估信息充分性
        
        Args:
            results: 搜索结果
            query: 查询
            
        Returns:
            充分性得分 (0-1)
        """
        # 简化版本:基于结果数量和平均相关性
        if not results:
            return 0.0
        
        avg_relevance = sum(r.relevance for r in results) / len(results)
        coverage_score = min(len(results) / 5, 1.0)  # 假设5个结果足够
        
        return (avg_relevance + coverage_score) / 2


class ReporterAgent:
    """报告生成器智能体"""
    
    def generate_report(self, query: str, results: List[SearchResult],
                       conversation_history: List[Dict[str, str]]) -> str:
        """
        生成报告
        
        Args:
            query: 查询
            results: 搜索结果
            conversation_history: 对话历史
            
        Returns:
            生成的报告
        """
        print(f"[Reporter] 生成报告,基于 {len(results)} 个证据")
        
        # 步骤1: 分析查询意图
        intent = self._analyze_intent(query)
        
        # 步骤2: 组织证据
        organized_evidence = self._organize_evidence(results)
        
        # 步骤3: 生成报告
        report = self._synthesize_report(query, organized_evidence, intent)
        
        # 步骤4: 添加引用
        report_with_citations = self._add_citations(report, results)
        
        return report_with_citations
    
    def _analyze_intent(self, query: str) -> str:
        """分析查询意图"""
        if any(kw in query.lower() for kw in ["比较", "对比", "compare"]):
            return "comparison"
        elif any(kw in query.lower() for kw in ["总结", "概述", "summarize"]):
            return "summary"
        elif any(kw in query.lower() for kw in ["为什么", "原因", "why"]):
            return "explanation"
        else:
            return "factual"
    
    def _organize_evidence(self, results: List[SearchResult]) -> Dict[str, List[SearchResult]]:
        """组织证据"""
        organized = {}
        
        for result in results:
            doc_id = result.doc_id
            if doc_id not in organized:
                organized[doc_id] = []
            organized[doc_id].append(result)
        
        return organized
    
    def _synthesize_report(self, query: str, 
                          evidence: Dict[str, List[SearchResult]], 
                          intent: str) -> str:
        """综合报告"""
        report_parts = []
        
        # 添加开头
        report_parts.append(f"针对您的查询「{query}」,我整理了以下信息:\n")
        
        # 根据意图组织内容
        if intent == "comparison":
            report_parts.append(self._generate_comparison(evidence))
        elif intent == "summary":
            report_parts.append(self._generate_summary(evidence))
        elif intent == "explanation":
            report_parts.append(self._generate_explanation(evidence))
        else:
            report_parts.append(self._generate_factual_answer(evidence))
        
        return "\n".join(report_parts)
    
    def _generate_comparison(self, evidence: Dict[str, List[SearchResult]]) -> str:
        """生成对比报告"""
        parts = ["## 对比分析\n"]
        
        for doc_id, results in evidence.items():
            parts.append(f"### 文档 {doc_id}")
            for result in results[:2]:  # 每个文档取前2个结果
                parts.append(f"- {result.content[:100]}...")
        
        return "\n".join(parts)
    
    def _generate_summary(self, evidence: Dict[str, List[SearchResult]]) -> str:
        """生成摘要报告"""
        parts = ["## 摘要\n"]
        
        all_results = []
        for results in evidence.values():
            all_results.extend(results)
        
        # 取相关性最高的几个结果
        top_results = sorted(all_results, key=lambda x: x.relevance, reverse=True)[:3]
        
        for i, result in enumerate(top_results, 1):
            parts.append(f"{i}. {result.content[:150]}...")
        
        return "\n".join(parts)
    
    def _generate_explanation(self, evidence: Dict[str, List[SearchResult]]) -> str:
        """生成解释报告"""
        parts = ["## 解释\n"]
        
        all_results = []
        for results in evidence.values():
            all_results.extend(results)
        
        for result in all_results[:3]:
            parts.append(f"- {result.content[:150]}...")
        
        return "\n".join(parts)
    
    def _generate_factual_answer(self, evidence: Dict[str, List[SearchResult]]) -> str:
        """生成事实性回答"""
        parts = []
        
        all_results = []
        for results in evidence.values():
            all_results.extend(results)
        
        for result in all_results[:3]:
            parts.append(result.content[:200])
        
        return "\n\n".join(parts)
    
    def _add_citations(self, report: str, results: List[SearchResult]) -> str:
        """添加引用"""
        # 简化版本:在报告末尾添加引用列表
        citations = ["\n\n## 参考文献\n"]
        
        for i, result in enumerate(results[:5], 1):
            citation = f"[{i}] 文档 {result.doc_id}"
            if result.page_id is not None:
                citation += f", 页面 {result.page_id}"
            if result.chunk_id is not None:
                citation += f", 块 {result.chunk_id}"
            citations.append(citation)
        
        return report + "\n".join(citations)


class DocResearcher:
    """Doc-Researcher主系统"""
    
    def __init__(self, max_iterations: int = 5, sufficiency_threshold: float = 0.7):
        """
        初始化Doc-Researcher系统
        
        Args:
            max_iterations: 最大迭代次数
            sufficiency_threshold: 信息充分性阈值
        """
        self.parser = MultimodalParser()
        self.retrieval_system = RetrievalSystem(paradigm="hybrid")
        self.planner = PlannerAgent()
        self.searcher = SearcherAgent(self.retrieval_system)
        self.refiner = RefinerAgent()
        self.reporter = ReporterAgent()
        
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
            
            # 解析文档
            document = self.parser.parse_document(doc_path, doc_id)
            
            # 索引文档
            self.retrieval_system.index_document(document)
        
        print(f"成功添加 {len(doc_paths)} 个文档")
    
    def research(self, query: str) -> str:
        """
        执行深度研究
        
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
        
        # 步骤1: 规划
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
            
            # 评估充分性
            sufficiency = self.refiner.evaluate_sufficiency(all_results, query)
            print(f"信息充分性: {sufficiency:.2f}")
            
            iteration += 1
            
            # 如果需要继续,生成新的子查询
            if sufficiency < self.sufficiency_threshold and iteration < self.max_iterations:
                print("信息不足,生成新的搜索方向...")
                current_subqueries = self._generate_new_subqueries(
                    query, all_results
                )
        
        # 步骤3: 生成报告
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
    
    def _generate_new_subqueries(self, original_query: str, 
                                current_results: List[SearchResult]) -> List[str]:
        """
        生成新的子查询
        
        Args:
            original_query: 原始查询
            current_results: 当前结果
            
        Returns:
            新的子查询列表
        """
        # 简化版本:基于现有结果生成相关查询
        # 实际应该使用LLM生成
        return [f"{original_query} 详细信息", f"{original_query} 相关背景"]


def demo():
    """演示系统功能"""
    print("Doc-Researcher 系统演示")
    print("="*60)
    
    # 创建系统
    researcher = DocResearcher(max_iterations=3, sufficiency_threshold=0.6)
    
    # 添加文档(这里使用模拟路径)
    doc_paths = [
        "paper1.pdf",
        "paper2.pdf",
        "report1.pdf"
    ]
    researcher.add_documents(doc_paths)
    
    # 执行研究
    queries = [
        "这些文档讨论的主要技术是什么?",
        "比较不同方法的性能表现",
    ]
    
    for query in queries:
        report = researcher.research(query)
        print(f"\n{'='*60}")
        print("生成的报告:")
        print(f"{'='*60}")
        print(report)
        print()


if __name__ == "__main__":
    demo()
