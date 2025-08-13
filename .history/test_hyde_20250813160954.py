"""
HyDE策略测试文件
"""

from config import LLM_API_KEY, LLM_API_URL
from hyde.runner import HydeRunner
import asyncio
import json
import time


def create_simple_retrieval_func(knowledge_base):
    """
    创建一个简单的检索函数，基于关键词匹配进行文档检索
    
    Args:
        knowledge_base: 知识库列表
        
    Returns:
        function: 检索函数
    """
    def retrieval_func(query_text, top_k=5):
        """
        简单的检索函数实现
        
        Args:
            query_text: 查询文本
            top_k: 返回的文档数量
            
        Returns:
            List[str]: 相关文档列表
        """
        # 简单的关键词匹配检索
        # 将查询文本分词，然后计算每个文档的相关度分数
        query_words = set(query_text.lower().replace('，', ',').replace('。', '.').replace('？', '?').replace('！', '!').split())
        
        doc_scores = []
        for i, doc in enumerate(knowledge_base):
            # 计算文档与查询的关键词重叠度
            doc_words = set(doc.lower().split())
            overlap = len(query_words.intersection(doc_words))
            if overlap > 0:
                doc_scores.append((overlap, i, doc))
        
        # 按相关度排序并返回top_k个结果
        doc_scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, _, doc in doc_scores[:top_k]]
    
    return retrieval_func


async def test_hyde():
    """测试HyDE策略的基本功能"""
    
    # 初始化runner
    runner = HydeRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    # 加载知识库
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    # 创建检索函数
    retrieval_func = create_simple_retrieval_func(knowledge)
    
    question = "什么是智能体,能用在哪些领域?"
    
    print("=" * 60)
    print("HyDE策略测试")
    print("=" * 60)
    
    print(f"\n❓ 问题: {question}")
    print("\n" + "=" * 60)
    
    # 异步执行HyDE策略
    start_time = time.time()
    result = await runner.run(question, retrieval_func, top_k=5)
    end_time = time.time()
    
    print("=" * 60)
    print("🎯 最终答案:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    print(f"⏱️  总处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)


async def test_hyde_hypothetical_answer():
    """测试HyDE策略的假设性答案生成"""
    
    runner = HydeRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    
    with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
        knowledge = json.load(f)
    
    retrieval_func = create_simple_retrieval_func(knowledge)
    
    question = "智能体的核心技术包括哪些?"
    
    final_result = await runner.run(question, retrieval_func, top_k=5)
    
    end_time = time.time()
    
    print("=" * 60)
    print("🎯 最终答案:")
    print("=" * 60)
    print(final_result)
    print("=" * 60)
    print(f"⏱️  总处理时间: {end_time - start_time:.2f}秒")
    print("=" * 60)


if __name__ == "__main__":
    # 运行基本测试
    # asyncio.run(test_hyde())
    
    # 运行假设性答案生成测试
    asyncio.run(test_hyde_hypothetical_answer())