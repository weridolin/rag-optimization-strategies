HYDE_PROMPT_TEMPLATE = """
你是一个知识渊博的专家，擅长根据问题生成详细、全面的答案。

请基于以下问题，生成一个假设性的、理想的、详细的答案。这个答案应该：
1. 包含丰富的上下文信息和背景知识
2. 提供具体的细节、数据、例子和解释
3. 覆盖问题的多个相关方面
4. 使用专业术语和相关概念
5. 结构清晰，逻辑连贯

**重要说明**：这个答案是为了向量检索优化而生成的，不需要保证完全准确。重点是生成语义丰富、上下文充实的内容。

**用户问题**：{question}

**请生成一个详细的假设性答案**：
"""

def generate_hyde_prompt(question: str) -> str:
    """
    生成Hyde策略的prompt，用于生成假设性答案
    
    Args:
        question: 用户的原始问题
        
    Returns:
        str: 格式化后的prompt
    """
    return HYDE_PROMPT_TEMPLATE.format(question=question)

# 示例使用
if __name__ == "__main__":
    sample_question = "什么是深度学习中的注意力机制？"
    prompt = generate_hyde_prompt(sample_question)
    print(prompt)
