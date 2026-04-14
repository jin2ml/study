# 第3月第2周学习代码示例
# 根据第3月第2周的学习内容（requests / httpx 基础），这些示例覆盖了GET、POST、Header、JSON提交、form提交。

import json

print("=== 1. requests 库基础（模拟） ===\n")

# 注：实际使用需要 pip install requests
# 这里展示 requests 库的用法示例和基本概念

print("--- requests 库介绍 ---")
print("""
requests 是 Python 最流行的 HTTP 客户端库
特点：
  - 简单易用的 API
  - 自动处理 Cookie 和 Session
  - 支持 timeout、重试等
  - 可以设置代理

安装：pip install requests
""")

print("\n--- GET 请求示例 ---")
print("""
import requests

# 简单 GET 请求
response = requests.get('https://api.example.com/users')
print(response.status_code)
print(response.json())

# 带参数的 GET 请求
params = {'page': 1, 'limit': 10}
response = requests.get('https://api.example.com/users', params=params)

# 带 Header 的 GET 请求
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'Bearer token123'
}
response = requests.get('https://api.example.com/users', headers=headers)
""")

print("\n--- POST 请求 (JSON) ---")
print("""
# POST JSON 数据
data = {
    'name': 'Alice',
    'email': 'alice@example.com',
    'age': 25
}
response = requests.post('https://api.example.com/users', json=data)

# 等价于：
response = requests.post(
    'https://api.example.com/users',
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)
""")

print("\n--- POST 请求 (Form) ---")
print("""
# POST 表单数据
data = {
    'username': 'alice',
    'password': 'secret123'
}
response = requests.post('https://example.com/login', data=data)

# 自动设置 Content-Type: application/x-www-form-urlencoded
""")

print("\n--- 请求超时和重试 ---")
print("""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 设置超时
response = requests.get('https://api.example.com/data', timeout=5)

# 超时参数详解
# timeout=5                    -> 连接和读取都是 5 秒
# timeout=(3.05, 27)           -> 连接 3.05 秒，读取 27 秒
response = requests.get(
    'https://api.example.com/data',
    timeout=(3.05, 27)
)

# 实现重试机制
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

response = session.get('https://api.example.com/data')
""")

print("\n--- 响应对象常用属性 ---")
print("""
response.status_code      # 状态码 (200, 404 等)
response.headers          # 响应头 (dict)
response.content          # 响应体（字节）
response.text             # 响应体（字符串）
response.json()           # 响应体（解析 JSON）
response.url              # 最终的 URL（重定向后）
response.history          # 重定向历史
response.elapsed          # 响应耗时
response.cookies          # Cookie 对象
""")

print("\n=== 2. httpx 库基础 ===\n")

print("--- httpx 库介绍 ---")
print("""
httpx 是新一代 HTTP 客户端库，支持异步
特点：
  - 支持 HTTP/2
  - 原生异步支持
  - API 与 requests 兼容
  - 更现代的实现

安装：pip install httpx
""")

print("\n--- httpx 基本用法 ---")
print("""
import httpx

# 同步请求（与 requests 最为相似）
with httpx.Client() as client:
    response = client.get('https://api.example.com/users')
    print(response.status_code)
    print(response.json())

# 异步请求
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/users')
        return response.json()
""")

print("\n=== 3. 实用请求函数封装 ===\n")

class SimpleHTTPClient:
    """简化的 HTTP 客户端"""
    
    def __init__(self, base_url='', default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.session_cookies = {}
    
    def _build_url(self, path):
        """构建完整 URL"""
        if path.startswith('http'):
            return path
        return self.base_url + path
    
    def _merge_headers(self, headers):
        """合并默认headers和自定义headers"""
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged
    
    def get(self, path, params=None, headers=None):
        """模拟 GET 请求"""
        url = self._build_url(path)
        headers = self._merge_headers(headers)
        
        # 构建查询字符串
        if params:
            import urllib.parse
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"
        
        return {
            'method': 'GET',
            'url': url,
            'headers': headers
        }
    
    def post(self, path, data=None, json_data=None, headers=None):
        """模拟 POST 请求"""
        url = self._build_url(path)
        headers = self._merge_headers(headers)
        
        if json_data is not None:
            headers['Content-Type'] = 'application/json'
            body = json.dumps(json_data)
        elif data is not None:
            if isinstance(data, dict):
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                import urllib.parse
                body = urllib.parse.urlencode(data)
            else:
                body = data
        else:
            body = None
        
        return {
            'method': 'POST',
            'url': url,
            'headers': headers,
            'body': body
        }
    
    def put(self, path, json_data=None, headers=None):
        """模拟 PUT 请求"""
        url = self._build_url(path)
        headers = self._merge_headers(headers)
        headers['Content-Type'] = 'application/json'
        
        body = json.dumps(json_data) if json_data else None
        
        return {
            'method': 'PUT',
            'url': url,
            'headers': headers,
            'body': body
        }
    
    def delete(self, path, headers=None):
        """模拟 DELETE 请求"""
        url = self._build_url(path)
        headers = self._merge_headers(headers)
        
        return {
            'method': 'DELETE',
            'url': url,
            'headers': headers
        }

# 使用示例
print("--- 请求客户端示例 ---\n")

client = SimpleHTTPClient(
    base_url='https://api.example.com',
    default_headers={'User-Agent': 'Python-Client/1.0'}
)

# GET 请求
get_request = client.get('/users', params={'page': 1, 'limit': 10})
print("GET 请求:")
print(f"  URL: {get_request['url']}")
print(f"  Headers: {get_request['headers']}")

# POST JSON
post_json = client.post('/users', json_data={'name': 'Alice', 'age': 25})
print("\nPOST JSON 请求:")
print(f"  URL: {post_json['url']}")
print(f"  Headers: {post_json['headers']}")
print(f"  Body: {post_json['body']}")

# POST Form
post_form = client.post('/login', data={'username': 'alice', 'password': 'secret'})
print("\nPOST Form 请求:")
print(f"  URL: {post_form['url']}")
print(f"  Headers: {post_form['headers']}")
print(f"  Body: {post_form['body']}")

print("\n=== 4. 常见 API 调用模式 ===\n")

print("--- 模式1：获取列表（分页） ---")
api_client = SimpleHTTPClient(base_url='https://api.github.com')
request = api_client.get(
    '/users/octocat/repos',
    params={'page': 1, 'per_page': 30}
)
print(f"请求: {request['method']} {request['url']}")

print("\n--- 模式2：创建资源 ---")
new_user = {
    'username': 'newuser',
    'email': 'new@example.com',
    'password': 'secret123'
}
request = api_client.post('/users', json_data=new_user)
print(f"请求: {request['method']} {request['url']}")
print(f"Body: {request['body']}")

print("\n--- 模式3：更新资源 ---")
update_data = {'email': 'updated@example.com'}
request = api_client.put('/users/123', json_data=update_data)
print(f"请求: {request['method']} {request['url']}")

print("\n--- 模式4：删除资源 ---")
request = api_client.delete('/users/123')
print(f"请求: {request['method']} {request['url']}")

print("\n=== 5. 快速参考 ===\n")

print("--- requests 常用方法 ---")
print("""
requests.get(url)           # GET 请求
requests.post(url)          # POST 请求
requests.put(url)           # PUT 请求
requests.patch(url)         # PATCH 请求
requests.delete(url)        # DELETE 请求
requests.head(url)          # HEAD 请求
requests.options(url)       # OPTIONS 请求

参数说明：
  params      # URL 参数 (dict) - GET 专用
  data        # 请求体 (dict/str) - POST/PUT
  json        # JSON 数据 (dict) - 自动序列化和设置 header
  headers     # 请求头 (dict)
  cookies     # Cookie (dict)
  timeout     # 超时时间 (秒)
  verify      # 是否验证 SSL (bool)
  allow_redirects # 是否跟随重定向 (bool)
""")

print("--- 响应对象常用方法 ---")
print("""
response.status_code        # 状态码
response.headers            # 响应头
response.content            # 字节内容
response.text               # 文本内容
response.json()             # 解析为 JSON
response.raise_for_status() # 状态码错误时抛异常
response.iter_content()     # 流式读取（适合大文件）
response.iter_lines()       # 逐行读取
""")
