'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2025-08-11 15:36:40
platform: windows 10
LastEditors: lhj
LastEditTime: 2025-08-11 23:54:59
'''
from .template import INITIAL_TEMPLATE,REFINE_TEMPLATE
from base.mixins import LLMCallMixin

class LLMRefineRunner(LLMCallMixin):
    def __init__(self, llm_api_key: str, llm_api_url: str):
        super().__init__(llm_api_key, llm_api_url)


    def run(self, question: str, iterate_account: str, context: list[str]) -> str:
        # 将上下文分成 iterate_account 个部分
        chunk_size = max(1, len(context) // iterate_account)
        context_chunks = [context[i:i + chunk_size] for i in range(0, len(context), chunk_size)]
        
        # 确保不超过指定的迭代次数
        context_chunks = context_chunks[:iterate_account]
        
        # 第一次迭代使用初始模板
        first_context = "\n".join(context_chunks[0])
        messages = self.create_messages(
            user_content=INITIAL_TEMPLATE.format(context=first_context, question=question)
        )
        current_answer = self.call_llm_sync(messages)
        
        # 后续迭代使用refinement模板
        for i in range(1, len(context_chunks)):
            chunk_context = "\n".join(context_chunks[i])
            messages = self.create_messages(
                user_content=REFINE_TEMPLATE.format(
                    question=question,
                    existing_answer=current_answer,
                    context=chunk_context
                )
            )
            current_answer = self.call_llm_sync(messages)
        
        return current_answer



if __name__ == "__main__":
    runner = LLMRefineRunner(llm_api_key="", llm_api_url="")
    question = "什么是智能体？"
    iterate_account = 3
    context = []
    answer = runner.run(question, iterate_account, context)
    print(answer)
