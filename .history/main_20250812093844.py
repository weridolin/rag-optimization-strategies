class AsyncGenerator:
    def __init__(self, data):
        self.data = data
    def __aiter__(self):
        self.index = 0
        return self
    async def __anext__(self):
        if self.index >= len(self.data):
            raise StopAsyncIteration
        val = self.data[self.index]
        self.index += 1
        return val

async def get_data():
    return AsyncGenerator([1, 2, 3])

async def main():
    async for chunk in await get_data():
        print(chunk)

# 运行
import asyncio
asyncio.run(main())
