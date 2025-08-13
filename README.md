# RAG 检索优化策略集合

## 📖 项目简介

本项目提供了一套完整的RAG（检索增强生成）系统优化策略，通过多种不同的技术方案来提升检索效果和答案质量。项目包含四种核心策略，每种策略都针对不同的应用场景和性能需求进行了深度优化。

## 🚀 核心策略

### 1. Query Decomposition (查询分解策略)
- **核心思想**: 将复杂查询分解为多个简单的子查询，并行处理后整合结果
- **适用场景**: 复杂多维问题、技术架构分析、综合性问题
- **主要优势**: 
  - 提高检索精度
  - 增强答案完整性 
  - 提升系统鲁棒性
- **文档**: [查看详细文档](query_decomposition/notes.md)

### 2. Refine (迭代优化策略)
- **核心思想**: 通过多轮迭代检索，逐步累积和完善答案质量
- **适用场景**: 知识密集型查询、对比分析类问题、需要深度信息整合的场景
- **主要优势**:
  - 信息覆盖度提升
  - 答案质量渐进优化
  - 自适应检索深度
- **文档**: [查看详细文档](refine/notes.md)

### 3. Map-Reduce (分布式处理策略)
- **核心思想**: 将大规模context分割成独立块进行并行处理，然后汇总整合
- **适用场景**: 大量文档处理、高并发需求、对响应速度要求较高的场景
- **主要优势**:
  - 显著的处理速度提升 (4-8倍)
  - 良好的可扩展性
  - 充分利用计算资源
- **文档**: [查看详细文档](map_reduce/notes.md)

### 4. HyDE (假设性文档嵌入策略)
- **核心思想**: 先生成假设性答案，再用该答案进行向量检索，最后基于真实文档生成最终答案
- **适用场景**: 语义匹配要求高、专业领域查询、用户表达与文档表达差异较大的场景
- **主要优势**:
  - 提升检索召回率
  - 增强检索精度
  - 改善语义匹配效果
- **文档**: [查看详细文档](hyde/notes.md)

## 📊 策略对比

| 策略 | 处理速度 | 答案质量 | 可扩展性 | 资源消耗 | 实现复杂度 | 适用场景 |
|------|----------|----------|----------|----------|------------|----------|
| **Query Decomposition** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 复杂问题分析 |
| **Refine** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 知识密集型查询 |
| **Map-Reduce** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 大规模文档处理 |
| **HyDE** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 语义检索优化 |


### 基本配置

```python
# config.py
LLM_API_URL = "your-llm-api-url"
LLM_API_KEY = "your-api-key"
```

### 使用示例

#### 1. Query Decomposition 策略

```python
from query_decomposition.runner import QueryDecompositionRunner
from config import LLM_API_KEY, LLM_API_URL

runner = QueryDecompositionRunner(
    llm_api_key=LLM_API_KEY, 
    llm_api_url=LLM_API_URL
)

question = "如何构建高性能的微服务监控系统？"
result = await runner.run_async(question, context_data)
```

#### 2. Refine 策略

```python
from refine.runner import RefineRunner

runner = RefineRunner(
    llm_api_key=LLM_API_KEY, 
    llm_api_url=LLM_API_URL
)

question = "区块链技术在供应链管理中的应用"
result = await runner.run_async(question, retrieval_func)
```

#### 3. Map-Reduce 策略

```python
from map_reduce.runner import LLMMapReduceRunner

runner = LLMMapReduceRunner(
    llm_api_key=LLM_API_KEY, 
    llm_api_url=LLM_API_URL
)

question = "什么是智能体，能用在哪些领域？"
result = await runner.run_async(question, knowledge_base, chunk_count=4)
```

#### 4. HyDE 策略

```python
from hyde.runner import HydeRunner

runner = HydeRunner(
    llm_api_key=LLM_API_KEY, 
    llm_api_url=LLM_API_URL
)

question = "什么是智能体？"
result = await runner.run(question, retrieval_func, top_k=5)
```

## 🎯 最佳实践

### 策略选择指南

1. **大规模文档处理** → 优先选择 **Map-Reduce**
2. **复杂多维问题** → 推荐使用 **Query Decomposition** 
3. **高质量答案需求** → 建议采用 **Refine** 策略
4. **语义匹配优化** → 适合使用 **HyDE** 策略


## 📚 详细文档

- [Query Decomposition 详细说明](query_decomposition/notes.md)
- [Refine 策略文档](refine/notes.md)  
- [Map-Reduce 技术文档](map_reduce/notes.md)
- [HyDE 使用指南](hyde/notes.md)

