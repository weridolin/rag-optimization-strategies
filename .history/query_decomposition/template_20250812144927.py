# RAG查询分解与结果汇总Prompt模板

# 查询分解Prompt模板
QUERY_DECOMPOSITION_PROMPT = """
你是一个专业的问题分析专家。你的任务是将用户的复杂问题分解成多个简单、具体的子问题，以便更好地进行信息检索和回答。

## 分解原则：
1. 将复杂问题拆分成2-5个相互独立但相关的子问题
2. 每个子问题应该足够具体，可以通过单次检索获得明确答案
3. 子问题应该覆盖原问题的所有关键方面
4. 保持子问题的逻辑顺序和连贯性
5. 避免重复或过于相似的子问题

## 输出格式：
请按照以下JSON格式输出分解后的子问题：
```json
{
    "original_query": "原始问题",
    "sub_queries": [
        {
            "id": 1,
            "question": "子问题1",
            "focus": "关注点描述"
        },
        {
            "id": 2,
            "question": "子问题2", 
            "focus": "关注点描述"
        }
    ],
    "reasoning": "分解思路说明"
}
```

## 用户问题：
{query}

请对上述问题进行分解：
"""

# 结果汇总Prompt模板
RESULT_SUMMARIZATION_PROMPT = """
你是一个专业的信息整合专家。你需要根据多个子问题的回答，为用户的原始问题提供一个全面、准确、连贯的最终答案。

## 汇总原则：
1. 综合所有子问题的答案，确保信息完整性
2. 消除重复信息，保持答案简洁明了
3. 保持逻辑清晰，按重要性和逻辑顺序组织内容
4. 如果子答案之间存在矛盾，需要明确指出并分析原因
5. 确保最终答案直接回应原始问题
6. 保持客观中立的语调

## 原始问题：
{original_query}

## 子问题及其答案：
{sub_qa_pairs}

## 请提供最终的综合答案：
请基于以上信息，为原始问题提供一个全面、准确的回答。答案应该：
- 直接回应原始问题的核心需求
- 整合所有相关的子问题答案
- 保持逻辑清晰和结构完整
- 突出重点信息
- 如有必要，可以补充相关的背景信息或注意事项
"""

# 辅助函数：格式化子问题和答案对
def format_sub_qa_pairs(sub_queries, sub_answers):
    """
    将子问题和对应答案格式化为字符串
    
    Args:
        sub_queries: 子问题列表
        sub_answers: 对应的答案列表
    
    Returns:
        格式化后的字符串
    """
    formatted_pairs = []
    for i, (query, answer) in enumerate(zip(sub_queries, sub_answers), 1):
        formatted_pairs.append(f"""
### 子问题 {i}：
**问题：** {query}
**答案：** {answer}
""")
    return "\n".join(formatted_pairs)

# 使用示例
def get_decomposition_prompt(user_query):
    """获取查询分解prompt"""
    return QUERY_DECOMPOSITION_PROMPT.format(query=user_query)

def get_summarization_prompt(original_query, sub_queries, sub_answers):
    """获取结果汇总prompt"""
    formatted_qa = format_sub_qa_pairs(sub_queries, sub_answers)
    return RESULT_SUMMARIZATION_PROMPT.format(
        original_query=original_query,
        sub_qa_pairs=formatted_qa
    )

# 高级模板：针对特定领域的查询分解
DOMAIN_SPECIFIC_PROMPTS = {
    "technical": """
    你是一个技术问题分析专家。请将以下技术问题分解成具体的子问题：
    
    分解时请特别关注：
    - 技术原理和机制
    - 实现方法和步骤
    - 可能的问题和解决方案
    - 最佳实践和注意事项
    
    问题：{query}
    """,
    
    "business": """
    你是一个商业分析专家。请将以下商业问题分解成具体的子问题：
    
    分解时请特别关注：
    - 市场环境和背景
    - 关键指标和数据
    - 策略和执行方案
    - 风险和机会分析
    
    问题：{query}
    """,
    
    "research": """
    你是一个研究方法专家。请将以下研究问题分解成具体的子问题：
    
    分解时请特别关注：
    - 核心概念和定义
    - 相关理论和模型
    - 实证证据和案例
    - 研究方法和局限性
    
    问题：{query}
    """
}

def get_domain_specific_prompt(domain, user_query):
    """获取特定领域的查询分解prompt"""
    if domain in DOMAIN_SPECIFIC_PROMPTS:
        return DOMAIN_SPECIFIC_PROMPTS[domain].format(query=user_query)
    else:
        return get_decomposition_prompt(user_query)
