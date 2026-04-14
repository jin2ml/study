# 第2月第3周学习代码示例  
# 根据第2月第3周的学习内容（哈希与HMAC），这些示例覆盖了md5、sha1、sha256、hmac、时间戳和签名拼接。

import hashlib
import hmac
import time
import json
from datetime import datetime

print("=== 1. 哈希函数基础 ===\n")

# MD5
print("--- MD5 ---")
text = "Hello, World!"
md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
print(f"文本: {text}")
print(f"MD5: {md5_hash}")
print(f"长度: {len(md5_hash)}")

# 处理字节
text_bytes = b"Binary Data"
md5_bytes = hashlib.md5(text_bytes).hexdigest()
print(f"字节: {text_bytes}")
print(f"MD5: {md5_bytes}")

# SHA 家族
print("\n--- SHA 系列 ---")
text = "Python Hashing"

sha1 = hashlib.sha1(text.encode('utf-8')).hexdigest()
sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()
sha512 = hashlib.sha512(text.encode('utf-8')).hexdigest()

print(f"文本: {text}")
print(f"SHA1   ({len(sha1)} chars): {sha1}")
print(f"SHA256 ({len(sha256)} chars): {sha256}")
print(f"SHA512 ({len(sha512)} chars): {sha512}")

# 相同内容哈希值相同
print("\n--- 哈希值确定性 ---")
text1 = "Same Content"
text2 = "Same Content"
text3 = "Different Content"

hash1 = hashlib.md5(text1.encode()).hexdigest()
hash2 = hashlib.md5(text2.encode()).hexdigest()
hash3 = hashlib.md5(text3.encode()).hexdigest()

print(f"'{text1}' MD5: {hash1}")
print(f"'{text2}' MD5: {hash2}")
print(f"相同吗？{hash1 == hash2}")
print(f"'{text3}' MD5: {hash3}")
print(f"与第一个相同吗？{hash1 == hash3}")

# 长输入哈希
print("\n--- 处理长输入 ---")
large_data = "X" * 10000
hash_large = hashlib.sha256(large_data.encode()).hexdigest()
print(f"输入大小: {len(large_data)} 字符")
print(f"SHA256: {hash_large}")

print("\n=== 2. HMAC 消息认证码 ===\n")

# 基础 HMAC
print("--- HMAC 基础 ---")
secret_key = "my_secret_key"
message = "Important Message"

hmac_md5 = hmac.new(
    secret_key.encode('utf-8'),
    message.encode('utf-8'),
    hashlib.md5
).hexdigest()

hmac_sha256 = hmac.new(
    secret_key.encode('utf-8'),
    message.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print(f"密钥: {secret_key}")
print(f"消息: {message}")
print(f"HMAC-MD5: {hmac_md5}")
print(f"HMAC-SHA256: {hmac_sha256}")

# HMAC 验证
print("\n--- HMAC 验证 ---")
received_hmac = hmac_sha256
calculated_hmac = hmac.new(
    secret_key.encode('utf-8'),
    message.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print(f"接收到的 HMAC: {received_hmac}")
print(f"计算的 HMAC: {calculated_hmac}")
print(f"验证通过: {received_hmac == calculated_hmac}")

# 密钥修改后验证失败
wrong_key = "wrong_key"
wrong_hmac = hmac.new(
    wrong_key.encode('utf-8'),
    message.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print(f"错误密钥的 HMAC: {wrong_hmac}")
print(f"与原始匹配: {wrong_hmac == calculated_hmac}")

# 安全比较
print("\n--- 安全比较 HMAC ---")
# 使用 hmac.compare_digest() 防止时序攻击
if hmac.compare_digest(calculated_hmac, received_hmac):
    print("HMAC 验证成功（安全比较）")
else:
    print("HMAC 验证失败")

print("\n=== 3. 时间戳与签名 ===\n")

# 时间戳签名
print("--- 基础时间戳签名 ---")
timestamp = int(time.time())
secret = "app_secret"
data = "user_data"

# 构造签名字符串
sign_str = f"{data}_{timestamp}"
signature = hashlib.md5(sign_str.encode()).hexdigest()

print(f"数据: {data}")
print(f"时间戳: {timestamp}")
print(f"签名字符串: {sign_str}")
print(f"签名: {signature}")

# 验证签名
print("\n--- 签名验证 ---")
received_timestamp = timestamp
received_signature = signature

# 验证时间戳不超过5分钟
current_time = int(time.time())
time_diff = current_time - received_timestamp
max_age = 5 * 60  # 5 分钟

if time_diff <= max_age:
    print(f"时间戳有效，差异: {time_diff} 秒")
    
    # 重新计算签名
    recalc_sign = hashlib.md5(f"{data}_{received_timestamp}".encode()).hexdigest()
    if hmac.compare_digest(received_signature, recalc_sign):
        print("签名验证成功")
    else:
        print("签名验证失败")
else:
    print(f"时间戳过期，差异: {time_diff} 秒，最大允许: {max_age} 秒")

# API 签名示例
print("\n--- API 签名示例 ---")
api_key = "test_api_key"
api_secret = "test_api_secret"
timestamp = int(time.time() * 1000)  # 毫秒时间戳

params = {
    'user_id': '12345',
    'action': 'get_profile',
    'timestamp': timestamp
}

# 排序参数
sorted_params = sorted(params.items())
param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])

# 生成签名
sign_base = f"{param_str}&secret={api_secret}"
api_sign = hashlib.sha256(sign_base.encode()).hexdigest()

print(f"参数: {params}")
print(f"排序参数: {param_str}")
print(f"签名基串: {sign_base}")
print(f"API签名: {api_sign}")

print("\n=== 4. JSON 签名 ===\n")

# JSON 数据签名
print("--- JSON 签名 ---")
user_data = {
    'id': '12345',
    'name': 'Alice',
    'email': 'alice@example.com'
}

json_str = json.dumps(user_data, sort_keys=True, separators=(',', ':'))
print(f"JSON: {json_str}")

signature = hashlib.sha256(json_str.encode()).hexdigest()
print(f"签名: {signature}")

# 验证 JSON 签名
modified_data = {
    'id': '12345',
    'name': 'Alice',
    'email': 'alice@modified.com'  # 修改了邮箱
}

modified_json = json.dumps(modified_data, sort_keys=True, separators=(',', ':'))
modified_sig = hashlib.sha256(modified_json.encode()).hexdigest()

print(f"\n修改后的 JSON: {modified_json}")
print(f"修改后的签名: {modified_sig}")
print(f"签名匹配: {signature == modified_sig}")

print("\n=== 5. 实用签名工具 ===\n")

class SignatureHelper:
    """签名辅助工具"""
    
    @staticmethod
    def md5(text):
        """MD5 哈希"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha256(text):
        """SHA256 哈希"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def hmac_sha256(message, secret):
        """HMAC-SHA256"""
        return hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def sign_params(params, secret, algorithm='sha256'):
        """对参数字典签名"""
        # 排序参数
        sorted_items = sorted(params.items())
        param_str = '&'.join([f"{k}={v}" for k, v in sorted_items])
        
        # 添加密钥
        sign_str = f"{param_str}&secret={secret}"
        
        # 生成签名
        if algorithm == 'md5':
            signature = hashlib.md5(sign_str.encode()).hexdigest()
        elif algorithm == 'sha256':
            signature = hashlib.sha256(sign_str.encode()).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        return signature
    
    @staticmethod
    def verify_sign(params, received_sign, secret, algorithm='sha256'):
        """验证签名"""
        calculated_sign = SignatureHelper.sign_params(params, secret, algorithm)
        return hmac.compare_digest(calculated_sign, received_sign)

# 测试工具
helper = SignatureHelper()

params = {
    'action': 'login',
    'username': 'alice',
    'timestamp': int(time.time())
}

secret = 'my_secret'
signature = helper.sign_params(params, secret)

print(f"参数: {params}")
print(f"签名: {signature}")
print(f"验证: {helper.verify_sign(params, signature, secret)}")

print("\n=== 6. 加盐哈希 ===\n")

# 密码加盐哈希
print("--- 密码加盐 ---")
password = "MyPassword123"
salt = "random_salt_value"

# 不加盐
simple_hash = hashlib.sha256(password.encode()).hexdigest()
print(f"密码: {password}")
print(f"简单哈希: {simple_hash}")

# 加盐
salted_hash = hashlib.sha256((salt + password).hexdigest().encode()).hexdigest()
print(f"盐值: {salt}")
print(f"加盐哈希: {salted_hash}")

# 验证加盐密码
def verify_password(password, salt, stored_hash):
    """验证加盐密码"""
    calculated = hashlib.sha256((salt + password).hexdigest().encode()).hexdigest()
    return hmac.compare_digest(calculated, stored_hash)

print(f"验证正确密码: {verify_password(password, salt, salted_hash)}")
print(f"验证错误密码: {verify_password('WrongPassword', salt, salted_hash)}")
