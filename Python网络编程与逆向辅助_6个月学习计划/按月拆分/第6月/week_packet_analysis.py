# 第6月学习代码示例（抓包分析、参数验证、综合实战）
# 抓包分析、动态参数识别、签名验证、完整案例复盘

import json
import re
import hashlib
import time
from typing import Dict, List, Any

print("=== 1. 抓包文件解析 ===\n")

print("--- HTTP Archive (HAR) 格式 ---")
print("""
HAR 格式用于记录浏览器的网络活动：
  - JSON 格式
  - 包含请求和响应的完整信息
  - 可以从浏览器开发者工具导出

结构示例：
{
  "log": {
    "version": "1.2",
    "creator": {...},
    "entries": [
      {
        "request": { "method": "POST", "url": "...", "headers": [...], "postData": {...} },
        "response": { "status": 200, "headers": [...], "content": {...} }
      }
    ]
  }
}
""")

class HARParser:
    """HAR 文件解析器"""
    
    @staticmethod
    def load_har(filename):
        """加载 HAR 文件"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def extract_requests(har_data):
        """提取所有请求"""
        requests = []
        for entry in har_data['log']['entries']:
            req = entry['request']
            requests.append({
                'method': req['method'],
                'url': req['url'],
                'headers': {h['name']: h['value'] for h in req.get('headers', [])},
                'body': req.get('postData', {}).get('text', '')
            })
        return requests
    
    @staticmethod
    def analyze_request(req):
        """分析单个请求"""
        print(f"方法: {req['method']}")
        print(f"URL: {req['url']}")
        print(f"请求头:")
        for k, v in req['headers'].items():
            if k.lower() not in ['authorization', 'cookie', 'x-token']:
                print(f"  {k}: {v}")
        if req['body']:
            print(f"请求体: {req['body'][:200]}...")

print("\n--- 抓包分析流程---")
print("""
1. 打开浏览器开发者工具 (F12)
2. 切换到 Network 标签
3. 执行目标操作（登录、搜索等）
4. 右键导出为 HAR 格式
5. 使用脚本解析和分析
""")

print("\n=== 2. 动态参数识别 ===\n")

class DynamicParameterAnalyzer:
    """动态参数分析器"""
    
    @staticmethod
    def identify_dynamic_fields(requests: List[Dict]) -> Dict[str, List[str]]:
        """识别动态字段"""
        # 按 URL 分组请求
        url_groups = {}
        for req in requests:
            url = req['url'].split('?')[0]  # 去掉查询参数
            if url not in url_groups:
                url_groups[url] = []
            url_groups[url].append(req)
        
        dynamic_fields = {}
        
        for url, reqs in url_groups.items():
            if len(reqs) < 2:
                continue
            
            # 比较请求体
            if all(req['body'] for req in reqs):
                try:
                    bodies = [json.loads(req['body']) if isinstance(req['body'], str) else req['body'] for req in reqs]
                    
                    # 找变化的字段
                    all_keys = set()
                    for body in bodies:
                        if isinstance(body, dict):
                            all_keys.update(body.keys())
                    
                    dynamic = []
                    for key in all_keys:
                        values = set()
                        for body in bodies:
                            if isinstance(body, dict) and key in body:
                                values.add(str(body[key]))
                        
                        if len(values) > 1:  # 字段值变化
                            dynamic.append(key)
                    
                    if dynamic:
                        dynamic_fields[url] = dynamic
                except:
                    pass
        
        return dynamic_fields

print("--- 动态参数识别的关键字段 ---")
print("""
常见的动态参数：
  1. 时间戳
     特征：Unix 时间戳（10-13 位数字）
     示例：1609459200, 1609459200000
  
  2. 随机数/UUID
     特征：十六进制或 UUID 格式
     示例：a1b2c3d4e5f6, 550e8400-e29b-41d4-a716-446655440000
  
  3. nonce（一次性数字）
     特征：随机字符串
     示例：abc123xyz789
  
  4. session/token
     特征：长随机字符串
     示例：sess_abc123..., jwt_token...
  
  5. 签名字段
     特征：哈希值（MD5/SHA1/SHA256）
     示例：5d41402abc4b2a76b9719d911017c592
""")

print("\n=== 3. 签名验证 ===\n")

class SignatureVerifier:
    """签名验证器"""
    
    @staticmethod
    def guess_hash_type(hash_str):
        """根据长度猜测哈希类型"""
        length = len(hash_str)
        if length == 32:
            return 'MD5'
        elif length == 40:
            return 'SHA1'
        elif length == 64:
            return 'SHA256'
        elif length == 128:
            return 'SHA512'
        else:
            return 'Unknown'
    
    @staticmethod
    def try_common_signatures(data, hash_value):
        """尝试常见的签名方式"""
        signatures = {}
        
        # MD5
        signatures['MD5(data)'] = hashlib.md5(data.encode()).hexdigest()
        
        # SHA256
        signatures['SHA256(data)'] = hashlib.sha256(data.encode()).hexdigest()
        
        # 带密钥的签名（常用密钥）
        import hmac
        for key in ['', 'secret', 'key', 'appkey', 'api_secret']:
            signatures[f'HMAC-SHA256(data, "{key}")'] = hmac.new(
                key.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
        
        # 找匹配的
        matches = []
        for method, sig in signatures.items():
            if sig == hash_value:
                matches.append(method)
        
        return matches

print("--- 签名验证示例 ---")
print("""
1. 观察多个请求，找出签名字段
2. 比较签名值和其他参数的关系
3. 使用 SignatureVerifier 尝试常见算法
4. 一旦找到规律，即可复现
""")

print("\n=== 4. 参数排序与签名生成 ===\n")

class SignatureBuilder:
    """签名生成器"""
    
    @staticmethod
    def build_signature_string(params, sort=True, include_values=True):
        """构建签名字符串"""
        if sort:
            items = sorted(params.items())
        else:
            items = list(params.items())
        
        if include_values:
            signature_str = '&'.join([f'{k}={v}' for k, v in items])
        else:
            signature_str = '&'.join([k for k, v in items])
        
        return signature_str
    
    @staticmethod
    def generate_signature(params, secret='', algorithm='sha256', append_secret=True):
        """生成签名"""
        # 参数排序
        sign_str = SignatureBuilder.build_signature_string(params, sort=True)
        
        # 是否追加密钥
        if append_secret and secret:
            sign_str += f'&secret={secret}'
        elif secret:
            sign_str = f'{secret}{sign_str}'
        
        # 计算哈希
        if algorithm == 'md5':
            return hashlib.md5(sign_str.encode()).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(sign_str.encode()).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(sign_str.encode()).hexdigest()

print("--- 签名生成示例 ---")
params = {'action': 'login', 'username': 'alice', 'timestamp': int(time.time())}
secret = 'my_secret'

sig_str = SignatureBuilder.build_signature_string(params)
signature = SignatureBuilder.generate_signature(params, secret)

print(f"参数: {params}")
print(f"签名字符串: {sig_str}")
print(f"签名（SHA256）: {signature}")

print("\n=== 5. 响应解析与验证 ===\n")

class ResponseAnalyzer:
    """响应分析器"""
    
    @staticmethod
    def parse_response(response_text):
        """解析响应"""
        try:
            return json.loads(response_text)
        except:
            return {'raw': response_text}
    
    @staticmethod
    def verify_response_structure(response, expected_fields):
        """验证响应结构"""
        if not isinstance(response, dict):
            return False, "响应不是 JSON 对象"
        
        missing = [f for f in expected_fields if f not in response]
        if missing:
            return False, f"缺少字段: {missing}"
        
        return True, "响应结构正确"
    
    @staticmethod
    def extract_sensitive_data(response, patterns):
        """提取敏感数据"""
        result = {}
        
        for name, pattern in patterns.items():
            for key, value in response.items():
                if re.search(pattern, str(key)):
                    result[name] = value
                    break
        
        return result

print("--- 响应分析示例 ---")
response = {
    'code': 0,
    'msg': 'success',
    'data': {'user_id': '12345', 'token': 'abc123xyz789'},
    'timestamp': int(time.time())
}

valid, msg = ResponseAnalyzer.verify_response_structure(
    response,
    ['code', 'msg', 'data']
)
print(f"结构验证: {valid} - {msg}")

# 提取敏感数据
sensitive = ResponseAnalyzer.extract_sensitive_data(
    response,
    {'token': r'token', 'user_id': r'user_id|uid'}
)
print(f"敏感数据: {sensitive}")

print("\n=== 6. 完整分析案例模板 ===\n")

class CaseAnalysisTemplate:
    """案例分析模板"""
    
    def __init__(self, api_endpoint):
        self.endpoint = api_endpoint
        self.requests = []
        self.analysis = {}
    
    def add_request(self, request):
        """添加请求"""
        self.requests.append(request)
    
    def analyze_pattern(self):
        """分析请求模式"""
        # 1. URL 分析
        urls = [r['url'] for r in self.requests]
        print("=== URL 分析 ===")
        print(f"唯一 URL 数: {len(set(urls))}")
        
        # 2. 请求头分析
        print("\n=== 请求头分析 ===")
        all_headers = {}
        for req in self.requests:
            all_headers.update(req['headers'])
        
        print(f"出现的请求头: {list(all_headers.keys())[:5]}...")
        
        # 3. 请求体分析
        print("\n=== 请求体分析 ===")
        if self.requests[0]['body']:
            body = json.loads(self.requests[0]['body'])
            print(f"请求体字段: {list(body.keys())}")
            
            # 识别动态字段
            analyzer = DynamicParameterAnalyzer()
            dynamic = analyzer.identify_dynamic_fields(self.requests)
            if dynamic:
                print(f"动态字段: {dynamic}")
    
    def generate_report(self):
        """生成分析报告"""
        print("\n" + "="*60)
        print(f"分析报告: {self.endpoint}")
        print("="*60)
        
        self.analyze_pattern()
        
        print("\n" + "="*60)
        print("建议的复现流程：")
        print("""
1. 获取必要的静态参数（URL、请求头等）
2. 识别并计算动态参数
3. 构建请求签名（如果需要）
4. 发送请求并处理响应
5. 验证响应数据完整性
        """)

print("--- 案例分析模板使用 ---")
case = CaseAnalysisTemplate('https://api.example.com/login')
# 添加请求并分析（需要真实数据）

print("\n=== 7. 最佳实践总结 ===\n")

print("""
抓包分析的完整步骤：

1. 数据收集
   ✓ 打开开发者工具
   ✓ 清除网络日志
   ✓ 执行目标操作
   ✓ 导出 HAR 文件

2. 请求分析
   ✓ 识别关键请求
   ✓ 查看请求头和请求体
   ✓ 对比多个相同请求

3. 参数识别
   ✓ 找出动态参数
   ✓ 分类：时间戳、随机数、签名等
   ✓ 记录参数变化规律

4. 签名验证
   ✓ 识别签名字段
   ✓ 尝试常见算法
   ✓ 验证排序规则

5. 代码复现
   ✓ 编写请求构造函数
   ✓ 实现签名计算
   ✓ 处理异常和重试

6. 测试验证
   ✓ 对比浏览器请求
   ✓ 验证响应数据
   ✓ 调整参数获得正确结果

关键工具：
  - 浏览器开发者工具
  - Fiddler / Burp Suite
  - 抓包分析脚本
  - hashlib / hmac 库
  - requests 库
""")
