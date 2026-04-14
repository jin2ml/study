# 第3月第4周学习代码示例
# 根据第3月第4周的学习内容（请求复现与上传下载），这些示例覆盖了文件上传、文件下载、代理设置、按抓包记录复现。

import io
import json
from pathlib import Path

print("=== 1. 文件上传 ===\n")

print("--- 文件上传概念 ---")
print("""
文件上传使用 multipart/form-data 编码
包含：
  1. 文本字段
  2. 文件字段
  3. 每个字段用边界（boundary）分隔

请求头：
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

requests 库会自动处理编码
""")

print("\n--- 单文件上传 ---")
print("""
import requests

# 上传单个文件
files = {'file': open('image.jpg', 'rb')}
response = requests.post('https://example.com/upload', files=files)

# 更简洁的方式
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('https://example.com/upload', files=files)
""")

print("\n--- 多文件上传 ---")
print("""
# 上传多个文件
files = [
    ('file1', open('file1.txt', 'rb')),
    ('file2', open('file2.txt', 'rb')),
    ('file3', open('file3.jpg', 'rb'))
]
response = requests.post('https://example.com/upload', files=files)
""")

print("\n--- 文件上传 + 表单字段 ---")
print("""
# 上传文件和其他数据
files = {'file': open('document.pdf', 'rb')}
data = {
    'title': 'My Document',
    'description': 'A PDF file',
    'category': 'documents'
}
response = requests.post(
    'https://example.com/upload',
    files=files,
    data=data
)

# 手动指定文件名和MIME类型
files = {'file': ('myfile.txt', open('file.txt', 'rb'), 'text/plain')}
response = requests.post('https://example.com/upload', files=files)
""")

print("\n=== 2. 文件下载 ===\n")

class FileDownloader:
    """文件下载工具"""
    
    @staticmethod
    def simple_download(url, save_path):
        """简单下载"""
        print(f"下载中: {url}")
        # 模拟下载
        print(f"已保存到: {save_path}")
    
    @staticmethod
    def stream_download(url, save_path, chunk_size=8192):
        """流式下载（适合大文件）"""
        print(f"流式下载: {url}")
        
        # 模拟流式响应
        total_size = 1000000  # 1MB
        downloaded = 0
        
        # 这是伪代码，实际使用 requests
        # with requests.get(url, stream=True) as r:
        #     with open(save_path, 'wb') as f:
        #         for chunk in r.iter_content(chunk_size=chunk_size):
        #             if chunk:
        #                 f.write(chunk)
        
        print(f"已保存到: {save_path}")
    
    @staticmethod
    def download_with_progress(url, save_path):
        """带进度条的下载"""
        print(f"下载: {url}")
        
        # 模拟下载进度
        for i in range(0, 101, 10):
            print(f"进度: {i}%")
        
        print(f"已保存到: {save_path}")

print("--- 下载方式对比 ---")
print("1. 简单下载：response.content（全部加载到内存）")
print("2. 流式下载：response.iter_content()（分块下载）")
print("3. 流式逐行：response.iter_lines()（适合文本文件）")

print("\n--- 实际下载示例 ---")
downloader = FileDownloader()
# downloader.simple_download('https://example.com/file.zip', 'file.zip')
# downloader.stream_download('https://example.com/large_file.iso', 'large_file.iso')

print("\n=== 3. 代理设置 ===\n")

print("--- 代理概念 ---")
print("""
代理用于：
  - 隐藏真实 IP
  - 绕过地理限制
  - 提高抓取效率

代理类型：
  HTTP 代理    - 用于 HTTP 请求
  HTTPS 代理   - 用于 HTTPS 请求
  SOCKS5 代理  - 更底层的代理协议
""")

print("\n--- 代理使用 ---")
print("""
import requests

# 单个代理
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}
response = requests.get('https://example.com', proxies=proxies)

# 带认证的代理
proxies = {
    'http': 'http://user:password@proxy.example.com:8080',
    'https': 'http://user:password@proxy.example.com:8080'
}

# SOCKS5 代理（需要 pip install pysocks）
proxies = {
    'http': 'socks5://proxy.example.com:1080',
    'https': 'socks5://proxy.example.com:1080'
}

# 多个代理轮换
proxies_list = [...]
for proxy in proxies_list:
    response = requests.get(url, proxies={'http': proxy, 'https': proxy})
""")

print("\n=== 4. 根据抓包复现请求 ===\n")

class PacketReplayHelper:
    """抓包复现助手"""
    
    @staticmethod
    def parse_curl(curl_command):
        """解析 curl 命令"""
        print("--- 从 curl 命令提取信息 ---")
        print(f"原 curl: {curl_command[:50]}...")
        
        # 解析示例
        import re
        
        # 提取 URL
        url_match = re.search(r"('([^']+)'|\"([^\"]+)\"|(\S+))", curl_command)
        
        # 提取 -H 头
        headers = {}
        header_matches = re.findall(r"-H '([^:]+): ([^']+)'", curl_command)
        for name, value in header_matches:
            headers[name] = value
        
        return {'headers': headers}
    
    @staticmethod
    def recreate_from_network_tab(request_info):
        """从浏览器开发者工具复现请求"""
        print("\n--- 从浏览器开发者工具复现 ---")
        
        # request_info 应包含：
        # {
        #     'url': 'https://api.example.com/data',
        #     'method': 'POST',
        #     'headers': {...},
        #     'body': {...}
        # }
        
        print(f"URL: {request_info.get('url')}")
        print(f"方法: {request_info.get('method')}")
        print(f"请求头数: {len(request_info.get('headers', {}))}")
        
        return request_info

print("--- 抓包复现流程 ---")
print("""
1. 开启浏览器开发者工具 (F12)
2. 切换到 Network 标签
3. 执行目标操作
4. 找到目标请求
5. 右键 -> Copy as cURL
6. 粘贴到代码中解析

或者直接从开发者工具中提取：
- URL
- 请求方法
- 请求头
- 请求体
- Cookie
""")

# 示例
curl_example = '''curl 'https://api.example.com/users' -X POST -H 'Authorization: Bearer token123' -H 'Content-Type: application/json' -d '{"name":"Alice"}' '''

print("\n--- 解析 curl 命令示例 ---")
# helper = PacketReplayHelper()
# helper.parse_curl(curl_example)

# 直接从网络信息创建请求
request_info = {
    'url': 'https://api.example.com/data',
    'method': 'POST',
    'headers': {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'Bearer token123',
        'Content-Type': 'application/json'
    },
    'body': {'action': 'get_data', 'user_id': '123'}
}

print("\n请求信息:")
for key, value in request_info.items():
    print(f"  {key}: {value}")

print("\n=== 5. 实用请求重建工具 ===\n")

class RequestReconstructor:
    """请求重建工具"""
    
    def __init__(self):
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
    
    def construct_get_request(self, url, params=None):
        """构造 GET 请求"""
        # 处理参数
        if params:
            import urllib.parse
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"
        
        return {
            'method': 'GET',
            'url': url,
            'headers': self.base_headers
        }
    
    def construct_post_request(self, url, data=None, json_data=None):
        """构造 POST 请求"""
        headers = self.base_headers.copy()
        
        if json_data:
            headers['Content-Type'] = 'application/json'
            body = json.dumps(json_data)
        elif data:
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
    
    def add_authorization(self, request, token):
        """添加认证令牌"""
        request['headers']['Authorization'] = f'Bearer {token}'
        return request

# 演示
print("--- 请求重建示例 ---")
reconstructor = RequestReconstructor()

# 构造 GET 请求
get_req = reconstructor.construct_get_request(
    'https://api.example.com/users',
    params={'page': 1, 'limit': 10}
)
print(f"GET 请求: {get_req['url']}")

# 构造 POST 请求
post_req = reconstructor.construct_post_request(
    'https://api.example.com/users',
    json_data={'name': 'Alice', 'email': 'alice@example.com'}
)
print(f"POST 请求: {post_req['url']}")
print(f"Body: {post_req['body']}")

# 添加认证
post_req = reconstructor.add_authorization(post_req, 'token_abc123')
print(f"带认证的请求头: Authorization = {post_req['headers']['Authorization']}")
