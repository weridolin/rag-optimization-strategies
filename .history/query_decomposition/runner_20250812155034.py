import json
import asyncio
from typing import List, Dict, Any, Callable, Optional, Awaitable
from query_decomposition.template import QUERY_DECOMPOSITION_PROMPT, RESULT_SUMMARIZATION_PROMPT,SINGLE_QUERY_PROMPT
from base.mixins import LLMCallMixin


class QueryDecompositionRunner(LLMCallMixin):
    def __init__(self, llm_api_key: str, llm_api_url: str):
        super().__init__(llm_api_key, llm_api_url)

    def run(self, question: str, context: list[str], retrieval_func: Optional[Callable[[str], List[str]]] = None) -> str:
        """
        同步执行query decomposition策略
        
        Args:
            question: 用户问题
            context: 初始上下文信息（当无检索函数时使用）
            retrieval_func: 检索函数，用于根据子问题检索相关信息
        
        Returns:
            str: 最终汇总答案
        """
        # 1. 分解问题
        print("=== 开始分解问题 ===")
        sub_queries = self._decompose_query(question)
        print(f"分解得到 {len(sub_queries)} 个子问题")
        
        # 2. 对每个子问题进行回答
        print("=== 开始回答子问题 ===")
        sub_qa_pairs = []
        for i, sub_query in enumerate(sub_queries, 1):
            print(f"\n处理第{i}个子问题: {sub_query['question']}")
            
            # 使用检索函数为每个子问题检索最相关的上下文
            if retrieval_func:
                print(f"  正在为子问题{i}检索相关上下文...")
                sub_context = retrieval_func(sub_query['question'])
                if sub_context:
                    context_str = "\n".join(sub_context)
                    print(f"  检索到 {len(sub_context)} 条相关信息")
                else:
                    context_str = "\n".join(context)
                    print(f"  未检索到相关信息，使用默认上下文")
            else:
                context_str = "\n".join(context)
                print(f"  使用默认上下文")
            
            # 使用上下文回答子问题
            sub_answer = self._answer_sub_query(sub_query['question'], context_str)
            
            sub_qa_pairs.append({
                'question': sub_query['question'],
                'focus': sub_query['focus'],
                'answer': sub_answer,
                'context_used': len(sub_context) if retrieval_func and sub_context else len(context)
            })
            print(f"子问题{i}回答完成")
        
        # 3. 汇总所有答案
        print("\n=== 开始汇总答案 ===")
        final_answer = self._summarize_answers(question, sub_qa_pairs)
        print("汇总完成")
        
        return final_answer

    async def run_async(self, question: str, context: list[str], retrieval_func: Optional[Callable[[str], Awaitable[List[str]]]] = None) -> str:
        """
        异步执行query decomposition策略
        
        Args:
            question: 用户问题
            context: 初始上下文信息（当无检索函数时使用）
            retrieval_func: 异步检索函数，用于根据子问题检索相关信息
        
        Returns:
            str: 最终汇总答案
        """
        # 1. 分解问题
        print("=== 开始分解问题 ===")
        sub_queries = await self._decompose_query_async(question)
        print(f"分解得到 {len(sub_queries)} 个子问题")
        
        # 2. 并行处理所有子问题
        print("=== 开始并行处理子问题 ===")
        tasks = []
        for i, sub_query in enumerate(sub_queries, 1):
            print(f"创建第{i}个子问题的处理任务: {sub_query['question']}")
            task = self._process_sub_query_async(sub_query, context, retrieval_func, i)
            tasks.append(task)
        
        # 等待所有子问题处理完成
        sub_qa_pairs = await asyncio.gather(*tasks)
        
        # 3. 汇总所有答案
        print("\n=== 开始汇总答案 ===")
        final_answer = await self._summarize_answers_async(question, sub_qa_pairs)
        print("汇总完成")
        
        return final_answer

    def _decompose_query(self, question: str) -> List[Dict[str, Any]]:
        """分解问题为子问题"""
        messages = self.create_messages(
            user_content=QUERY_DECOMPOSITION_PROMPT.format(query=question)
        )
        
        response = self.call_llm_sync(messages)
        return self._parse_decomposition_result(response)

    async def _decompose_query_async(self, question: str) -> List[Dict[str, Any]]:
        """异步分解问题为子问题"""
        messages = self.create_messages(
            user_content=QUERY_DECOMPOSITION_PROMPT.format(query=question)
        )
        
        response = await self.call_llm_async(messages)
        return self._parse_decomposition_result(response)

    def _parse_decomposition_result(self, response: str) -> List[Dict[str, Any]]:
        """解析分解结果"""
        try:
            # 提取JSON部分
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                return result.get('sub_queries', [])
        except Exception as e:
            print(f"解析分解结果时出错: {e}")
            # 如果解析失败，返回原问题作为单个子问题
            return [{'id': 1, 'question': '原问题', 'focus': '完整回答'}]

    def _answer_sub_query(self, sub_question: str, context: str) -> str:
        """回答单个子问题"""
        prompt = SINGLE_QUERY_PROMPT.format(query=sub_question, context=context)
        messages = self.create_messages(user_content=prompt)
        return self.call_llm_sync(messages)

    async def _answer_sub_query_async(self, sub_question: str, context: str) -> str:
        """异步回答单个子问题"""
        prompt = SINGLE_QUERY_PROMPT.format(query=sub_question, context=context)
        
        messages = self.create_messages(user_content=prompt)
        return await self.call_llm_async(messages)

    async def _process_sub_query_async(self, sub_query: Dict[str, Any],
                                    retrieval_func: Optional[Callable[[str], Awaitable[List[str]]]] = None, 
                                    index: int = 1) -> Dict[str, Any]:
        """异步处理单个子问题"""
        try:
            # 使用检索函数为每个子问题检索最相关的上下文
            if retrieval_func:
                print(f"  正在为子问题{index}检索相关上下文...")
            
                sub_context = await retrieval_func(sub_query['question'])
                if sub_context:
                    context_str = "\n".join(sub_context)
                    context_used = len(sub_context)
                    print(f"  检索到 {len(sub_context)} 条相关信息")
                else:
                    context_str = []
            
            # 回答子问题
            sub_answer = await self._answer_sub_query_async(sub_query['question'], context_str)
            
            print(f"子问题{index}处理完成: {sub_query['question'][:50]}...")
            
            return {
                'question': sub_query['question'],
                'focus': sub_query['focus'],
                'answer': sub_answer,
                'context_used': context_used
            }
        except Exception as e:
            print(f"处理子问题{index}时出错: {e}")
            return {
                'question': sub_query['question'],
                'focus': sub_query['focus'],
                'answer': f"处理该子问题时出现错误: {str(e)}",
                'context_used': 0
            }

    def _summarize_answers(self, original_question: str, sub_qa_pairs: List[Dict[str, Any]]) -> str:
        """汇总所有子问题的答案"""
        # 格式化子问题和答案
        formatted_qa = []
        total_context_used = 0
        
        for i, qa in enumerate(sub_qa_pairs, 1):
            context_info = f" (使用了 {qa.get('context_used', 0)} 条上下文信息)" if 'context_used' in qa else ""
            total_context_used += qa.get('context_used', 0)
            
            formatted_qa.append(f"""
子问题{i}: {qa['question']}
关注点: {qa['focus']}{context_info}
回答: {qa['answer']}
""")
        
        print(f"总共使用了 {total_context_used} 条上下文信息")
        sub_qa_text = "\n".join(formatted_qa)
        
        messages = self.create_messages(
            user_content=RESULT_SUMMARIZATION_PROMPT.format(
                original_query=original_question,
                sub_qa_pairs=sub_qa_text
            )
        )
        
        return self.call_llm_sync(messages)

    async def _summarize_answers_async(self, original_question: str, sub_qa_pairs: List[Dict[str, Any]]) -> str:
        """异步汇总所有子问题的答案"""
        # 格式化子问题和答案
        formatted_qa = []
        total_context_used = 0
        
        for i, qa in enumerate(sub_qa_pairs, 1):
            context_info = f" (使用了 {qa.get('context_used', 0)} 条上下文信息)" if 'context_used' in qa else ""
            total_context_used += qa.get('context_used', 0)
            
            formatted_qa.append(f"""
子问题{i}: {qa['question']}
关注点: {qa['focus']}{context_info}
回答: {qa['answer']}
""")
        
        print(f"总共使用了 {total_context_used} 条上下文信息")
        sub_qa_text = "\n".join(formatted_qa)
        
        messages = self.create_messages(
            user_content=RESULT_SUMMARIZATION_PROMPT.format(
                original_query=original_question,
                sub_qa_pairs=sub_qa_text
            )
        )
        
        return await self.call_llm_async(messages)
