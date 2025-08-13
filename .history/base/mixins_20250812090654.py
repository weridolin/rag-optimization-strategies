
import asyncio
from typing import Any, Dict, List, Optional, Union, AsyncGenerator, Generator
from openai import OpenAI, AsyncOpenAI

DEFAULT_SYSTEM_PROMPT:str = """你是一个专业的问答助手，专门根据提供的上下文信息来回答用户的问题。请遵循以下规则：

1. **严格基于上下文**：只使用提供的context上下文信息来回答问题，不要添加任何上下文中没有的信息。

2. **准确性优先**：如果上下文中没有足够的信息来回答问题，请明确说明"根据提供的上下文信息，无法回答这个问题"或"上下文中没有包含相关信息"。

3. **结构化回答**：
   - 直接回答用户的核心问题
   - 提供相关的详细信息和解释
   - 如果有多个相关点，请分点列出

4. **引用意识**：在回答时，可以提及信息来源于上下文，如"根据提供的资料"、"文档中提到"等。

5. **保持客观**：以中性、客观的语调回答，避免主观判断和推测。

6. **完整性检查**：确保回答完整地解决了用户的问题，如果问题有多个部分，请逐一回应。

请根据即将提供的上下文信息，准确回答用户的问题。"""



class LLMCallMixin:
    """调用 LLM 的通用混合类，支持同步/异步调用和 stream/非stream 模式"""
    
    def __init__(self, llm_api_key: str, llm_api_url: str, model: str = "deepseek-chat"):
        self.llm_api_key = llm_api_key
        self.llm_api_url = llm_api_url
        self.model = model
        self._client = None
        self._async_client = None
    
    @property
    def client(self) -> OpenAI:
        """获取同步客户端"""
        if self._client is None:
            self._client = OpenAI(api_key=self.llm_api_key, base_url=self.llm_api_url)
        return self._client
    
    @property
    def async_client(self) -> AsyncOpenAI:
        """获取异步客户端"""
        if self._async_client is None:
            self._async_client = AsyncOpenAI(api_key=self.llm_api_key, base_url=self.llm_api_url)
        return self._async_client
    
    def call_llm_sync(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """
        同步调用 LLM
        
        Args:
            messages: 消息列表
            stream: 是否使用流式输出
            **kwargs: 其他参数传递给 API
        
        Returns:
            str: 非流式模式下返回完整响应
            Generator: 流式模式下返回生成器
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            **kwargs
        )
        
        if stream:
            return self._process_stream_response(response)
        else:
            return response.choices[0].message.content
    
    async def call_llm_async(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        """
        异步调用 LLM
        
        Args:
            messages: 消息列表
            stream: 是否使用流式输出
            **kwargs: 其他参数传递给 API
        
        Returns:
            str: 非流式模式下返回完整响应
            AsyncGenerator: 流式模式下返回异步生成器
        """
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            **kwargs
        )
        
        if stream:
            return self._process_async_stream_response(response)
        else:
            return response.choices[0].message.content
    
    def _process_stream_response(self, response) -> Generator[str, None, None]:
        """处理同步流式响应"""
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def _process_async_stream_response(self, response) -> AsyncGenerator[str, None]:
        """处理异步流式响应"""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def create_messages(
        self,
        user_content: str,
        system_content: str = DEFAULT_SYSTEM_PROMPT,
        history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """
        创建消息列表的辅助方法
        
        Args:
            user_content: 用户消息内容
            system_content: 系统消息内容
            history: 历史对话记录
        
        Returns:
            List[Dict[str, str]]: 格式化的消息列表
        """
        messages = [{"role": "system", "content": system_content}]
        
        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": user_content})
        return messages
