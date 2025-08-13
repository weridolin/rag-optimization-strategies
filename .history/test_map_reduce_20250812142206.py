"""
Map-Reduce策略测试文件
"""

from config import LLM_API_KEY, LLM_API_URL
from map_reduce.runner import LLMMapReduceRunner
import asyncio
import json
import time

async def test_map_reduce():
    """测试Map-Reduce策略的基本功能"""
    
    # 初始化runner
    runner = LLMMapReduceRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    # 加载知识库
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "什么是智能体,能用在哪些领域?"
    
    print("=" * 60)
    print("Map-Reduce策略测试")
    print("=" * 60)
    
    print(f"\n❓ 问题: {question}")
    print("\n" + "=" * 60)
    
    # 异步执行Map-Reduce策略
    start_time = time.time()
    result = await runner.run_async(question, knowledge, chunk_count=4)
    end_time = time.time()
    
    print("=" * 60)
    print("🎯 最终答案:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print(f"⏱️  总处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)

async def test_map_reduce_stream():
    """测试Map-Reduce策略的流式处理"""
    
    runner = LLMMapReduceRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "智能体的核心技术包括哪些?"
    
    print("\n" + "=" * 60)
    print("Map-Reduce流式处理测试")
    print("=" * 60)
    print(f"❓ 问题: {question}")
    print("=" * 60)
    
    start_time = time.time()
    result = await runner.run_async_stream(question, knowledge, chunk_count=4)
    end_time = time.time()
    
    print("=" * 60)
    print(f"⏱️  总处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)

if __name__ == "__main__":
    # 运行基本测试
    # asyncio.run(test_map_reduce())
    
    # 运行流式处理测试
    asyncio.run(test_map_reduce_stream()) 