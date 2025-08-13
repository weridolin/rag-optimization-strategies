import os

# 大模型调用地址
LLM_API_URL = "https://api.deepseek.com"
from dotenv import load_dotenv
load_dotenv()

# 大模型调用API Key
LLM_API_KEY = os.getenv("LLM_API_KEY")
print(LLM_API_KEY)

