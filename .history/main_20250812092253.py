from config import LLM_API_KEY, LLM_API_URL
from refine.runner import LLMRefineRunner
import json

with open("ai_agent_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

if __name__ == "__main__":
    runner = LLMRefineRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    question = "什么是智能体,能用在哪些领域?"
    iterate_account = 3
    context = knowledge
    answer = runner.run(question, iterate_account, context)
    print("最终答案")
    print(answer)