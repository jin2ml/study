# 第2月第1周学习代码示例
# 根据第2月第1周的学习内容（JSON 与正则），这些示例覆盖了JSON处理和正则表达式应用。

import json
import re

print("=== 1. JSON 基础操作 ===\n")

# JSON 字符串反序列化
print("--- json.loads() 字符串转对象 ---")
json_str = '{"name": "Alice", "age": 25, "skills": ["Python", "JavaScript"]}'
data = json.loads(json_str)
print(f"类型: {type(data)}")
print(f"数据: {data}")
print(f"获取值: {data['name']}, 年龄: {data['age']}")

# JSON 对象序列化
print("\n--- json.dumps() 对象转字符串 ---")
person = {
    "name": "Bob",
    "age": 30,
    "email": "bob@example.com",
    "hobbies": ["reading", "gaming"]
}
json_output = json.dumps(person)
print(f"紧凑格式: {json_output}")

json_pretty = json.dumps(person, indent=2, ensure_ascii=False)
print(f"美化格式:\n{json_pretty}")

# 处理嵌套 JSON
print("\n--- 嵌套 JSON 处理 ---")
nested_json = '''
{
    "users": [
        {"id": 1, "name": "Alice", "address": {"city": "Beijing", "zip": "10000"}},
        {"id": 2, "name": "Bob", "address": {"city": "Shanghai", "zip": "20000"}},
        {"id": 3, "name": "Charlie", "address": {"city": "Shenzhen", "zip": "30000"}}
    ],
    "total": 3
}
'''

users_data = json.loads(nested_json)
print(f"总用户数: {users_data['total']}")
for user in users_data['users']:
    print(f"  {user['name']} 来自 {user['address']['city']}")

# JSON 字段提取
print("\n--- JSON 字段提取 ---")
def extract_fields(json_obj, fields):
    """从JSON对象中提取指定字段"""
    result = {}
    for field in fields:
        if field in json_obj:
            result[field] = json_obj[field]
    return result

extracted = extract_fields(person, ['name', 'age', 'email'])
print(f"提取字段: {extracted}")

# 安全的 JSON 解析（处理错误）
print("\n--- 安全的 JSON 解析 ---")
invalid_json = '{invalid json}'
try:
    json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")
    print(f"错误位置: 行 {e.lineno}, 列 {e.colno}")

print("\n=== 2. 正则表达式基础 ===\n")

# 基本匹配
print("--- 基本匹配 (match / fullmatch) ---")
pattern = r"^\d{3}-\d{3}-\d{4}$"  # 电话号码格式
tests = ["123-456-7890", "123-45-6789", "123-456-789"]

for test in tests:
    if re.match(pattern, test):
        print(f"  ✓ '{test}' 匹配")
    else:
        print(f"  ✗ '{test}' 不匹配")

# 搜索
print("\n--- 搜索 (search) ---")
text = "联系我：邮箱是 user@example.com 或者 admin@site.org"
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
matches = re.findall(email_pattern, text)
print(f"找到的邮箱: {matches}")

# 分组
print("\n--- 分组提取 (groups) ---")
text = "我的电话是 010-1234-5678"
phone_pattern = r"(\d{3})-(\d{4})-(\d{4})"
match = re.search(phone_pattern, text)
if match:
    print(f"完整匹配: {match.group(0)}")
    print(f"第1组: {match.group(1)}")
    print(f"第2组: {match.group(2)}")
    print(f"第3组: {match.group(3)}")

# 替换
print("\n--- 替换 (sub) ---")
text = "我的电话是 010-1234-5678，你的呢？我的是 020-8888-9999"
result = re.sub(phone_pattern, "***-****-****", text)
print(f"原文本: {text}")
print(f"替换后: {result}")

# 使用替换函数
print("\n--- 替换函数 (sub with function) ---")
def mask_digits(match):
    """将匹配的数字替换为*"""
    text = match.group(0)
    return text[:2] + '*' * (len(text) - 4) + text[-2:]

result = re.sub(r"\d{4,}", mask_digits, "我的卡号是 1234567890，账号是 9876543210")
print(f"结果: {result}")

# 分割
print("\n--- 分割 (split) ---")
text = "Python,JavaScript;Go,Rust"
result = re.split(r'[,;]', text)
print(f"分割结果: {result}")

# 编译正则表达式
print("\n--- 编译正则表达式 (compile) ---")
compiled_pattern = re.compile(email_pattern)
text = "联系 alice@example.com 或 bob@test.org"
matches = compiled_pattern.findall(text)
print(f"找到的邮箱: {matches}")

print("\n=== 3. JSON + 正则综合应用 ===\n")

# 从 JSON 中提取信息并进行正则处理
print("--- JSON 数据处理 ---")
json_data = '''
{
    "contacts": [
        {
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "010-1234-5678",
            "bio": "我在学习 Python 和 JavaScript"
        },
        {
            "name": "Bob",
            "email": "bob@example.org",
            "phone": "020-8888-9999",
            "bio": "喜欢编程，特别是 Go 和 Rust"
        }
    ]
}
'''

contacts = json.loads(json_data)

for contact in contacts['contacts']:
    print(f"\n联系人: {contact['name']}")
    
    # 验证邮箱
    if re.match(r'^[^@]+@[^@]+\.[a-z]{2,}$', contact['email']):
        print(f"  邮箱: {contact['email']} ✓")
    
    # 验证电话
    if re.match(r'^\d{3}-\d{4}-\d{4}$', contact['phone']):
        print(f"  电话: {contact['phone']} ✓")
    
    # 提取 bio 中的编程语言
    languages = re.findall(r'\b(Python|JavaScript|Go|Rust|Java|C\+\+)\b', contact['bio'])
    if languages:
        print(f"  技能: {', '.join(set(languages))}")

# 正则验证 JSON 内容
print("\n--- 正则验证 JSON 内容 ---")

def validate_email_in_json(json_str):
    """验证 JSON 中的所有邮箱格式"""
    data = json.loads(json_str)
    email_pattern = r'^[^@]+@[^@]+\.[a-z]{2,}$'
    
    invalid_emails = []
    
    if isinstance(data, dict) and 'email' in data:
        if not re.match(email_pattern, data['email']):
            invalid_emails.append(data['email'])
    
    return invalid_emails

test_json = '{"name": "Test", "email": "invalid-email"}'
invalid = validate_email_in_json(test_json)
if invalid:
    print(f"无效的邮箱: {invalid}")
else:
    print("所有邮箱验证通过")

print("\n=== 4. 实用工具函数 ===\n")

def parse_query_string(query_str):
    """解析查询字符串为 JSON"""
    pattern = r'([^&=]+)=([^&]*)'
    matches = re.findall(pattern, query_str)
    result = {}
    for key, value in matches:
        result[key] = value
    return result

# 测试
query = "name=alice&age=25&city=Beijing&skills=Python,JavaScript"
parsed = parse_query_string(query)
print(f"查询字符串: {query}")
print(f"解析结果: {json.dumps(parsed, ensure_ascii=False, indent=2)}")

def extract_json_from_text(text):
    """从文本中提取 JSON 对象"""
    pattern = r'\{[^{}]*\}'
    matches = re.finditer(pattern, text)
    jsons = []
    for match in matches:
        try:
            json_obj = json.loads(match.group(0))
            jsons.append(json_obj)
        except:
            pass
    return jsons

# 测试
text = '这是一些文本，包含JSON {"name": "Alice", "age": 25} 和 {"name": "Bob"}'
extracted_jsons = extract_json_from_text(text)
print(f"\n从文本中提取的 JSON:")
for j in extracted_jsons:
    print(f"  {j}")
