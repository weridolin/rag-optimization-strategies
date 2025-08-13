# RAG查询分解策略使用示例

from template import (
    get_decomposition_prompt, 
    get_summarization_prompt,
    get_domain_specific_prompt
)

def example_query_decomposition():
    """查询分解示例"""
    
    # 示例1：复杂技术问题
    user_query = "如何在Python中实现一个高性能的分布式缓存系统？"
    
    print("=== 查询分解示例 ===")
    print(f"原始问题: {user_query}")
    print("\n生成的分解Prompt:")
    print("-" * 50)
    
    decomposition_prompt = get_decomposition_prompt(user_query)
    print(decomposition_prompt)
    
    # 模拟大模型返回的分解结果
    mock_decomposition_result = {
        "original_query": "如何在Python中实现一个高性能的分布式缓存系统？",
        "sub_queries": [
            {
                "id": 1,
                "question": "Python中有哪些可用的分布式缓存解决方案和框架？",
                "focus": "技术选型和可用工具"
            },
            {
                "id": 2,
                "question": "分布式缓存系统的核心架构组件有哪些？",
                "focus": "系统架构设计"
            },
            {
                "id": 3,
                "question": "如何在Python中实现缓存的一致性和数据同步？",
                "focus": "一致性保证机制"
            },
            {
                "id": 4,
                "question": "分布式缓存系统的性能优化策略有哪些？",
                "focus": "性能优化方法"
            }
        ],
        "reasoning": "将复杂的分布式缓存实现问题分解为技术选型、架构设计、一致性机制和性能优化四个核心方面"
    }
    
    return user_query, mock_decomposition_result

def example_result_summarization():
    """结果汇总示例"""
    
    original_query, decomposition = example_query_decomposition()
    
    # 模拟子问题的答案
    sub_queries = [item["question"] for item in decomposition["sub_queries"]]
    sub_answers = [
        "Python中主要的分布式缓存解决方案包括Redis、Memcached、Hazelcast等。Redis是最受欢迎的选择，提供了丰富的数据结构和集群支持。",
        "分布式缓存系统的核心组件包括：缓存节点、负载均衡器、一致性哈希环、故障检测机制、数据分片策略等。",
        "可以通过一致性哈希、向量时钟、分布式锁等机制来保证数据一致性。Redis Cluster提供了自动故障转移和数据同步功能。",
        "性能优化策略包括：合理的数据分片、连接池管理、异步I/O、批量操作、内存优化、网络优化等。"
    ]
    
    print("\n\n=== 结果汇总示例 ===")
    print("生成的汇总Prompt:")
    print("-" * 50)
    
    summarization_prompt = get_summarization_prompt(original_query, sub_queries, sub_answers)
    print(summarization_prompt)

def example_domain_specific():
    """特定领域prompt示例"""
    
    print("\n\n=== 特定领域Prompt示例 ===")
    
    # 技术领域示例
    tech_query = "微服务架构中如何处理分布式事务？"
    tech_prompt = get_domain_specific_prompt("technical", tech_query)
    
    print("技术领域Prompt:")
    print("-" * 30)
    print(tech_prompt)
    
    # 商业领域示例
    business_query = "如何提高电商平台的用户留存率？"
    business_prompt = get_domain_specific_prompt("business", business_query)
    
    print("\n商业领域Prompt:")
    print("-" * 30)
    print(business_prompt)

def rag_workflow_example():
    """完整的RAG工作流程示例"""
    
    print("\n\n=== 完整RAG查询分解工作流程 ===")
    print("1. 接收用户查询")
    print("2. 生成查询分解prompt")
    print("3. 大模型分解问题")
    print("4. 针对每个子问题进行RAG检索")
    print("5. 收集所有子问题答案")
    print("6. 生成结果汇总prompt")
    print("7. 大模型汇总最终答案")
    
    workflow_code = """
# 伪代码示例
def rag_with_query_decomposition(user_query, llm, retriever):
    # 步骤1: 查询分解
    decomp_prompt = get_decomposition_prompt(user_query)
    decomposition = llm.generate(decomp_prompt)
    
    # 步骤2: 分别处理子问题
    sub_answers = []
    for sub_query in decomposition['sub_queries']:
        # RAG检索
        retrieved_docs = retriever.search(sub_query['question'])
        
        # 生成答案
        qa_prompt = f"基于以下文档回答问题：\\n文档：{retrieved_docs}\\n问题：{sub_query['question']}"
        answer = llm.generate(qa_prompt)
        sub_answers.append(answer)
    
    # 步骤3: 结果汇总
    summary_prompt = get_summarization_prompt(
        user_query, 
        [q['question'] for q in decomposition['sub_queries']], 
        sub_answers
    )
    final_answer = llm.generate(summary_prompt)
    
    return final_answer
"""
    
    print("\n工作流程伪代码:")
    print("-" * 40)
    print(workflow_code)

if __name__ == "__main__":
    # 运行所有示例
    example_query_decomposition()
    example_result_summarization()
    example_domain_specific()
    rag_workflow_example() 