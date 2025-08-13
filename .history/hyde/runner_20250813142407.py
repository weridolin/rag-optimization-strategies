import asyncio
from typing import List, Dict, Any, Optional
from .template import (
    PROMPT_TYPES,
    QUESTION_CLASSIFICATION_PROMPT,
    FINAL_ANSWER_PROMPT
)
from base.mixins import LLMCallMixin


class HydeRunner(LLMCallMixin):
    """基于Hyde策略的RAG检索优化处理器
    
    Hyde策略通过以下步骤优化检索：
    1. 接收用户问题
    2. 使用LLM生成假设性的理想答案
    3. 将假设性答案进行向量化embedding
    4. 使用假设性答案的向量去检索相关文档
    5. 基于检索到的真实文档生成最终答案
    """
    
    def __init__(self, llm_api_key: str, llm_api_url: str):
        super().__init__(llm_api_key, llm_api_url)
        self.hyde_cache = {}  # 缓存假设性答案


    
    def auto_detect_prompt_type(self, question: str) -> str:
        """
        自动检测问题类型
        """
        prompt = QUESTION_CLASSIFICATION_PROMPT.format(question=question)   
        ## 调用大模型获取分类结果
        messages = self.create_messages(user_content=prompt)
        response = self.call_llm_sync(messages)
        return response


    def generate_hypothetical_answer(self, question: str, prompt_type: Optional[str] = None) -> str:
        """
        生成假设性答案（Hyde策略的核心步骤）
        Args:
            question: 用户的原始问题
            prompt_type: 指定prompt类型，如果为None则自动检测
            
        Returns:
            str: 生成的假设性答案
        """
        # 自动检测或使用指定的prompt类型
        if prompt_type is None:
            prompt_type = self.auto_detect_prompt_type(question)
            print(f"自动检测到问题类型: {prompt_type}")
        
        # 生成Hyde prompt
        hyde_prompt = PROMPT_TYPES[prompt_type].format(question=question)
        
        print(f"正在生成假设性答案 (类型: {prompt_type})...")
        
        # 调用LLM生成假设性答案
        messages = self.create_messages(user_content=hyde_prompt)
        hypothetical_answer = self.call_llm_sync(messages)
        
        print("假设性答案生成完成")
        return hypothetical_answer
    
    async def generate_hypothetical_answer_async(self, question: str, prompt_type: Optional[str] = None) -> str:
        """
        流式生成假设性答案
        
        Args:
            question: 用户的原始问题
            prompt_type: 指定prompt类型，如果为None则自动检测
            
        Returns:
            str: 生成的假设性答案
        """

        # 自动检测或使用指定的prompt类型
        if prompt_type is None:
            prompt_type = self.auto_detect_prompt_type(question)
            print(f"自动检测到问题类型: {prompt_type}")
        
        hyde_prompt = PROMPT_TYPES[prompt_type].format(question=question)
        
        # 调用LLM流式生成假设性答案
        messages = self.create_messages(user_content=hyde_prompt)
        hypothetical_answer = ""
        
        async for chunk in await self.call_llm_async(messages, stream=True):
            print(chunk, end='', flush=True)
            hypothetical_answer += chunk
        print("\n")
        
        print("假设性答案生成完成")
        return hypothetical_answer
    
    def run_with_retrieval(self, question: str, retrieval_func, prompt_type: Optional[str] = None, 
                          top_k: int = 5) -> Dict[str, Any]:
        """
        完整的Hyde策略执行：生成假设性答案 -> 检索 -> 生成最终答案
        
        Args:
            question: 用户问题
            retrieval_func: 检索函数，接受文本返回相关文档列表
            prompt_type: prompt类型
            top_k: 检索返回的文档数量
            
        Returns:
            Dict[str, Any]: 包含假设性答案、检索结果和最终答案的字典
        """
        print("=== Hyde策略执行开始 ===")
        
        # 步骤1: 生成假设性答案
        hypothetical_answer = self.generate_hypothetical_answer(question, prompt_type)
        
        # 步骤2: 使用假设性答案进行检索
        print("正在使用假设性答案进行文档检索...")
        retrieved_docs = retrieval_func(hypothetical_answer, top_k=top_k)
        print(f"检索到 {len(retrieved_docs)} 个相关文档")
        
        # 步骤3: 基于真实检索文档生成最终答案
        print("正在基于检索文档生成最终答案...")
        final_answer_prompt = self._create_final_answer_prompt(question, retrieved_docs)
        messages = self.create_messages(user_content=final_answer_prompt)
        final_answer = self.call_llm_sync(messages)
        
        print("=== Hyde策略执行完成 ===")
        
        return {
            "original_question": question,
            "hypothetical_answer": hypothetical_answer,
            "retrieved_documents": retrieved_docs,
            "final_answer": final_answer,
            "prompt_type": prompt_type or auto_detect_prompt_type(question),
            "retrieval_count": len(retrieved_docs)
        }
    
    async def run(self, question: str, retrieval_func, prompt_type: Optional[str] = None,
                                    top_k: int = 5) -> Dict[str, Any]:
        """
        异步版本的完整Hyde策略执行
        
        Args:
            question: 用户问题
            retrieval_func: 检索函数，接受文本返回相关文档列表
            prompt_type: prompt类型
            top_k: 检索返回的文档数量
            
        Returns:
            Dict[str, Any]: 包含假设性答案、检索结果和最终答案的字典
        """
        print("=== Hyde策略异步执行开始 ===")
        
        # 步骤1: 异步生成假设性答案
        hypothetical_answer = await self.generate_hypothetical_answer_async(question, prompt_type)
        
        # 步骤2: 使用假设性答案进行检索
        print("正在使用假设性答案进行文档检索...")
        retrieved_docs = retrieval_func(hypothetical_answer, top_k=top_k)
        print(f"检索到 {len(retrieved_docs)} 个相关文档")
        
        if isinstance(retrieved_docs, list):
            context = "\n\n".join([f"文档{i+1}:\n{doc}" for i, doc in enumerate(retrieved_docs)])
        # 步骤3: 基于真实检索文档异步生成最终答案
        print("正在基于检索文档异步生成最终答案...")
        final_answer_prompt = FINAL_ANSWER_PROMPT.format(question=question, context=retrieved_docs)
        messages = self.create_messages(user_content=final_answer_prompt)
        final_answer = await self.call_llm_async(messages)
        
        print("=== Hyde策略异步执行完成 ===")
        
        return {
            "original_question": question,
            "hypothetical_answer": hypothetical_answer,
            "retrieved_documents": retrieved_docs,
            "final_answer": final_answer,
            "prompt_type": prompt_type or auto_detect_prompt_type(question),
            "retrieval_count": len(retrieved_docs)
        }
    
    def _create_final_answer_prompt(self, question: str, retrieved_docs: List[str]) -> str:
        """
        创建基于检索文档的最终答案生成prompt
        
        Args:
            question: 原始问题
            retrieved_docs: 检索到的文档列表
            
        Returns:
            str: 最终答案生成的prompt
        """
        context = "\n\n".join([f"文档{i+1}:\n{doc}" for i, doc in enumerate(retrieved_docs)])
        
        final_prompt = f"""
基于以下检索到的相关文档，请详细回答用户的问题。

**用户问题**: {question}

**相关文档**:
{context}

**回答要求**:
1. 基于提供的文档内容进行回答
2. 如果文档信息不足，请明确说明
3. 引用具体的文档内容作为支撑
4. 保持答案的准确性和客观性
5. 结构清晰，逻辑连贯

**请提供详细回答**:
"""
        return final_prompt
    
    def compare_with_baseline(self, question: str, baseline_retrieval_func, hyde_retrieval_func,
                            prompt_type: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
        """
        比较Hyde策略与baseline检索策略的效果
        
        Args:
            question: 用户问题
            baseline_retrieval_func: 基线检索函数（直接使用原始问题检索）
            hyde_retrieval_func: Hyde检索函数（使用假设性答案检索）
            prompt_type: prompt类型
            top_k: 检索返回的文档数量
            
        Returns:
            Dict[str, Any]: 比较结果
        """
        print("=== Hyde策略 vs Baseline 比较测试 ===")
        
        # Baseline方法：直接使用原始问题检索
        print("执行Baseline检索...")
        baseline_docs = baseline_retrieval_func(question, top_k=top_k)
        baseline_prompt = self._create_final_answer_prompt(question, baseline_docs)
        messages = self.create_messages(user_content=baseline_prompt)
        baseline_answer = self.call_llm_sync(messages)
        
        # Hyde方法
        print("执行Hyde策略...")
        hyde_result = self.run_with_retrieval(question, hyde_retrieval_func, prompt_type, top_k)
        
        return {
            "question": question,
            "baseline": {
                "retrieved_documents": baseline_docs,
                "final_answer": baseline_answer,
                "method": "direct_question_retrieval"
            },
            "hyde": {
                "hypothetical_answer": hyde_result["hypothetical_answer"],
                "retrieved_documents": hyde_result["retrieved_documents"],
                "final_answer": hyde_result["final_answer"],
                "prompt_type": hyde_result["prompt_type"],
                "method": "hypothetical_answer_retrieval"
            },
            "comparison": {
                "baseline_doc_count": len(baseline_docs),
                "hyde_doc_count": len(hyde_result["retrieved_documents"]),
                "prompt_type_used": hyde_result["prompt_type"]
            }
        }
    
    def get_available_prompt_types(self) -> Dict[str, str]:
        """
        获取可用的prompt类型及其描述
        
        Returns:
            Dict[str, str]: prompt类型及描述
        """
        return {
            "general": "通用prompt，适用于大多数问题",
            "technical": "技术类prompt，适用于编程、算法、系统架构等技术问题",
            "business": "商业类prompt，适用于市场、管理、策略等商业问题",
            "academic": "学术类prompt，适用于研究、理论、实验等学术问题",
            "enhanced": "增强版prompt，包含更详细的引导信息"
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Returns:
            Dict[str, Any]: 性能统计信息
        """
        return {
            "cache_size": len(self.hyde_cache),
            "cached_questions": list(self.hyde_cache.keys()),
            "available_prompt_types": list(self.get_available_prompt_types().keys()),
            "strategy": "hyde_hypothetical_document_embeddings"
        }
    
    def clear_cache(self):
        """清空假设性答案缓存"""
        self.hyde_cache.clear()
        print("Hyde缓存已清空")
    
    def export_hypothetical_answers(self) -> Dict[str, str]:
        """
        导出所有缓存的假设性答案
        
        Returns:
            Dict[str, str]: 问题到假设性答案的映射
        """
        return self.hyde_cache.copy()
