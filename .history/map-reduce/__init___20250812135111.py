"""
Map-Reduce策略包
用于RAG检索优化的并行处理模块
"""

from .runner import LLMMapReduceRunner
from .template import MAP_TEMPLATE, REDUCE_TEMPLATE, DEFAULT_CHUNK_COUNT, MAX_CONCURRENT_REQUESTS

__all__ = [
    'LLMMapReduceRunner',
    'MAP_TEMPLATE', 
    'REDUCE_TEMPLATE',
    'DEFAULT_CHUNK_COUNT',
    'MAX_CONCURRENT_REQUESTS'
]

__version__ = "1.0.0"
__author__ = "RAG优化团队"
__description__ = "基于Map-Reduce策略的RAG检索优化模块" 