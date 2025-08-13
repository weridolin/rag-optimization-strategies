from config import LLM_API_KEY, LLM_API_URL
from refine.runner import LLMRefineRunner

if __name__ == "__main__":
    runner = LLMRefineRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    question = "什么是智能体？"
    iterate_account = 3
    context = []
    answer = runner.run(question, iterate_account, context)
    print(answer)