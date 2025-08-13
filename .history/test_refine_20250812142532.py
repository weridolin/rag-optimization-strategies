'''
Author: werido 359066432@qq.com
Date: 2025-08-11 23:56:27
LastEditors: werido 359066432@qq.com
LastEditTime: 2025-08-12 14:25:31
FilePath: \rag-perf\test_refine.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
Refine策略测试文件
"""

from config import LLM_API_KEY, LLM_API_URL
from refine.runner import LLMRefineRunner
import asyncio
import json
import time

async def test_refine():
    """测试Refine策略的基本功能"""
    
    # 初始化runner
    runner = LLMRefineRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    # 加载知识库
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "什么是智能体,能用在哪些领域?"
    iterate_account = 3
    
    print("=" * 60)
    print("Refine策略测试")
    print("=" * 60)
    
    print(f"\n❓ 问题: {question}")
    print(f"🔄 迭代次数: {iterate_account}")
    print("\n" + "=" * 60)
    
    # 异步执行Refine策略
    start_time = time.time()
    result = await runner.run_async(question, iterate_account, knowledge)
    end_time = time.time()
    
    print("=" * 60)
    print("🎯 最终答案:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print(f"⏱️  总处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)

async def test_refine_different_iterations():
    """测试Refine策略在不同迭代次数下的表现"""
    
    runner = LLMRefineRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    question = "智能体的核心技术包括哪些?"
    iteration_counts = [1, 2, 4]
    
    print("\n" + "=" * 60)
    print("Refine策略不同迭代次数测试")
    print("=" * 60)
    print(f"❓ 问题: {question}")
    print("=" * 60)
    
    for iterate_count in iteration_counts:
        print(f"\n🔄 测试迭代次数: {iterate_count}")
        print("-" * 40)
        
        start_time = time.time()
        result = await runner.run_async(question, iterate_count, knowledge)
        end_time = time.time()
        
        print(f"📝 结果长度: {len(result)} 字符")
        print(f"⏱️  处理时间: {end_time - start_time:.2f}秒")
        print(f"📄 答案预览: {result[:100]}...")
        print("-" * 40)
    
    print("=" * 60)

if __name__ == "__main__":
    # 运行基本测试
    # asyncio.run(test_refine())
    
    # 运行不同迭代次数测试
    asyncio.run(test_refine_different_iterations())
