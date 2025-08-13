from query_decomposition.runner import QueryDecompositionRunner
from config import LLM_API_KEY, LLM_API_URL
import asyncio


def test_query_decomposition():
    runner = QueryDecompositionRunner(
        llm_api_key=LLM_API_KEY,
        llm_api_url=LLM_API_URL
    )
    runner.run()


