# 第3月第3周学习代码示例
# 根据第3月第3周的学习内容（登录态与会话），这些示例覆盖了Cookie、Session、Token、重定向、超时、重试。

import time
import json
from urllib.parse import urljoin

print("=== 1. Cookie 基础 ===\n")

print("--- Cookie 概念 ---")
print("""
Cookie 用于在 HTTP 请求中保存客户端状态
- 由服务器通过 Set-Cookie 头发送给客户端
- 客户端在后续请求中通过 Cookie 头发送回服务器
- 用于：用户登录、用户偏好、跟踪等

Cookie 属性：
  Name=Value          # Cookie 内容
  Domain              # Cookie 有效的域名
  Path                # Cookie 有效的路径
  Expires/Max-Age     # Cookie 过期时间
  Secure              # 仅在 HTTPS 发送
  HttpOnly            # JavaScript 无法访问
  SameSite            # 跨域请求限制
""")

print("--- Cookie 使用示例 ---")
print("""
import requests

# 自动保存 Cookie
session = requests.Session()

# 第一次请求（会保存服务器下发的 Cookie）
response1 = session.get('https://example.com/login')

# 第二次请求（自动发送保存的 Cookie）
response2 = session.get('https://example.com/dashboard')

# 手动设置 Cookie
cookies = {'session_id': 'abc123', 'user_id': '456'}
response = requests.get('https://example.com/profile', cookies=cookies)

# 获取所有 Cookie
print(session.cookies)
print(dict(session.cookies))
""")

print("\n=== 2. Session 会话管理 ===\n")

class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        self.cookies = {}
        self.headers = {}
        self.base_url = ''
    
    def login(self, username, password):
        """登录"""
        print(f"正在以 {username} 名义登录...")
        
        # 模拟登录请求
        self.cookies['session_id'] = f"sess_{hash(username)}"
        self.cookies['user_id'] = '123'
        self.headers['Authorization'] = f'Bearer token_{hash(password)}'
        
        return True
    
    def logout(self):
        """登出"""
        print("正在登出...")
        self.cookies.clear()
        self.headers.clear()
    
    def is_authenticated(self):
        """检查是否已认证"""
        return 'session_id' in self.cookies
    
    def get_headers(self):
        """获取当前headers"""
        return self.headers.copy()
    
    def get_cookies(self):
        """获取当前cookies"""
        return self.cookies.copy()

print("--- Session 使用示例 ---")
session_mgr = SessionManager()
print(f"认证状态: {session_mgr.is_authenticated()}")

session_mgr.login('alice', 'password123')
print(f"认证状态: {session_mgr.is_authenticated()}")
print(f"Cookies: {session_mgr.get_cookies()}")
print(f"Headers: {session_mgr.get_headers()}")

session_mgr.logout()
print(f"认证状态: {session_mgr.is_authenticated()}")

print("\n=== 3. Token 认证 ===\n")

print("--- Token 认证模式 ---")
print("""
1. 获取 Token：POST /auth/token -> 返回 token
2. 存储 Token：保存在本地
3. 使用 Token：在 Authorization 头中附带
   Authorization: Bearer <token>
4. Token 刷新：如果 Token 过期，用 refresh_token 获取新的

常见 Token 类型：
  Bearer Token    # 最常见，后跟具体 token 值
  Basic Auth      # 用户名:密码 Base64 编码
  API Key         # 简单的 API 密钥
""")

class TokenAuthClient:
    """Token 认证客户端"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.token_type = 'Bearer'
        self.expires_at = None
    
    def login(self, username, password):
        """登录获取 Token"""
        # 模拟登录请求
        response = {
            'access_token': f'token_{hash(username)}',
            'token_type': 'Bearer',
            'expires_in': 3600
        }
        
        self.token = response['access_token']
        self.token_type = response['token_type']
        self.expires_at = time.time() + response['expires_in']
        
        return self.token
    
    def get_auth_header(self):
        """获取认证头"""
        if not self.token:
            return None
        return {'Authorization': f'{self.token_type} {self.token}'}
    
    def is_token_expired(self):
        """检查 Token 是否过期"""
        if not self.expires_at:
            return True
        return time.time() > self.expires_at

print("--- Token 使用示例 ---")
client = TokenAuthClient('https://api.example.com')
token = client.login('alice', 'password123')
print(f"获得 Token: {token[:10]}...")
print(f"Auth Header: {client.get_auth_header()}")
print(f"Token 过期状态: {client.is_token_expired()}")

print("\n=== 4. 重定向处理 ===\n")

print("--- HTTP 重定向 ---")
print("""
重定向状态码：
  301 (Moved Permanently)   # 永久重定向，更改请求方法为 GET
  302 (Found)               # 临时重定向，通常保持原请求方法
  303 (See Other)           # 重定向到不同资源，改为 GET
  307 (Temporary Redirect)  # 保持原请求方法的临时重定向
  308 (Permanent Redirect)  # 保持原请求方法的永久重定向

Location 头包含重定向目标 URL
""")

print("--- 重定向处理示例 ---")
print("""
import requests

# requests 默认自动跟随重定向（最多30次）
response = requests.get('https://example.com/old-page')

# 禁用自动重定向
response = requests.get('https://example.com/old-page', allow_redirects=False)
if response.status_code in (301, 302, 303, 307, 308):
    location = response.headers['Location']
    print(f"重定向到: {location}")

# 检查重定向历史
response = requests.get('https://example.com/old-page')
for resp in response.history:
    print(f"{resp.status_code} -> {resp.url}")
print(f"最终 URL: {response.url}")
""")

print("\n=== 5. 超时和重试 ===\n")

class RobustHTTPClient:
    """健壮的 HTTP 客户端（支持超时和重试）"""
    
    def __init__(self, timeout=5, max_retries=3, backoff_factor=0.5):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def request_with_retry(self, method, url, **kwargs):
        """带重试的请求"""
        retries = 0
        last_error = None
        
        while retries < self.max_retries:
            try:
                print(f"尝试请求 {retries + 1}/{self.max_retries}: {method} {url}")
                
                # 设置超时和其他参数
                kwargs['timeout'] = kwargs.get('timeout', self.timeout)
                
                # 模拟请求
                if retries == 0:
                    status_code = 200
                elif retries == 1:
                    status_code = 500  # 第一次重试失败
                else:
                    status_code = 200  # 第二次重试成功
                
                if status_code == 200:
                    return {'status_code': 200, 'data': 'Success'}
                elif status_code >= 500:
                    raise Exception(f"Server error: {status_code}")
                
            except Exception as e:
                last_error = e
                retries += 1
                if retries < self.max_retries:
                    wait_time = self.backoff_factor ** (retries - 1)
                    print(f"  请求失败，{wait_time:.1f}秒后重试...")
                    time.sleep(wait_time)
        
        raise Exception(f"请求失败，已重试 {self.max_retries} 次。最后错误: {last_error}")

print("--- 超时和重试示例 ---")
client = RobustHTTPClient(timeout=5, max_retries=3)
try:
    result = client.request_with_retry('GET', 'https://api.example.com/data')
    print(f"请求成功: {result}")
except Exception as e:
    print(f"最终失败: {e}")

print("\n=== 6. 完整的登录流程示例 ===\n")

class FullLoginExample:
    """完整的登录流程示例"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = {
            'cookies': {},
            'token': None,
            'user_data': None
        }
    
    def login(self, username, password):
        """完整登录流程"""
        print(f"[1] 发送登录请求")
        login_data = {'username': username, 'password': password}
        print(f"    POST {self.base_url}/login")
        
        # 模拟登录响应
        self.session['cookies']['session_id'] = f"sess_{hash(username)}"
        self.session['token'] = f"token_{hash(password)}"
        self.session['user_data'] = {
            'id': '123',
            'username': username,
            'email': f'{username}@example.com'
        }
        
        print(f"[2] 保存 Cookie: {self.session['cookies']}")
        print(f"[3] 保存 Token: {self.session['token'][:20]}...")
        print(f"[4] 保存用户数据: {self.session['user_data']}")
        
        return True
    
    def make_authenticated_request(self, path):
        """发送需要认证的请求"""
        headers = {
            'Authorization': f'Bearer {self.session["token"]}'
        }
        cookies = self.session['cookies']
        
        print(f"\n发送认证请求:")
        print(f"  URL: {self.base_url}{path}")
        print(f"  Headers: {headers}")
        print(f"  Cookies: {cookies}")
        
        return {'status': 200, 'data': 'Protected resource'}
    
    def logout(self):
        """登出"""
        self.session = {
            'cookies': {},
            'token': None,
            'user_data': None
        }
        print("已登出，清除所有认证信息")

# 演示完整流程
print("--- 完整登录流程 ---")
example = FullLoginExample('https://api.example.com')
example.login('alice', 'password123')
result = example.make_authenticated_request('/profile')
print(f"  响应: {result}")
example.logout()
