# 第5月学习代码示例（asyncio 与并发请求）
# asyncio基础、异步HTTP请求、并发工具化、WebSocket

import asyncio
import json
import time
from typing import List

print("=== 1. asyncio 基础 ===\n")

print("--- 协程与事件循环 ---")
print("""
异步编程关键概念：
  - 协程（Coroutine）：可暂停和恢复的函数
  - 事件循环：调度和运行协程
  - await：等待协程完成
  - async def：定义协程函数

优点：
  - 高效处理 I/O 密集型任务
  - 单线程并发（避免线程同步问题）
  - 支持大量并发连接
""")

print("--- 基础协程示例 ---")
print("""
import asyncio

async def hello(name):
    print(f"Hello {name}")
    await asyncio.sleep(1)  # 模拟异步操作
    return f"Done {name}"

# 运行协程
async def main():
    result = await hello("Alice")
    print(result)

asyncio.run(main())
""")

print("\n--- 并发执行多个协程 ---")
print("""
async def main():
    # 方式1：使用 gather
    results = await asyncio.gather(
        hello("Alice"),
        hello("Bob"),
        hello("Charlie")
    )
    print(results)
    
    # 方式2：创建任务
    tasks = [
        asyncio.create_task(hello(name))
        for name in ["Alice", "Bob", "Charlie"]
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
""")

print("\n=== 2. asyncio 实用工具类 ===\n")

class AsyncHTTPClient:
    """异步 HTTP 客户端示例"""
    
    def __init__(self, max_concurrent=10):
        self.max_concurrent = max_concurrent
        self.semaphore = None
    
    async def fetch(self, url, retries=3):
        """获取单个 URL（带重试）"""
        if self.semaphore is None:
            self.semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async with self.semaphore:
            for attempt in range(retries):
                try:
                    print(f"获取: {url} (尝试 {attempt + 1})")
                    # 模拟网络请求
                    await asyncio.sleep(0.1)
                    return {'url': url, 'status': 200, 'data': 'success'}
                
                except Exception as e:
                    if attempt == retries - 1:
                        return {'url': url, 'error': str(e)}
                    await asyncio.sleep(2 ** attempt)
    
    async def fetch_many(self, urls):
        """获取多个 URL（限制并发数）"""
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks)

print("--- 异步客户端使用示例 ---")
print("""
async def main():
    client = AsyncHTTPClient(max_concurrent=5)
    urls = ['http://example.com/1', 'http://example.com/2', ...]
    
    results = await client.fetch_many(urls)
    for result in results:
        print(result)

asyncio.run(main())
""")

print("\n=== 3. 并发限制与超时控制 ===\n")

class AsyncTaskPool:
    """异步任务池"""
    
    def __init__(self, max_workers=10, timeout=30):
        self.max_workers = max_workers
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(max_workers)
    
    async def run_with_timeout(self, coro):
        """带超时的协程执行"""
        try:
            return await asyncio.wait_for(coro, timeout=self.timeout)
        except asyncio.TimeoutError:
            return {'error': 'timeout'}
    
    async def submit(self, coro):
        """提交协程（自动限制并发）"""
        async with self.semaphore:
            return await self.run_with_timeout(coro)
    
    async def map(self, func, items):
        """批量处理（限制并发）"""
        tasks = [self.submit(func(item)) for item in items]
        return await asyncio.gather(*tasks)

print("--- 任务池示例 ---")
print("""
async def fetch_url(url):
    await asyncio.sleep(0.1)
    return f"Fetched {url}"

async def main():
    pool = AsyncTaskPool(max_workers=5, timeout=10)
    urls = ['url1', 'url2', 'url3', ...]
    
    results = await pool.map(fetch_url, urls)
    print(results)

asyncio.run(main())
""")

print("\n=== 4. 异步上下文管理 ===\n")

print("--- 异步上下文管理示例 ---")
print("""
class AsyncResourceManager:
    async def __aenter__(self):
        print("获取资源")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")
        await asyncio.sleep(0.1)

async def main():
    async with AsyncResourceManager() as manager:
        print("使用资源")

asyncio.run(main())
""")

print("\n=== 5. 异步生产者-消费者 ===\n")

class AsyncQueue:
    """异步队列示例"""
    
    def __init__(self, maxsize=0):
        self.queue = asyncio.Queue(maxsize=maxsize)
    
    async def producer(self, items, delay=0.1):
        """生产者"""
        for item in items:
            print(f"生产: {item}")
            await self.queue.put(item)
            await asyncio.sleep(delay)
        await self.queue.put(None)  # 结束标记
    
    async def consumer(self, consumer_id):
        """消费者"""
        while True:
            item = await self.queue.get()
            if item is None:
                break
            print(f"消费者 {consumer_id}: 处理 {item}")
            await asyncio.sleep(0.2)

print("--- 生产者-消费者示例 ---")
print("""
async def main():
    queue = AsyncQueue()
    
    # 创建一个生产者和多个消费者
    producer_task = asyncio.create_task(
        queue.producer(['A', 'B', 'C', 'D', 'E'])
    )
    
    consumer_tasks = [
        asyncio.create_task(queue.consumer(i))
        for i in range(3)
    ]
    
    await asyncio.gather(producer_task, *consumer_tasks)

asyncio.run(main())
""")

print("\n=== 6. WebSocket 基础 ===\n")

print("--- WebSocket 概念 ---")
print("""
WebSocket 是 HTML5 提供的持久双向通信协议：
  - 建立在 TCP 之上
  - 支持全双工通信
  - 适合实时应用（聊天、行情等）
  - 与 HTTP 兼容性好

握手过程：
  1. 客户端发送 HTTP upgrade 请求
  2. 服务器响应 101 Switching Protocols
  3. 连接升级为 WebSocket

常见库：
  - websockets：轻量级 WebSocket 库
  - python-socketio：更高级的实时通信库
""")

print("\n--- WebSocket 客户端示例 ---")
print("""
import websockets
import json

async def websocket_client():
    async with websockets.connect('wss://echo.websocket.org') as websocket:
        # 发送消息
        await websocket.send("Hello Server")
        
        # 接收消息
        response = await websocket.recv()
        print(f"收到: {response}")
        
        # 保持连接并处理消息
        async for message in websocket:
            print(f"消息: {message}")

asyncio.run(websocket_client())
""")

print("\n--- WebSocket 服务端示例 ---")
print("""
import websockets

async def websocket_server(websocket, path):
    try:
        async for message in websocket:
            print(f"收到: {message}")
            # 回复消息
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("连接已关闭")

async def main():
    async with websockets.serve(websocket_server, "localhost", 8765):
        await asyncio.Future()  # 永久运行

asyncio.run(main())
""")

print("\n=== 7. 实用的异步工具 ===\n")

class AsyncTools:
    """异步工具集合"""
    
    @staticmethod
    async def sleep_and_retry(delay, max_retries):
        """延迟重试"""
        for i in range(max_retries):
            yield i
            if i < max_retries - 1:
                await asyncio.sleep(delay)
    
    @staticmethod
    async def gather_with_limit(coros, limit):
        """限制并发的 gather"""
        semaphore = asyncio.Semaphore(limit)
        
        async def bounded_coro(coro):
            async with semaphore:
                return await coro
        
        return await asyncio.gather(*(bounded_coro(c) for c in coros))
    
    @staticmethod
    async def timeout_with_fallback(coro, timeout, fallback_value=None):
        """带后备值的超时"""
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            return fallback_value

print("--- 异步工具使用示例 ---")
print("工具已定义，可用于异步编程")

print("\n=== 8. asyncio 最佳实践 ===\n")

print("""
1. 使用 asyncio.gather() 并发执行多个协程
2. 使用 Semaphore 限制并发数
3. 使用 Queue 处理任务队列
4. 用 try/except 处理超时异常
5. 避免在协程中使用 time.sleep()，改用 await asyncio.sleep()
6. 使用 asyncio.create_task() 而非直接 await
7. 合理使用 timeout 避免长时间挂起
8. 使用日志记录异步操作便于调试
""")
