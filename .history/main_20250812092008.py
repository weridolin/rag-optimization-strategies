'''
Author: werido 359066432@qq.com
Date: 2025-08-11 23:56:27
LastEditors: werido 359066432@qq.com
LastEditTime: 2025-08-12 09:19:46
FilePath: \rag-perf\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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
    print(answer)