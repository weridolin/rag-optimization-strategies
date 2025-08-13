#!/usr/bin/env python3
"""
Hyde策略使用示例

演示如何使用HydeRunner进行假设性答案生成和检索优化
"""

import asyncio
from typing import List
from hyde.runner import HydeRunner
from hyde.template import generate_hyde_prompt, auto_detect_prompt_type


def mock_retrieval_function(query: str, top_k: int = 5) -> List[str]:
    """
    模拟检索函数 - 在实际应用中，这里会调用向量数据库进行检索
    
    Args:
        query: 查询文本（可能是原始问题或假设性答案）
        top_k: 返回的文档数量
        
    Returns:
        List[str]: 模拟的检索文档
    """
    print(f"模拟检索: 查询='{query[:50]}...', top_k={top_k}")
    
    # 这里只是模拟返回一些相关文档
    mock_docs = [
        "文档1: 深度学习中的注意力机制是一种让模型能够关注输入序列中重要部分的技术...",
        "文档2: Transformer架构中的自注意力机制通过查询、键、值三个矩阵来计算注意力权重...",
        "文档3: 注意力机制的数学原理基于相似度计算，通过softmax函数归一化注意力分数...",
        "文档4: 在自然语言处理任务中，注意力机制显著提升了模型的性能和可解释性...",
        "文档5: 多头注意力机制允许模型同时关注不同位置的信息，增强了表达能力..."
    ]
    
    return mock_docs[:top_k]


def demo_hyde_basic():
    """演示Hyde策略的基本使用"""
    print("=== Hyde策略基本使用演示 ===\n")
    
    # 创建Hyde runner（需要提供实际的API配置）
    # 这里使用模拟配置
    runner = HydeRunner(
        llm_api_key="your-api-key", 
        llm_api_url="your-api-url"
    )
    
    # 测试问题
    question = "什么是深度学习中的注意力机制？"
    
    # 1. 自动检测问题类型
    prompt_type = auto_detect_prompt_type(question)
    print(f"问题: {question}")
    print(f"自动检测的类型: {prompt_type}\n")
    
    # 2. 生成Hyde prompt
    hyde_prompt = generate_hyde_prompt(question, prompt_type)
    print("生成的Hyde Prompt:")
    print("=" * 50)
    print(hyde_prompt)
    print("=" * 50 + "\n")
    
    # 3. 查看可用的prompt类型
    prompt_types = runner.get_available_prompt_types()
    print("可用的Prompt类型:")
    for ptype, description in prompt_types.items():
        print(f"  - {ptype}: {description}")
    print()


def demo_hyde_comparison():
    """演示Hyde策略与baseline的比较"""
    print("=== Hyde策略 vs Baseline 比较演示 ===\n")
    
    runner = HydeRunner(
        llm_api_key="your-api-key", 
        llm_api_url="your-api-url"
    )
    
    question = "如何优化深度学习模型的训练速度？"
    
    # 定义baseline检索函数（直接使用问题检索）
    def baseline_retrieval(query: str, top_k: int = 5) -> List[str]:
        print(f"Baseline检索 - 直接使用问题: '{query}'")
        return mock_retrieval_function(query, top_k)
    
    # 定义hyde检索函数（使用假设性答案检索）
    def hyde_retrieval(hypothetical_answer: str, top_k: int = 5) -> List[str]:
        print(f"Hyde检索 - 使用假设性答案: '{hypothetical_answer[:100]}...'")
        return mock_retrieval_function(hypothetical_answer, top_k)
    
    # 注意：这里只是演示结构，实际运行需要真实的LLM API
    print(f"比较问题: {question}")
    print("在实际使用中，这里会:")
    print("1. 生成假设性答案")
    print("2. 使用假设性答案进行检索")
    print("3. 比较两种方法的检索结果")
    print("4. 生成最终答案并对比效果\n")


async def demo_hyde_async():
    """演示Hyde策略的异步使用"""
    print("=== Hyde策略异步使用演示 ===\n")
    
    runner = HydeRunner(
        llm_api_key="your-api-key", 
        llm_api_url="your-api-url"
    )
    
    questions = [
        "什么是区块链技术？",
        "如何设计高并发系统？",
        "机器学习中的过拟合问题如何解决？"
    ]
    
    print("演示多个问题的并行处理:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")
    print()
    
    # 在实际使用中，这里会并行生成假设性答案
    print("在实际使用中，这里会:")
    print("1. 并行为所有问题生成假设性答案")
    print("2. 并行进行文档检索")
    print("3. 生成最终答案")
    print("4. 显著提升处理速度\n")


def demo_cache_functionality():
    """演示缓存功能"""
    print("=== Hyde策略缓存功能演示 ===\n")
    
    runner = HydeRunner(
        llm_api_key="your-api-key", 
        llm_api_url="your-api-url"
    )
    
    # 模拟缓存一些假设性答案
    runner.hyde_cache = {
        "什么是人工智能?:technical": "人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统...",
        "如何提高销售业绩?:business": "提高销售业绩需要从多个维度进行优化，包括客户关系管理、产品定位、销售流程优化..."
    }
    
    # 展示性能统计
    stats = runner.get_performance_stats()
    print("性能统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # 展示导出功能
    exported = runner.export_hypothetical_answers()
    print("已缓存的假设性答案:")
    for question, answer in exported.items():
        print(f"  问题: {question}")
        print(f"  答案: {answer[:100]}...")
        print()


def main():
    """主函数 - 运行所有演示"""
    print("Hyde策略完整演示\n")
    print("注意: 这是演示代码，需要配置真实的LLM API才能运行\n")
    
    # 运行各种演示
    demo_hyde_basic()
    print("\n" + "="*80 + "\n")
    
    demo_hyde_comparison()
    print("\n" + "="*80 + "\n")
    
    asyncio.run(demo_hyde_async())
    print("\n" + "="*80 + "\n")
    
    demo_cache_functionality()
    
    print("演示完成！")
    print("\n使用说明:")
    print("1. 配置LLM API密钥和URL")
    print("2. 实现真实的向量检索函数")
    print("3. 根据需要调整prompt类型")
    print("4. 可以通过缓存提升重复查询的性能")


if __name__ == "__main__":
    main() 