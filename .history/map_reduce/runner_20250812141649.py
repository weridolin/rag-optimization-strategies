import asyncio
from typing import List, Dict, Any
from .template import MAP_TEMPLATE, REDUCE_TEMPLATE, DEFAULT_CHUNK_COUNT, MAX_CONCURRENT_REQUESTS
from base.mixins import LLMCallMixin


class LLMMapReduceRunner(LLMCallMixin):
    """基于Map-Reduce策略的RAG检索优化处理器"""
    
    def __init__(self, llm_api_key: str, llm_api_url: str):
        super().__init__(llm_api_key, llm_api_url)
    
    def run(self, question: str, context: List[str], chunk_count: int = DEFAULT_CHUNK_COUNT) -> str:
        """        
        Args:
            question: 用户问题
            context: 上下文信息列表
            chunk_count: 分割的chunk数量
            
        Returns:
            str: 最终整合的答案
        """
        # Map阶段：分割context并并行处理
        context_chunks = self._split_context(context, chunk_count)
        map_results = []
        
        print(f"Map阶段：将context分割为{len(context_chunks)}个部分进行处理...")
        
        for i, chunk in enumerate(context_chunks):
            print(f"处理第{i+1}个chunk...")
            chunk_context = "\n".join(chunk)
            messages = self.create_messages(
                user_content=MAP_TEMPLATE.format(
                    chunk_index=i+1,
                    context=chunk_context,
                    question=question
                )
            )
            result = self.call_llm_sync(messages)
            map_results.append(f"片段{i+1}的回答:\n{result}")
        
        # Reduce阶段：整合所有结果
        print("Reduce阶段：整合所有片段的回答...")
        combined_results = "\n\n".join(map_results)
        messages = self.create_messages(
            user_content=REDUCE_TEMPLATE.format(
                question=question,
                map_results=combined_results
            )
        )
        final_answer = self.call_llm_sync(messages)
        
        return final_answer
    
    async def run_async(self, question: str, context: List[str], chunk_count: int = DEFAULT_CHUNK_COUNT) -> str:
        """        
        Args:
            question: 用户问题
            context: 上下文信息列表
            chunk_count: 分割的chunk数量
            
        Returns:
            str: 最终整合的答案
        """
        # Map阶段：分割context并并行处理
        context_chunks = self._split_context(context, chunk_count)
        
        print(f"Map阶段：将context分割为{len(context_chunks)}个部分进行并行处理...")
        
        # 并行执行Map任务
        map_tasks = []
        for i, chunk in enumerate(context_chunks):
            task = self._process_chunk_async(chunk, question, i+1)
            map_tasks.append(task)
        
        # 控制并发数量
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        async def limited_task(task):
            async with semaphore:
                return await task
        
        map_results = await asyncio.gather(*[limited_task(task) for task in map_tasks])
        
        # Reduce阶段：整合所有结果
        print("Reduce阶段：整合所有片段的回答...")
        combined_results = "\n\n".join([f"片段{i+1}的回答:\n{result}" 
                                    for i, result in enumerate(map_results)])
        
        messages = self.create_messages(
            user_content=REDUCE_TEMPLATE.format(
                question=question,
                map_results=combined_results
            )
        )
        final_answer = await self.call_llm_async(messages)
        
        return final_answer
    
    async def run_async_stream(self, question: str, context: List[str], chunk_count: int = DEFAULT_CHUNK_COUNT) -> str:
        """
        异步流式执行Map-Reduce策略，实时显示处理过程
        
        Args:
            question: 用户问题
            context: 上下文信息列表
            chunk_count: 分割的chunk数量
            
        Returns:
            str: 最终整合的答案
        """
        # Map阶段：分割context并并行处理
        context_chunks = self._split_context(context, chunk_count)
        
        print(f"Map阶段:将context分割为{len(context_chunks)}个部分进行并行处理...")
        
        # 并行执行Map任务
        map_tasks = []
        for i, chunk in enumerate(context_chunks):
            task = self._process_chunk_async(chunk, question, i+1)
            map_tasks.append(task)
        
        # 控制并发数量
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        async def limited_task(task):
            async with semaphore:
                return await task
        
        map_results = await asyncio.gather(*[limited_task(task) for task in map_tasks])
        
        # Reduce阶段：流式整合所有结果
        print("Reduce阶段:整合所有片段的回答...")
        combined_results = "\n\n".join([f"片段{i+1}的回答:\n{result}"  for i, result in enumerate(map_results)])
        
        messages = self.create_messages(
            user_content=REDUCE_TEMPLATE.format(
                question=question,
                map_results=combined_results
            )
        )
        
        final_answer = ""
        async for chunk in await self.call_llm_async(messages, stream=True):
            print(chunk, end='', flush=True)
            final_answer += chunk
        print("")
        
        return final_answer
    
    def _split_context(self, context: List[str], chunk_count: int) -> List[List[str]]:
        """
        将上下文信息分割为指定数量的chunk
        
        Args:
            context: 上下文信息列表
            chunk_count: 分割的chunk数量
            
        Returns:
            List[List[str]]: 分割后的context chunks
        """
        if not context:
            return []
        
        chunk_size = max(1, len(context) // chunk_count)
        chunks = []
        
        for i in range(0, len(context), chunk_size):
            chunk = context[i:i + chunk_size]
            chunks.append(chunk)
        
        # 确保不超过指定的chunk数量
        if len(chunks) > chunk_count:
            # 将最后几个小chunk合并到倒数第二个chunk中
            last_chunks = chunks[chunk_count-1:]
            merged_chunk = []
            for chunk in last_chunks:
                merged_chunk.extend(chunk)
            chunks = chunks[:chunk_count-1] + [merged_chunk]
        
        return chunks
    
    async def _process_chunk_async(self, chunk: List[str], question: str, chunk_index: int) -> str:
        """
        异步处理单个chunk
        
        Args:
            chunk: 单个context chunk
            question: 用户问题
            chunk_index: chunk索引(用于显示)
            
        Returns:
            str: 该chunk的处理结果
        """
        chunk_context = "\n".join(chunk)
        messages = self.create_messages(
            user_content=MAP_TEMPLATE.format(
                chunk_index=chunk_index,
                context=chunk_context,
                question=question
            )
        )
        print(f"  - 处理第{chunk_index}个chunk...")
        result = await self.call_llm_async(messages)
        print(f"  - 第{chunk_index}个chunk处理完成")
        return result
    
    def get_performance_stats(self, context: List[str], chunk_count: int = DEFAULT_CHUNK_COUNT) -> Dict[str, Any]:
        """
        获取性能统计信息
        
        Args:
            context: 上下文信息列表
            chunk_count: 分割的chunk数量
            
        Returns:
            Dict[str, Any]: 性能统计信息
        """
        chunks = self._split_context(context, chunk_count)
        
        return {
            "total_context_items": len(context),
            "chunk_count": len(chunks),
            "chunk_sizes": [len(chunk) for chunk in chunks],
            "avg_chunk_size": sum(len(chunk) for chunk in chunks) / len(chunks) if chunks else 0,
            "max_concurrent_requests": MAX_CONCURRENT_REQUESTS,
            "estimated_parallel_speedup": f"{min(len(chunks), MAX_CONCURRENT_REQUESTS)}x"
        }
