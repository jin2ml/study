# 第2月第4周学习代码示例
# 根据第2月第4周的学习内容（压缩与解压），这些示例覆盖了gzip、zlib、binascii、响应解压验证。

import gzip
import zlib
import binascii
import io
import json

print("=== 1. gzip 压缩与解压 ===\n")

# 字符串 gzip 压缩
print("--- gzip 基础 ---")
text = "Hello, Python! " * 100  # 重复文本以看到压缩效果
text_bytes = text.encode('utf-8')

print(f"原始大小: {len(text_bytes)} 字节")

# 压缩
compressed = gzip.compress(text_bytes)
print(f"压缩后: {len(compressed)} 字节")
print(f"压缩率: {len(compressed) / len(text_bytes) * 100:.2f}%")

# 解压
decompressed = gzip.decompress(compressed)
print(f"解压后: {len(decompressed)} 字节")
print(f"解压验证: {text_bytes == decompressed}")

# 文件 gzip 操作
print("\n--- gzip 文件操作 ---")
test_file = "test_compressed.txt.gz"
test_content = "这是测试内容。" * 50

# 写入 gzip 文件
with gzip.open(test_file, 'wt', encoding='utf-8') as f:
    f.write(test_content)
print(f"已创建压缩文件: {test_file}")

# 读取 gzip 文件
with gzip.open(test_file, 'rt', encoding='utf-8') as f:
    read_content = f.read()

print(f"读取验证: {read_content == test_content}")

# 检查文件大小
import os
if os.path.exists(test_file):
    original_size = len(test_content.encode('utf-8'))
    compressed_size = os.path.getsize(test_file)
    print(f"原始内容大小: {original_size} 字节")
    print(f"压缩文件大小: {compressed_size} 字节")

# 流式 gzip 处理
print("\n--- 流式处理 ---")
data = b"Stream processing example " * 100
buffer = io.BytesIO()

# 写入压缩数据
with gzip.GzipFile(fileobj=buffer, mode='wb') as gz:
    gz.write(data)

# 获取压缩数据
compressed_data = buffer.getvalue()
print(f"原始大小: {len(data)}")
print(f"压缩大小: {len(compressed_data)}")

# 读取压缩数据
buffer.seek(0)
with gzip.GzipFile(fileobj=buffer, mode='rb') as gz:
    decompressed_data = gz.read()

print(f"解压验证: {data == decompressed_data}")

print("\n=== 2. zlib 压缩与解压 ===\n")

# zlib 基础
print("--- zlib 基础 ---")
text = "Zlib compression example " * 100
text_bytes = text.encode('utf-8')

print(f"原始大小: {len(text_bytes)} 字节")

#压缩
compressed_zlib = zlib.compress(text_bytes)
print(f"压缩后: {len(compressed_zlib)} 字节")
print(f"压缩率: {len(compressed_zlib) / len(text_bytes) * 100:.2f}%")

# 解压
decompressed_zlib = zlib.decompress(compressed_zlib)
print(f"解压验证: {text_bytes == decompressed_zlib}")

# gzip vs zlib
print("\n--- gzip vs zlib 对比 ---")
test_data = "Compression comparison " * 100
test_bytes = test_data.encode('utf-8')

gz_compressed = gzip.compress(test_bytes)
zl_compressed = zlib.compress(test_bytes)

print(f"原始大小: {len(test_bytes)} 字节")
print(f"gzip 压缩: {len(gz_compressed)} 字节")
print(f"zlib 压缩: {len(zl_compressed)} 字节")
print(f"zlib 通常更小，因为没有 gzip 文件头")

# 压缩级别
print("\n--- 压缩级别 ---")
data = "Level test " * 1000
for level in [1, 6, 9]:
    compressed = zlib.compress(data.encode(), level=level)
    print(f"级别 {level}: {len(compressed)} 字节")

# 增量压缩
print("\n--- 增量压缩 ---")
compressor = zlib.compressobj()
data_parts = [
    "Part 1 " * 100,
    "Part 2 " * 100,
    "Part 3 " * 100
]

compressed_parts = []
for part in data_parts:
    part_compressed = compressor.compress(part.encode())
    if part_compressed:
        compressed_parts.append(part_compressed)

final_data = compressor.flush()
if final_data:
    compressed_parts.append(final_data)

total_compressed = b''.join(compressed_parts)
print(f"分段压缩完成，总大小: {len(total_compressed)} 字节")

# 增量解压
decompressor = zlib.decompressobj()
decompressed_data = b''
for part in compressed_parts:
    decompressed_data += decompressor.decompress(part)

decompressed_data += decompressor.flush()
print(f"分段解压验证: {''.join(data_parts) == decompressed_data.decode()}")

print("\n=== 3. JSON 压缩 ===\n")

# JSON 数据压缩
print("--- JSON 压缩 ---")
json_data = {
    'users': [
        {'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com'}
        for i in range(100)
    ]
}

json_str = json.dumps(json_data)
json_bytes = json_str.encode('utf-8')

print(f"原始 JSON 大小: {len(json_bytes)} 字节")

# 压缩
compressed_json = gzip.compress(json_bytes)
print(f"压缩后大小: {len(compressed_json)} 字节")
print(f"压缩率: {len(compressed_json) / len(json_bytes) * 100:.2f}%")

# 解压并解析
decompressed_json = gzip.decompress(compressed_json).decode('utf-8')
parsed_data = json.loads(decompressed_json)
print(f"解压并解析成功: {len(parsed_data['users'])} 条用户数据")

print("\n=== 4. HTTP 响应解压 ===\n")

# 模拟 HTTP 响应
print("--- 模拟压缩的 HTTP 响应 ---")

class MockHTTPResponse:
    """模拟 HTTP 响应"""
    
    def __init__(self, content, encoding='gzip'):
        self.encoding = encoding
        if encoding == 'gzip':
            self.content = gzip.compress(content.encode('utf-8'))
        elif encoding == 'deflate':
            self.content = zlib.compress(content.encode('utf-8'))
        else:
            self.content = content.encode('utf-8')
        
        self.headers = {'Content-Encoding': encoding}
    
    def get_content(self):
        """获取解压后的内容"""
        encoding = self.headers.get('Content-Encoding', 'identity')
        
        if encoding == 'gzip':
            return gzip.decompress(self.content).decode('utf-8')
        elif encoding == 'deflate':
            return zlib.decompress(self.content).decode('utf-8')
        else:
            return self.content.decode('utf-8')

# 创建模拟响应
response_data = "这是一个模拟的 HTTP 响应" * 100
response = MockHTTPResponse(response_data, encoding='gzip')

print(f"Content-Encoding: {response.headers['Content-Encoding']}")
print(f"压缩内容大小: {len(response.content)} 字节")

# 解压内容
decompressed = response.get_content()
print(f"解压后大小: {len(decompressed)} 字节")
print(f"内容验证: {decompressed == response_data}")

# 处理不同编码
print("\n--- 自动处理多种编码 ---")
def decompress_response(content_bytes, encoding):
    """根据编码解压内容"""
    if encoding == 'gzip':
        return gzip.decompress(content_bytes).decode('utf-8')
    elif encoding in ('deflate', 'x-deflate'):
        return zlib.decompress(content_bytes).decode('utf-8')
    elif encoding == 'identity' or encoding is None:
        return content_bytes.decode('utf-8')
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")

# 测试
encodings = ['gzip', 'deflate', 'identity']
test_content = "Test content" * 100

for enc in encodings:
    if enc == 'gzip':
        compressed = gzip.compress(test_content.encode())
    elif enc == 'deflate':
        compressed = zlib.compress(test_content.encode())
    else:
        compressed = test_content.encode()
    
    try:
        decompressed = decompress_response(compressed, enc)
        print(f"{enc:10}: 解压成功 ({len(decompressed)} 字符)")
    except Exception as e:
        print(f"{enc:10}: 解压失败 - {e}")

print("\n=== 5. 实用工具类 ===\n")

class CompressionToolkit:
    """压缩工具集"""
    
    @staticmethod
    def gzip_string(data):
        """压缩字符串"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return gzip.compress(data)
    
    @staticmethod
    def ungzip_string(data):
        """解压缩字符串"""
        return gzip.decompress(data).decode('utf-8')
    
    @staticmethod
    def zlib_string(data, level=6):
        """zlib 压缩"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return zlib.compress(data, level)
    
    @staticmethod
    def unzlib_string(data):
        """zlib 解压"""
        return zlib.decompress(data).decode('utf-8')
    
    @staticmethod
    def get_compression_ratio(original, compressed):
        """获取压缩率"""
        if isinstance(original, str):
            original = original.encode('utf-8')
        if isinstance(compressed, bytes):
            compressed = len(compressed)
        if isinstance(original, bytes):
            original = len(original)
        return (1 - compressed / original) * 100 if original > 0 else 0

# 测试工具
toolkit = CompressionToolkit()
test_data = "Toolkit test " * 200

gzip_data = toolkit.gzip_string(test_data)
ungzip_data = toolkit.ungzip_string(gzip_data)

print(f"原始: {len(test_data)} 字符")
print(f"gzip: {len(gzip_data)} 字节")
print(f"压缩率: {toolkit.get_compression_ratio(test_data, gzip_data):.2f}%")
print(f"解压验证: {ungzip_data == test_data}")

# 清理测试文件
import os
if os.path.exists(test_file):
    os.remove(test_file)
    print(f"\n已删除测试文件: {test_file}")
