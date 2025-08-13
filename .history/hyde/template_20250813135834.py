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

# 针对技术问题的专用prompt
HYDE_TECHNICAL_PROMPT = """
作为一名资深技术专家，请针对以下技术问题生成一个详细的假设性答案。

你的答案应该包含：
- 技术背景和原理解释
- 具体的实现方法和代码示例
- 相关的技术栈、工具和框架
- 最佳实践和常见陷阱
- 性能考量和优化策略
- 相关的技术概念和术语

**技术问题**：{question}

**详细技术解答**：
"""

# 针对商业/业务问题的专用prompt
HYDE_BUSINESS_PROMPT = """
作为一名经验丰富的商业顾问，请针对以下业务问题提供一个全面的假设性分析。

你的分析应该涵盖：
- 问题的商业背景和市场环境
- 相关的商业模式和策略框架
- 具体的解决方案和实施步骤
- 风险评估和机会分析
- 行业最佳实践和案例研究
- 相关的商业术语和概念

**业务问题**：{question}

**商业分析**：
"""

# 针对学术/研究问题的专用prompt
HYDE_ACADEMIC_PROMPT = """
作为一名学术研究专家，请针对以下学术问题提供一个深入的假设性论述。

你的论述应该包含：
- 理论基础和文献背景
- 研究方法和实验设计
- 数据分析和结果解释
- 学术争议和不同观点
- 未来研究方向和影响
- 相关的学术术语和概念

**学术问题**：{question}

**学术论述**：
"""

# 增强版通用prompt，包含更多引导
HYDE_ENHANCED_PROMPT = """
请扮演该领域的权威专家，针对以下问题生成一个详尽的假设性答案。

**答案要求**：
✓ 从多个角度全面分析问题
✓ 提供具体的事实、数据和案例
✓ 包含相关的专业术语和概念
✓ 解释因果关系和内在逻辑
✓ 提及相关的工具、方法或框架
✓ 讨论潜在的挑战和解决方案
✓ 语言丰富，信息密度高

**问题**：{question}

**开始详细解答**：
让我为您详细分析这个问题...
"""

def generate_hyde_prompt(question: str, prompt_type: str = "general") -> str:
    """
    生成Hyde策略的prompt，用于生成假设性答案
    
    Args:
        question: 用户的原始问题
        prompt_type: prompt类型 ("general", "technical", "business", "academic", "enhanced")
        
    Returns:
        str: 格式化后的prompt
    """
    prompt_templates = {
        "general": HYDE_PROMPT_TEMPLATE,
        "technical": HYDE_TECHNICAL_PROMPT,
        "business": HYDE_BUSINESS_PROMPT,
        "academic": HYDE_ACADEMIC_PROMPT,
        "enhanced": HYDE_ENHANCED_PROMPT
    }
    
    template = prompt_templates.get(prompt_type, HYDE_PROMPT_TEMPLATE)
    return template.format(question=question)

def auto_detect_prompt_type(question: str) -> str:
    """
    根据问题内容自动检测最适合的prompt类型
    
    Args:
        question: 用户问题
        
    Returns:
        str: 推荐的prompt类型
    """
    question_lower = question.lower()
    
    # 技术关键词
    tech_keywords = [
        "代码", "编程", "算法", "api", "数据库", "框架", "库", "技术", 
        "实现", "开发", "系统", "架构", "性能", "优化", "bug", "debug"
    ]
    
    # 商业关键词
    business_keywords = [
        "商业", "市场", "营销", "销售", "客户", "用户", "产品", "服务",
        "策略", "管理", "运营", "盈利", "成本", "竞争", "品牌"
    ]
    
    # 学术关键词
    academic_keywords = [
        "研究", "理论", "实验", "分析", "论文", "学术", "科学", "方法",
        "模型", "假设", "数据", "统计", "文献", "期刊"
    ]
    
    tech_score = sum(1 for keyword in tech_keywords if keyword in question_lower)
    business_score = sum(1 for keyword in business_keywords if keyword in question_lower)
    academic_score = sum(1 for keyword in academic_keywords if keyword in question_lower)
    
    if tech_score >= business_score and tech_score >= academic_score and tech_score > 0:
        return "technical"
    elif business_score >= academic_score and business_score > 0:
        return "business"
    elif academic_score > 0:
        return "academic"
    else:
        return "enhanced"  # 使用增强版作为默认

# 示例使用
if __name__ == "__main__":
    test_questions = [
        "什么是深度学习中的注意力机制？",
        "如何提高产品的市场占有率？",
        "机器学习在自然语言处理中的应用研究现状如何？",
        "Python中如何实现多线程编程？"
    ]
    
    for question in test_questions:
        prompt_type = auto_detect_prompt_type(question)
        prompt = generate_hyde_prompt(question, prompt_type)
        print(f"问题：{question}")
        print(f"检测到的类型：{prompt_type}")
        print(f"生成的prompt：\n{prompt}\n" + "="*50 + "\n")
