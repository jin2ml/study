# 第3月第1周学习代码示例
# 根据第3月第1周的学习内容（HTTP基础），这些示例覆盖了请求行、请求头、请求体、状态码、Query参数与Body、常见Content-Type。

print("=== 1. HTTP 请求结构 ===\n")

# HTTP 请求的基本组成部分
print("--- HTTP 请求结构示例 ---")
http_request = """
GET /api/users?page=1&limit=10 HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: application/json
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: session_id=abc123; user_id=456

"""
print(http_request)

print("=== 2. HTTP 请求行详解 ===\n")

print("--- 请求行结构 ---")
print("GET /api/users HTTP/1.1")
print("  GET: 请求方法")
print("  /api/users: 请求路径（URI）")
print("  HTTP/1.1: 协议版本")

print("\n--- 常见请求方法 ---")
methods = {
    'GET': '获取资源',
    'POST': '创建资源',
    'PUT': '整体替换资源',
    'PATCH': '部分更新资源',
    'DELETE': '删除资源',
    'HEAD': '获取响应头（不获取body）',
    'OPTIONS': '获取服务端支持的方法'
}

for method, description in methods.items():
    print(f"  {method:8}: {description}")

print("\n=== 3. HTTP 请求头详解 ===\n")

print("--- 常见请求头 ---")
headers = {
    'Host': '请求的主机名和端口',
    'User-Agent': '客户端信息（浏览器/爬虫）',
    'Accept': '客户端能接受的数据类型',
    'Accept-Encoding': '客户端能接受的压缩方式',
    'Accept-Language': '客户端能接受的语言',
    'Connection': '连接类型（keep-alive/close）',
    'Cookie': '客户端保存的Cookies',
    'Authorization': '身份认证信息',
    'Referer': '请求来源页面',
    'Content-Type': '请求体的数据类型',
    'Content-Length': '请求体的字节数'
}

for header, description in headers.items():
    print(f"  {header:20}: {description}")

print("\n--- 示例请求头 ---")
example_headers = {
    'Host': 'api.example.com',
    'User-Agent': 'Python-requests/2.28.0',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Authorization': 'Bearer token_abc123',
    'Content-Type': 'application/json'
}

for key, value in example_headers.items():
    print(f"  {key}: {value}")

print("\n=== 4. HTTP 请求体详解 ===\n")

print("--- 不同的 Content-Type ---")
content_types = {
    'application/json': '{"key": "value"}',
    'application/x-www-form-urlencoded': 'key1=value1&key2=value2',
    'multipart/form-data': '用于文件上传',
    'text/plain': '纯文本',
    'application/xml': '<root><key>value</key></root>'
}

for content_type, example in content_types.items():
    print(f"\n{content_type}:")
    print(f"  例: {example}")

print("\n--- 请求体示例 ---")
print("JSON 格式请求体:")
print("""{
  "username": "alice",
  "password": "secret123",
  "email": "alice@example.com"
}""")

print("\nForm 格式请求体:")
print("username=alice&password=secret123&email=alice@example.com")

print("\n=== 5. HTTP 状态码详解 ===\n")

print("--- 状态码分类 ---")
status_code_ranges = {
    '1xx': '信息性状态码',
    '2xx': '成功状态码',
    '3xx': '重定向状态码',
    '4xx': '客户端错误状态码',
    '5xx': '服务器错误状态码'
}

for code_range, description in status_code_ranges.items():
    print(f"  {code_range}: {description}")

print("\n--- 常见状态码 ---")
status_codes = {
    200: 'OK - 请求成功',
    201: 'Created - 资源已创建',
    204: 'No Content - 成功但无返回内容',
    302: 'Found - 临时重定向',
    304: 'Not Modified - 资源未修改',
    400: 'Bad Request - 请求参数错误',
    401: 'Unauthorized - 需要认证',
    403: 'Forbidden - 禁止访问',
    404: 'Not Found - 资源不存在',
    429: 'Too Many Requests - 请求过频繁',
    500: 'Internal Server Error - 服务器错误',
    503: 'Service Unavailable - 服务不可用'
}

for code, description in status_codes.items():
    print(f"  {code}: {description}")

print("\n=== 6. URL 和 Query 参数 ===\n")

print("--- URL 结构 ---")
url = "https://api.example.com:8080/api/users/123?page=1&limit=10#section1"
print(f"完整 URL: {url}")
print("""
https://              -> 协议
api.example.com       -> 域名
:8080                 -> 端口
/api/users/123        -> 路径/资源
?page=1&limit=10      -> Query 参数
#section1             -> 锚点/片段
""")

print("--- Query 参数处理 ---")
import urllib.parse

params = {
    'page': '1',
    'limit': '10',
    'search': 'python',
    'sort': 'date_desc'
}

query_string = urllib.parse.urlencode(params)
print(f"参数字典: {params}")
print(f"Query 字符串: {query_string}")
print(f"完整 URL: https://api.example.com/search?{query_string}")

# 解析 Query 字符串
parsed_params = urllib.parse.parse_qs(query_string)
print(f"解析后: {parsed_params}")

print("\n=== 7. HTTP 请求响应周期 ===\n")

print("--- 完整的 HTTP 请求/响应流程 ---")
print("""
1. 客户端建立连接
   - DNS 查询（域名 -> IP）
   - TCP 连接（三次握手）
   - TLS 握手（HTTPS）

2. 客户端发送请求
   - 请求行
   - 请求头
   - 空行
   - 请求体（可选）

3. 服务器处理请求
   - 解析请求
   - 执行业务逻辑
   - 准备响应

4. 服务器发送响应
   - 状态行
   - 响应头
   - 空行
   - 响应体

5. 关闭连接
   - TCP 四次挥手（或保持连接）
""")

print("\n=== 8. 常见的 HTTP 场景 ===\n")

print("--- 场景1：GET 请求 ---")
print("""
请求：
GET /api/users/123 HTTP/1.1
Host: api.example.com

说明：获取 ID 为 123 的用户信息
""")

print("--- 场景2：POST 请求（JSON） ---")
print("""
请求：
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 47

{"name":"Alice","email":"alice@example.com"}

说明：创建新用户
""")

print("--- 场景3：POST 请求（Form） ---")
print("""
请求：
POST /login HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

username=alice&password=secret123

说明：表单提交登录
""")

print("--- 场景4：带 Cookie 和 Authorization ---")
print("""
请求：
GET /api/profile HTTP/1.1
Host: api.example.com
Cookie: session_id=abc123; user_id=456
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

说明：需要身份认证的请求
""")

print("\n=== 9. 实用参考表 ===\n")

print("--- HTTP 方法选择 ---")
print("""
GET     -> 查询数据（幂等）
POST    -> 创建数据（非幂等）
PUT     -> 完全替换（幂等）
PATCH   -> 部分更新（可幂等）
DELETE  -> 删除数据（幂等）
""")

print("--- Content-Type 速查 ---")
print("""
application/json           -> JSON 格式
application/x-www-form-urlencoded -> 表单数据
multipart/form-data        -> 表单 + 文件上传
application/xml            -> XML 格式
text/plain                 -> 纯文本
text/html                  -> HTML 页面
image/jpeg, image/png      -> 图片
""")

print("--- 状态码快速判断 ---")
print("""
2xx -> 成功，继续处理
3xx -> 重定向，跟随 Location 头
4xx -> 客户端错误，检查请求
5xx -> 服务器错误，稍后重试
""")
