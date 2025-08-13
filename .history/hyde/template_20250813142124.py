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
4. 结果只需要返回分类结果(technical/business/academic/enhanced)，不需要任何解释

"""

# 基于检索context生成最终答案的prompt
FINAL_ANSWER_PROMPT = """
你是一个专业的知识问答专家。现在需要你基于检索到的相关文档，为用户的问题提供准确、详细的最终答案。

**用户问题**：{question}

**检索到的相关文档**：
{context}

**回答要求**：
1. **准确性优先**：严格基于提供的文档内容进行回答，不要添加文档中没有的信息
2. **引用支撑**：在回答中明确引用具体的文档内容作为支撑
3. **结构清晰**：组织答案结构，使用标题、要点等方式提高可读性
4. **完整全面**：综合多个文档的信息，提供全面的答案
5. **诚实表达**：如果文档信息不足或存在矛盾，请明确说明
6. **重点突出**：针对用户问题的核心需求，突出最重要的信息

**答案格式**：
请按以下结构组织你的回答：

## 核心答案
[直接回答用户问题的核心内容]

## 详细说明
[基于文档的详细解释和补充信息]

## 相关要点
[其他相关的重要信息]

## 参考依据
[说明答案基于哪些文档内容]

**开始回答**：
"""

# 技术类问题的最终答案prompt
TECHNICAL_FINAL_ANSWER_PROMPT = """
你是一个资深技术专家。基于检索到的技术文档，为用户提供专业、实用的技术解答。

**技术问题**：{question}

**技术文档资料**：
{context}

**技术回答要求**：
1. **技术准确性**：确保所有技术细节、代码示例、配置参数等完全准确
2. **实用性**：提供可直接应用的解决方案和最佳实践
3. **代码示例**：如果文档中有代码，请在回答中包含相关代码片段
4. **技术原理**：解释技术实现的底层原理和机制
5. **注意事项**：指出可能的坑点、限制条件和注意事项
6. **版本兼容性**：如果涉及版本问题，请明确说明

**请提供技术解答**：
"""

# 商业类问题的最终答案prompt
BUSINESS_FINAL_ANSWER_PROMPT = """
你是一个经验丰富的商业顾问。基于检索到的商业资料，为用户提供实用的商业建议和分析。

**商业问题**：{question}

**商业资料**：
{context}

**商业回答要求**：
1. **实用性**：提供可操作的商业建议和具体行动方案
2. **数据支撑**：如果文档中有数据、案例，请在回答中引用
3. **风险评估**：分析可能的风险和挑战
4. **成本效益**：考虑实施的成本和预期收益
5. **市场环境**：结合市场环境和行业背景分析
6. **可行性**：评估建议的可行性和实施难度

**请提供商业分析**：
"""

# 学术类问题的最终答案prompt
ACADEMIC_FINAL_ANSWER_PROMPT = """
你是一个严谨的学术研究专家。基于检索到的学术文献和资料，为用户提供科学、严谨的学术回答。

**学术问题**：{question}

**学术资料**：
{context}

**学术回答要求**：
1. **科学严谨**：确保所有结论都有充分的文献支撑
2. **文献引用**：明确引用相关研究、理论和数据来源
3. **客观中立**：保持学术客观性，避免主观臆断
4. **理论框架**：基于相关理论框架进行分析
5. **研究方法**：如果涉及研究方法，请详细说明
6. **学术争议**：如果存在不同观点，请客观呈现

**请提供学术分析**：
"""


PROMPT_TYPES = {
    "technical": HYDE_TECHNICAL_PROMPT,
    "business": HYDE_BUSINESS_PROMPT,
    "academic": HYDE_ACADEMIC_PROMPT,
    "enhanced": HYDE_ENHANCED_PROMPT
}

# 最终答案prompt模板映射
FINAL_ANSWER_PROMPTS = {
    "technical": TECHNICAL_FINAL_ANSWER_PROMPT,
    "business": BUSINESS_FINAL_ANSWER_PROMPT,
    "academic": ACADEMIC_FINAL_ANSWER_PROMPT,
    "enhanced": FINAL_ANSWER_PROMPT,
    "general": FINAL_ANSWER_PROMPT
}

def generate_final_answer_prompt(question: str, context: str, prompt_type: str = "general") -> str:
    """
    根据问题类型生成最终答案的prompt
    
    Args:
        question: 用户的原始问题
        context: 检索到的相关文档内容
        prompt_type: 问题类型 ("technical", "business", "academic", "enhanced", "general")
        
    Returns:
        str: 格式化后的最终答案prompt
    """
    template = FINAL_ANSWER_PROMPTS.get(prompt_type, FINAL_ANSWER_PROMPT)
    return template.format(question=question, context=context)

def generate_hyde_prompt(question: str, prompt_type: str = "enhanced") -> str:
    """
    生成Hyde策略的prompt，用于生成假设性答案
    
    Args:
        question: 用户的原始问题
        prompt_type: prompt类型 ("technical", "business", "academic", "enhanced")
        
    Returns:
        str: 格式化后的prompt
    """
    template = PROMPT_TYPES.get(prompt_type, HYDE_ENHANCED_PROMPT)
    return template.format(question=question)

def generate_classification_prompt(question: str) -> str:
    """
    生成问题分类的prompt
    
    Args:
        question: 用户的原始问题
        
    Returns:
        str: 格式化后的分类prompt
    """
    return QUESTION_CLASSIFICATION_PROMPT.format(question=question)