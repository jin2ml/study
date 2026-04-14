# 第2月第2周学习代码示例
# 根据第2月第2周的学习内容（编码与字节处理），这些示例覆盖了Base64、Hex、URL编码、bytes/str转换。

import base64
import binascii
import urllib.parse
import codecs

print("=== 1. Base64 编码解码 ===\n")

# Base64 基础
print("--- Base64 编码 ---")
text = "Hello, Python! 你好，世界！"
print(f"原文本: {text}")
print(f"类型: {type(text)}")

# 字符串 -> 字节 -> Base64
text_bytes = text.encode('utf-8')
print(f"字节: {text_bytes}")

encoded = base64.b64encode(text_bytes)
print(f"Base64 编码: {encoded}")
print(f"Base64 字符串: {encoded.decode('utf-8')}")

# Base64 解码
print("\n--- Base64 解码 ---")
encoded_str = "SGVsbG8sIFB5dGhvbiEg5L2g5aW9LOS4gOeCjSDkuJzhkIjvvI8="
decoded_bytes = base64.b64decode(encoded_str)
decoded_text = decoded_bytes.decode('utf-8')
print(f"Base64 字符串: {encoded_str}")
print(f"解码后字节: {decoded_bytes}")
print(f"解码后文本: {decoded_text}")

# 处理 Base64 错误
print("\n--- Base64 错误处理 ---")
invalid_base64 = "Invalid!!Base64"
try:
    base64.b64decode(invalid_base64)
except binascii.Error as e:
    print(f"解码错误: {e}")

# URL 安全的 Base64
print("\n--- URL 安全的 Base64 ---")
data = b"Hello+World/Test="
safe_encoded = base64.urlsafe_b64encode(data)
print(f"标准 Base64: {base64.b64encode(data)}")
print(f"URL 安全: {safe_encoded}")

safe_decoded = base64.urlsafe_b64decode(safe_encoded)
print(f"URL 安全解码: {safe_decoded}")

print("\n=== 2. Hex 编码解码 ===\n")

# Hex 基础
print("--- Hex 编码 ---")
text = "Hello, World!"
text_bytes = text.encode('utf-8')
print(f"原文本: {text}")
print(f"字节: {text_bytes}")

hex_encoded = binascii.hexlify(text_bytes)
print(f"Hex 编码: {hex_encoded}")
print(f"Hex 字符串: {hex_encoded.decode('utf-8')}")

# 使用 bytes.hex()
hex_direct = text_bytes.hex()
print(f"直接 hex(): {hex_direct}")

# Hex 解码
print("\n--- Hex 解码 ---")
hex_str = "48656c6c6f2c20576f726c6421"
decoded_bytes = binascii.unhexlify(hex_str)
decoded_text = decoded_bytes.decode('utf-8')
print(f"Hex 字符串: {hex_str}")
print(f"解码后: {decoded_text}")

# 使用 bytes.fromhex()
decoded_direct = bytes.fromhex(hex_str)
print(f"直接 fromhex(): {decoded_direct}")

# 二进制数据的 Hex 表现
print("\n--- 二进制数据 Hex 表示 ---")
binary_data = b'\x00\x01\x02\x03\xff\xfe\xfd'
hex_repr = binary_data.hex()
print(f"二进制: {binary_data}")
print(f"Hex: {hex_repr}")
reconstructed = bytes.fromhex(hex_repr)
print(f"重建: {reconstructed}")

print("\n=== 3. URL 编码解码 ===\n")

# URL 编码
print("--- URL 编码 ---")
text = "Hello World! 你好？page=1&name=Alice"
print(f"原文本: {text}")

# quote() - 编码特定字符
encoded = urllib.parse.quote(text)
print(f"quote(): {encoded}")

# quote_plus() - 将空格编码为 +
encoded_plus = urllib.parse.quote_plus(text)
print(f"quote_plus(): {encoded_plus}")

# URL 解码
print("\n--- URL 解码 ---")
url_encoded = "Hello%20World%21%20%E4%BD%A0%E5%A5%BD%EF%BC%9F"
decoded = urllib.parse.unquote(url_encoded)
print(f"URL 编码: {url_encoded}")
print(f"解码: {decoded}")

decoded_plus = urllib.parse.unquote_plus("Hello+World%21")
print(f"unquote_plus(): {decoded_plus}")

# 查询字符串编码
print("\n--- 查询字符串编码 ---")
params = {
    'name': 'Alice',
    'age': '25',
    'city': '北京',
    'skills': 'Python,JavaScript'
}
query_string = urllib.parse.urlencode(params)
print(f"参数字典: {params}")
print(f"查询字符串: {query_string}")

# 查询字符串解码
print("\n--- 查询字符串解码 ---")
encoded_query = "name=Alice&age=25&city=%E5%8C%97%E4%BA%AC"
decoded_params = urllib.parse.parse_qs(encoded_query)
print(f"编码查询: {encoded_query}")
print(f"解码参数: {decoded_params}")

print("\n=== 4. bytes 与 str 转换 ===\n")

# bytes 基础
print("--- bytes 创建 ---")
s = "Hello, Python!"
b = s.encode('utf-8')
print(f"字符串: {s} (类型: {type(s).__name__})")
print(f"字节: {b} (类型: {type(b).__name__})")

# 不同编码
print("\n--- 不同编码 ---")
text = "你好世界"
for encoding in ['utf-8', 'gbk', 'utf-16', 'ascii']:
    try:
        encoded = text.encode(encoding)
        print(f"{encoding:10}: {encoded}")
    except UnicodeEncodeError as e:
        print(f"{encoding:10}: 编码失败 - {e.reason}")

# bytes 解码
print("\n--- bytes 解码 ---")
utf8_bytes = "Hello".encode('utf-8')
gbk_bytes = "你好".encode('gbk')

print(f"UTF-8 解码: {utf8_bytes.decode('utf-8')}")
print(f"GBK 解码: {gbk_bytes.decode('gbk')}")

# 错误处理
print("\n--- 编码错误处理 ---")
# errors 参数: 'strict'(默认), 'ignore', 'replace', 'xmlcharrefreplace'
data = b'\xff\xfe'
print(f"原字节: {data}")
print(f"strict (报错): ", end='')
try:
    print(data.decode('utf-8', errors='strict'))
except UnicodeDecodeError as e:
    print(f"错误 - {e}")

print(f"ignore: {data.decode('utf-8', errors='ignore')}")
print(f"replace: {data.decode('utf-8', errors='replace')}")

print("\n=== 5. 编码转换 ===\n")

# Latin-1 <-> UTF-8
print("--- 编码转换 ---")
text = "Café"
utf8_bytes = text.encode('utf-8')
print(f"原文本: {text}")
print(f"UTF-8: {utf8_bytes}")

# 模拟错误的编码转换
# 把 UTF-8 字节当作 Latin-1 来解码
latin1_str = utf8_bytes.decode('latin-1')
print(f"当作 Latin-1 解码: {latin1_str}")

# 修复：重新用正确的编码
correct = latin1_str.encode('latin-1').decode('utf-8')
print(f"修复后: {correct}")

print("\n=== 6. 实用工具函数 ===\n")

class EncodingToolkit:
    """编码工具集"""
    
    @staticmethod
    def to_base64(text):
        """字符串转 Base64"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def from_base64(encoded_text):
        """Base64 转字符串"""
        return base64.b64decode(encoded_text).decode('utf-8')
    
    @staticmethod
    def to_hex(text):
        """字符串转 Hex"""
        return text.encode('utf-8').hex()
    
    @staticmethod
    def from_hex(hex_text):
        """Hex 转字符串"""
        return bytes.fromhex(hex_text).decode('utf-8')
    
    @staticmethod
    def to_url_encode(text):
        """字符串转 URL 编码"""
        return urllib.parse.quote(text)
    
    @staticmethod
    def from_url_encode(encoded_text):
        """URL 编码转字符串"""
        return urllib.parse.unquote(encoded_text)

# 测试工具
toolkit = EncodingToolkit()
text = "Hello, 世界! @#$%"

print(f"原文本: {text}")
print(f"Base64: {toolkit.to_base64(text)}")
print(f"Hex: {toolkit.to_hex(text)}")
print(f"URL: {toolkit.to_url_encode(text)}")

# 链式转换
print("\n--- 链式转换 ---")
result = text
result = toolkit.to_base64(result)
print(f"1. Base64: {result}")
result = toolkit.to_hex(result) 
print(f"2. Hex: {result}")
result = toolkit.to_url_encode(result)
print(f"3. URL: {result}")
