"""
LLM客户端封装 - 用于Doc-Researcher系统
支持Qwen3模型API调用
"""

import requests
import json
import time
from typing import List, Dict, Any, Optional


class LLMClient:
    """LLM客户端 - 封装Qwen3 API调用"""
    
    def __init__(
        self,
        api_url: str = "http://12.11.5.3:3200/v1/chat/completions",
        model: str = "Qwen3_2507",
        timeout: int = 1200,
        max_retries: int = 3
    ):
        """
        初始化LLM客户端
        
        Args:
            api_url: API地址
            model: 模型名称
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.api_url = api_url
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0,
        top_p: float = 1,
        max_tokens: int = 4000,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        调用聊天API
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            top_p: top_p参数
            max_tokens: 最大token数
            system_prompt: 系统提示（如果提供，会添加到消息开头）
            
        Returns:
            模型回复内容
        """
        # 构建完整的消息列表
        full_messages = []
        
        # 添加系统提示
        if system_prompt:
            full_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 添加用户消息
        full_messages.extend(messages)
        
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": full_messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "chat_template_kwargs": {"enable_thinking": False},
            "seed": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # 重试逻辑
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return content
                
            except requests.exceptions.RequestException as e:
                print(f"API请求错误 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    raise Exception(f"API调用失败，已重试{self.max_retries}次: {e}")
                    
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                print(f"响应解析错误: {e}")
                raise Exception(f"API响应格式错误: {e}")
    
    def generate_table_description(self, table_markdown: str) -> str:
        """
        生成表格描述
        
        Args:
            table_markdown: 表格的Markdown格式
            
        Returns:
            表格描述（粗粒度和细粒度）
        """
        system_prompt = "你是一位专业的数据分析专家，擅长理解和描述表格内容。"
        
        user_message = f"""请分析以下表格，并提供两个层次的描述：

表格内容（Markdown格式）：
```
{table_markdown}
```

请按以下格式输出：

[粗粒度描述]
（用1-2句话概括表格的整体内容和目的）

[细粒度描述]
（详细描述表格的结构、列含义、数据特点和关键信息）
"""
        
        messages = [{"role": "user", "content": user_message}]
        return self.chat(messages, temperature=0.3, max_tokens=1000)
    
    def generate_figure_description(self, figure_context: str = "") -> str:
        """
        生成图片描述
        
        Args:
            figure_context: 图片的上下文信息（如标题、说明等）
            
        Returns:
            图片描述（粗粒度和细粒度）
        """
        system_prompt = "你是一位专业的视觉内容分析专家，擅长描述图表和示意图。"
        
        user_message = f"""请为一张图片生成描述。图片的上下文信息如下：

{figure_context if figure_context else "（图片标题：技术架构图）"}

由于无法直接看到图片，请基于上下文生成合理的描述。按以下格式输出：

[粗粒度描述]
（用1-2句话概括图片的主题和类型）

[细粒度描述]
（描述可能包含的主要元素、结构、流程或关系）
"""
        
        messages = [{"role": "user", "content": user_message}]
        return self.chat(messages, temperature=0.3, max_tokens=1000)
    
    def generate_summary(self, full_text: str, max_length: int = 500) -> str:
        """
        生成文档摘要
        
        Args:
            full_text: 完整文本
            max_length: 摘要最大长度
            
        Returns:
            文档摘要
        """
        system_prompt = "你是一位专业的文档摘要专家，擅长提取文档的核心内容。"
        
        # 如果文本太长，截取前部分
        text_preview = full_text[:3000] if len(full_text) > 3000 else full_text
        
        user_message = f"""请为以下文档生成一个{max_length}字以内的摘要，概括其主要内容、关键观点和重要信息：

{text_preview}

{"..." if len(full_text) > 3000 else ""}

摘要要求：
1. 概括文档的主题和目的
2. 提取关键信息点
3. 保持客观准确
4. 字数不超过{max_length}字
"""
        
        messages = [{"role": "user", "content": user_message}]
        return self.chat(messages, temperature=0.2, max_tokens=1000)
    
    def analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """
        分析查询意图
        
        Args:
            query: 用户查询
            
        Returns:
            意图分析结果
        """
        system_prompt = "你是一位专业的查询分析专家，擅长理解用户意图。"
        
        user_message = f"""请分析以下用户查询的意图，并以JSON格式返回分析结果：

查询：{query}

请分析：
1. intent_type: 查询类型（factual/comparison/summary/explanation）
2. granularity: 建议的检索粒度（chunk/page/full/summary）
3. complexity: 查询复杂度（simple/medium/complex）
4. needs_multi_doc: 是否需要多文档（true/false）

只返回JSON格式，不要其他内容：
```json
{{
    "intent_type": "...",
    "granularity": "...",
    "complexity": "...",
    "needs_multi_doc": true/false
}}
```
"""
        
        messages = [{"role": "user", "content": user_message}]
        response = self.chat(messages, temperature=0, max_tokens=500)
        
        # 提取JSON
        try:
            # 尝试从markdown代码块中提取
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except:
            # 如果解析失败，返回默认值
            return {
                "intent_type": "factual",
                "granularity": "chunk",
                "complexity": "medium",
                "needs_multi_doc": False
            }
    
    def generate_subqueries(self, query: str, max_subqueries: int = 3) -> List[str]:
        """
        生成子查询
        
        Args:
            query: 原始查询
            max_subqueries: 最大子查询数
            
        Returns:
            子查询列表
        """
        system_prompt = "你是一位专业的查询分解专家，擅长将复杂查询分解为简单子查询。"
        
        user_message = f"""请将以下复杂查询分解为{max_subqueries}个更简单、更具体的子查询：

原始查询：{query}

要求：
1. 每个子查询应该独立且可回答
2. 子查询应该覆盖原始查询的不同方面
3. 保持查询的核心意图
4. 如果查询已经很简单，可以只返回1个子查询

请以JSON数组格式返回，只返回JSON，不要其他内容：
```json
[
    "子查询1",
    "子查询2",
    "子查询3"
]
```
"""
        
        messages = [{"role": "user", "content": user_message}]
        response = self.chat(messages, temperature=0.3, max_tokens=1000)
        
        # 提取JSON
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            subqueries = json.loads(json_str)
            return subqueries[:max_subqueries]
        except:
            # 如果解析失败，返回原始查询
            return [query]
    
    def evaluate_information_sufficiency(
        self,
        query: str,
        retrieved_contents: List[str]
    ) -> float:
        """
        评估信息充分性
        
        Args:
            query: 查询
            retrieved_contents: 检索到的内容列表
            
        Returns:
            充分性得分（0-1）
        """
        system_prompt = "你是一位专业的信息评估专家，擅长判断信息是否充分回答问题。"
        
        # 合并检索内容（限制长度）
        combined_content = "\n\n---\n\n".join(retrieved_contents[:5])
        if len(combined_content) > 2000:
            combined_content = combined_content[:2000] + "..."
        
        user_message = f"""请评估以下检索到的信息是否充分回答了用户的查询。

用户查询：{query}

检索到的信息：
{combined_content}

请以0-1之间的分数评估信息充分性，并简要说明理由。

只返回JSON格式：
```json
{{
    "sufficiency_score": 0.0-1.0,
    "reason": "评估理由"
}}
```
"""
        
        messages = [{"role": "user", "content": user_message}]
        response = self.chat(messages, temperature=0, max_tokens=500)
        
        # 提取JSON
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            result = json.loads(json_str)
            return float(result.get("sufficiency_score", 0.5))
        except:
            # 如果解析失败，返回默认值
            return 0.5
    
    def generate_report(
        self,
        query: str,
        evidence_list: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        生成研究报告
        
        Args:
            query: 用户查询
            evidence_list: 证据列表
            conversation_history: 对话历史
            
        Returns:
            研究报告
        """
        system_prompt = """你是一位专业的研究报告撰写专家，擅长综合多个信息源生成高质量的报告。

要求：
1. 基于提供的证据进行综合分析
2. 保持客观准确，不要编造信息
3. 使用清晰的结构组织内容
4. 在适当位置标注引用[引用X]
5. 如果证据不足，明确说明"""
        
        # 准备证据内容
        evidence_texts = []
        for i, evidence in enumerate(evidence_list[:10], 1):  # 最多使用10个证据
            content = evidence.get('content', '')
            doc_id = evidence.get('doc_id', 'unknown')
            evidence_texts.append(f"[证据{i}] (来源: {doc_id})\n{content[:300]}...")
        
        evidence_section = "\n\n".join(evidence_texts)
        
        # 准备对话历史
        history_section = ""
        if conversation_history and len(conversation_history) > 1:
            recent_history = conversation_history[-4:]  # 最近2轮对话
            history_texts = []
            for msg in recent_history:
                role = "用户" if msg['role'] == 'user' else "助手"
                history_texts.append(f"{role}: {msg['content'][:100]}...")
            history_section = "对话历史：\n" + "\n".join(history_texts) + "\n\n"
        
        user_message = f"""{history_section}当前查询：{query}

检索到的证据：
{evidence_section}

请基于以上证据，为用户查询生成一个全面、准确的研究报告。报告应该：
1. 直接回答用户的问题
2. 综合多个证据来源
3. 使用[引用X]标注信息来源
4. 结构清晰，易于阅读
5. 字数适中（300-800字）
"""
        
        messages = [{"role": "user", "content": user_message}]
        return self.chat(messages, temperature=0.3, max_tokens=2000)


# 测试函数
def test_llm_client():
    """测试LLM客户端"""
    print("="*60)
    print("测试LLM客户端")
    print("="*60)
    
    client = LLMClient()
    
    # 测试1: 简单对话
    print("\n【测试1: 简单对话】")
    messages = [{"role": "user", "content": "请用一句话介绍什么是深度学习"}]
    response = client.chat(messages)
    print(f"回复: {response}")
    
    # 测试2: 生成表格描述
    print("\n【测试2: 生成表格描述】")
    table_md = """| 方法 | 准确率 | 召回率 |
|------|--------|--------|
| A    | 0.85   | 0.82   |
| B    | 0.90   | 0.88   |"""
    description = client.generate_table_description(table_md)
    print(f"表格描述:\n{description}")
    
    # 测试3: 分析查询意图
    print("\n【测试3: 分析查询意图】")
    query = "比较这些文档中讨论的不同方法的性能表现"
    intent = client.analyze_query_intent(query)
    print(f"意图分析: {json.dumps(intent, ensure_ascii=False, indent=2)}")
    
    # 测试4: 生成子查询
    print("\n【测试4: 生成子查询】")
    subqueries = client.generate_subqueries(query)
    print(f"子查询: {json.dumps(subqueries, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    test_llm_client()
