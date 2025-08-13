"""
Query Decomposition策略测试文件
"""

from config import LLM_API_KEY, LLM_API_URL
from query_decomposition.runner import QueryDecompositionRunner
import asyncio
import json
import time


async def test_query_decomposition():
    """测试Query Decomposition策略的基本功能"""
    
    # 初始化runner
    runner = QueryDecompositionRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    # 加载知识库
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "什么是智能体，它的核心组件和应用领域有哪些？"
    
    print("=" * 60)
    print("Query Decomposition策略测试")
    print("=" * 60)
    
    print(f"\n❓ 问题: {question}")
    print("\n" + "=" * 60)
    
    # 异步执行Query Decomposition策略
    start_time = time.time()
    result = await runner.run_async(question, knowledge)
    end_time = time.time()
    
    print("=" * 60)
    print("🎯 最终答案:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print(f"⏱️  总处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)


async def test_complex_question():
    """测试Query Decomposition策略处理复杂问题的能力"""
    
    runner = QueryDecompositionRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "智能体的BDI架构是什么,强化学习在智能体中如何应用？多智能体系统有什么特点和优势？"
    
    print("\n" + "=" * 60)
    print("Query Decomposition策略复杂问题测试")
    print("=" * 60)
    print(f"❓ 问题: {question}")
    print("=" * 60)
    
    start_time = time.time()
    result = await runner.run_async(question, knowledge)
    end_time = time.time()
    
    print("=" * 60)
    print("🎯 最终答案:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print(f"📝 结果长度: {len(result)} 字符")
    print(f"⏱️  处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)


async def test_different_questions():
    """测试Query Decomposition策略在不同类型问题下的表现"""
    
    runner = QueryDecompositionRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    questions = [
        "智能体的学习能力如何实现？",
        "智能体在自动驾驶中的应用原理是什么？",
        "反应式智能体和计划式智能体有什么区别？",
        "多智能体系统中的协调机制包括哪些方法？"
    ]
    
    print("\n" + "=" * 60)
    print("Query Decomposition策略多问题测试")
    print("=" * 60)
    
    total_start_time = time.time()
    
    for i, question in enumerate(questions, 1):
        print(f"\n🔍 测试问题 {i}: {question}")
        print("-" * 50)
        
        start_time = time.time()
        result = await runner.run_async(question, knowledge)
        end_time = time.time()
        
        print(f"📝 结果长度: {len(result)} 字符")
        print(f"⏱️  处理时间: {end_time - start_time:.2f}秒")
        print(f"📄 答案预览: {result[:100]}...")
        print("-" * 50)
    
    total_end_time = time.time()
    print("=" * 60)
    print(f"🕐 总测试时间: {total_end_time - total_start_time:.2f}秒")
    print(f"📊 平均每题时间: {(total_end_time - total_start_time) / len(questions):.2f}秒")
    print("=" * 60)


async def test_sync_vs_async():
    """对比同步和异步版本的性能"""
    
    runner = QueryDecompositionRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "智能体的核心技术和应用场景有哪些？"
    
    print("\n" + "=" * 60)
    print("Query Decomposition策略同步 vs 异步测试")
    print("=" * 60)
    print(f"❓ 问题: {question}")
    print("=" * 60)
    
    # 测试同步版本
    print("\n🔄 同步版本测试:")
    print("-" * 40)
    
    sync_start_time = time.time()
    sync_result = runner.run(question, knowledge)
    sync_end_time = time.time()
    
    print(f"📝 结果长度: {len(sync_result)} 字符")
    print(f"⏱️  同步处理时间: {sync_end_time - sync_start_time:.2f}秒")
    print(f"📄 答案预览: {sync_result[:100]}...")
    
    # 测试异步版本
    print("\n⚡ 异步版本测试:")
    print("-" * 40)
    
    async_start_time = time.time()
    async_result = await runner.run_async(question, knowledge)
    async_end_time = time.time()
    
    print(f"📝 结果长度: {len(async_result)} 字符")
    print(f"⏱️  异步处理时间: {async_end_time - async_start_time:.2f}秒")
    print(f"📄 答案预览: {async_result[:100]}...")
    
    # 性能对比
    print("\n📊 性能对比:")
    print("-" * 40)
    time_diff = sync_end_time - sync_start_time - (async_end_time - async_start_time)
    if time_diff > 0:
        print(f"🚀 异步版本快了 {time_diff:.2f}秒")
    elif time_diff < 0:
        print(f"🐌 同步版本快了 {abs(time_diff):.2f}秒")
    else:
        print("🤝 两版本性能相当")
    
    print("=" * 60)


if __name__ == "__main__":
    # 运行基本测试
    # asyncio.run(test_query_decomposition())
    
    # 运行复杂问题测试
    asyncio.run(test_complex_question())
    
    # 运行多问题测试
    # asyncio.run(test_different_questions())
    
    # 运行同步vs异步对比测试
    # asyncio.run(test_sync_vs_async())


