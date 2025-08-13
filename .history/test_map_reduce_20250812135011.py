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
    
    # 显示性能统计
    stats = runner.get_performance_stats(knowledge, chunk_count=4)
    print("\n📊 性能统计信息:")
    print(f"总context数量: {stats['total_context_items']}")
    print(f"分割chunk数: {stats['chunk_count']}")
    print(f"各chunk大小: {stats['chunk_sizes']}")
    print(f"平均chunk大小: {stats['avg_chunk_size']:.1f}")
    print(f"最大并发数: {stats['max_concurrent_requests']}")
    print(f"预估加速比: {stats['estimated_parallel_speedup']}")
    
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
    asyncio.run(test_map_reduce())
    
    # 运行流式处理测试
    asyncio.run(test_map_reduce_stream()) 