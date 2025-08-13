#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def log(msg):
    with open("debug.log", "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
    print(msg)

try:
    log("=== HyDE 调试测试开始 ===")
    
    # 基本导入测试
    log("1. 测试基本导入...")
    import json
    log("   - json 导入成功")
    
    import asyncio
    log("   - asyncio 导入成功")
    
    # OpenAI 导入测试
    log("2. 测试 OpenAI 导入...")
    from openai import OpenAI, AsyncOpenAI
    log("   - OpenAI 导入成功")
    
    # 配置导入测试
    log("3. 测试配置导入...")
    from config import LLM_API_KEY, LLM_API_URL
    log(f"   - 配置导入成功, URL: {LLM_API_URL}")
    
    # Base 模块导入测试
    log("4. 测试 base 模块导入...")
    from base.mixins import LLMCallMixin
    log("   - LLMCallMixin 导入成功")
    
    # HyDE 模块导入测试
    log("5. 测试 HyDE 模块导入...")
    from hyde.runner import HydeRunner
    log("   - HydeRunner 导入成功")
    
    # 初始化测试
    log("6. 测试 HydeRunner 初始化...")
    runner = HydeRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    log("   - HydeRunner 初始化成功")
    
    log("=== 所有测试通过 ===")
    
except Exception as e:
    log(f"❌ 错误: {e}")
    import traceback
    log(f"错误详情: {traceback.format_exc()}") 