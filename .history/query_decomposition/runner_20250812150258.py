import json
import asyncio
from typing import List, Dict, Any
from query_decomposition.template import QUERY_DECOMPOSITION_PROMPT, RESULT_SUMMARIZATION_PROMPT
from base.mixins import LLMCallMixin


class QueryDecompositionRunner(LLMCallMixin):
    def __init__(self, llm_api_key: str, llm_api_url: str):
        super().__init__(llm_api_key, llm_api_url)

    def run(self, question: str, context: list[str], retrieval_func=None) -> str:
        """
        同步执行query decomposition策略
        
        Args:
            question: 用户问题
            context: 初始上下文信息
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
            
            # 如果提供了检索函数，使用它检索相关上下文
            if retrieval_func:
                sub_context = retrieval_func(sub_query['question'])
                context_str = "\n".join(sub_context if sub_context else context)
            else:
                context_str = "\n".join(context)
            
            # 使用上下文回答子问题
            sub_answer = self._answer_sub_query(sub_query['question'], context_str)
            
            sub_qa_pairs.append({
                'question': sub_query['question'],
                'focus': sub_query['focus'],
                'answer': sub_answer
            })
            print(f"子问题{i}回答完成")
        
        # 3. 汇总所有答案
        print("\n=== 开始汇总答案 ===")
        final_answer = self._summarize_answers(question, sub_qa_pairs)
        print("汇总完成")
        
        return final_answer

    async def run_async(self, question: str, context: list[str]) -> str:
        """
        异步执行query decomposition策略
        
        Args:
            question: 用户问题
            context: 初始上下文信息
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
            task = self._process_sub_query_async(sub_query, context, i)
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
        prompt = f"""
基于以下上下文信息，请回答问题：

上下文信息：
{context}

问题：{sub_question}

请提供准确、简洁的回答：
"""
        messages = self.create_messages(user_content=prompt)
        return self.call_llm_sync(messages)

    async def _answer_sub_query_async(self, sub_question: str, context: str) -> str:
        """异步回答单个子问题"""
        prompt = f"""
基于以下上下文信息，请回答问题：

上下文信息：
{context}

问题：{sub_question}

请提供准确、简洁的回答：
"""
        messages = self.create_messages(user_content=prompt)
        return await self.call_llm_async(messages)

    async def _process_sub_query_async(self, sub_query: Dict[str, Any], context: list[str], index: int = 1) -> Dict[str, Any]:
        """异步处理单个子问题"""
        try:
            context_str = "\n".join(context)
            
            # 回答子问题
            sub_answer = await self._answer_sub_query_async(sub_query['question'], context_str)
            
            print(f"子问题{index}处理完成: {sub_query['question'][:50]}...")
            
            return {
                'question': sub_query['question'],
                'focus': sub_query['focus'],
                'answer': sub_answer
            }
        except Exception as e:
            print(f"处理子问题{index}时出错: {e}")
            return {
                'question': sub_query['question'],
                'focus': sub_query['focus'],
                'answer': f"处理该子问题时出现错误: {str(e)}"
            }

    def _summarize_answers(self, original_question: str, sub_qa_pairs: List[Dict[str, Any]]) -> str:
        """汇总所有子问题的答案"""
        # 格式化子问题和答案
        formatted_qa = []
        for i, qa in enumerate(sub_qa_pairs, 1):
            formatted_qa.append(f"""
子问题{i}: {qa['question']}
关注点: {qa['focus']}
回答: {qa['answer']}
""")
        
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
        for i, qa in enumerate(sub_qa_pairs, 1):
            formatted_qa.append(f"""
子问题{i}: {qa['question']}
关注点: {qa['focus']}
回答: {qa['answer']}
""")
        
        sub_qa_text = "\n".join(formatted_qa)
        
        messages = self.create_messages(
            user_content=RESULT_SUMMARIZATION_PROMPT.format(
                original_query=original_question,
                sub_qa_pairs=sub_qa_text
            )
        )
        
        return await self.call_llm_async(messages)
