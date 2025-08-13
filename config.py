import os

# 大模型调用地址
from dotenv import load_dotenv
load_dotenv()

# 大模型调用API Key
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL")

