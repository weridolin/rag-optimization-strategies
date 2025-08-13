#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    print("开始测试 HyDE 功能...")
    
    # 导入测试
    from hyde.runner import HydeRunner
    print("✓ HydeRunner 导入成功")
    
    from config import LLM_API_KEY, LLM_API_URL
    print("✓ 配置加载成功")
    
    # 初始化测试
    runner = HydeRunner(llm_api_key=LLM_API_KEY, llm_api_url=LLM_API_URL)
    print("✓ HydeRunner 初始化成功")
    
    # 测试问题分类
    question = "什么是智能体?"
    print(f"\n测试问题: {question}")
    
    prompt_type = runner.auto_detect_prompt_type(question)
    print(f"✓ 自动检测问题类型: {prompt_type}")
    
    print("\n测试完成!")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc() 