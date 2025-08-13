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
        
        print(f"正在生成假设性答案 (问题类型: {prompt_type})...")
        
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
    
    def run(self, question: str, retrieval_func, prompt_type: Optional[str] = None, 
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
        final_answer_prompt = FINAL_ANSWER_PROMPT.format(question=question, context=retrieved_docs)
        messages = self.create_messages(user_content=final_answer_prompt)
        final_answer = self.call_llm_sync(messages)
        
        print("=== Hyde策略执行完成 ===")
        
        return final_answer
    
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
        context = retrieval_func(hypothetical_answer, top_k=top_k)
        print(f"检索到 {len(context)} 个相关文档")
        
        if isinstance(context, list):
            context = "\n\n".join([f"文档{i+1}:\n{doc}" for i, doc in enumerate(context)])
        # 步骤3: 基于真实检索文档异步生成最终答案
        print("正在基于检索文档异步生成最终答案...")
        final_answer_prompt = FINAL_ANSWER_PROMPT.format(question=question, context=context)
        messages = self.create_messages(user_content=final_answer_prompt)
        final_answer = await self.call_llm_async(messages)
        
        print("=== Hyde策略异步执行完成 ===")
        
        return final_answer


