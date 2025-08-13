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

# 问题分类prompt - 用于自动检测问题类型
QUESTION_CLASSIFICATION_PROMPT = """
你是一个专业的问题分类专家。请分析以下问题，并将其归类到最合适的类别中。

**分类标准**：

**技术类 (technical)**：
- 编程、算法、代码实现相关
- 系统架构、技术框架、工具使用
- 软件开发、数据库、API设计
- 性能优化、调试、技术原理
- 关键词：代码、编程、算法、架构、系统、开发、技术、实现、框架、性能

**商业类 (business)**：
- 市场营销、销售策略、商业模式
- 管理运营、客户服务、产品规划
- 财务分析、竞争策略、品牌建设
- 商业决策、盈利模式、市场分析
- 关键词：市场、销售、客户、产品、管理、策略、营销、竞争、品牌、盈利

**学术类 (academic)**：
- 科学研究、理论分析、实验设计
- 学术论文、文献综述、研究方法
- 数据统计、模型建立、假设验证
- 学科知识、理论探讨、前沿研究
- 关键词：研究、理论、实验、学术、科学、数据、模型、分析、论文、文献

**通用增强类 (enhanced)**：
- 综合性问题，涉及多个领域
- 复杂的概念解释和知识问答
- 需要深入分析的一般性问题
- 不明确属于以上三类的问题

**问题**：{question}

**分析要求**：
1. 仔细分析问题的核心内容和关键词
2. 考虑问题的应用场景和目标受众
3. 选择最符合的单一类别
4. 给出简短的分类理由

**请按以下格式回答**：
分类结果：[technical/business/academic/enhanced]
分类理由：[30字以内的简短说明]
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


