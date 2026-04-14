# 第3周学习代码示例
# 根据第3周的学习内容（文件与异常），这些示例覆盖了文件读写、JSON处理、异常处理、路径处理和日志输出。

import os
import json
import logging
from pathlib import Path

print("=== 1. 文本文件读写 ===")

# 创建示例文件用于演示
example_file = "test_file.txt"
with open(example_file, 'w', encoding='utf-8') as f:
    f.write("第一行：Hello, World!\n")
    f.write("第二行：Python 文件操作\n")
    f.write("第三行：学习读写文件\n")

print(f"文件 '{example_file}' 已创建")

# 读整个文件
print("\n--- 方法1：读整个文件 ---")
with open(example_file, 'r', encoding='utf-8') as f:
    content = f.read()
print(f"文件内容:\n{content}")

# 按行读取
print("--- 方法2：按行读取 ---")
with open(example_file, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        print(f"行 {line_num}: {line.rstrip()}")

# readlines() 读取所有行
print("--- 方法3：readlines() ---")
with open(example_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        print(f"行 {i}: {line.rstrip()}")

# 追加写入
print("--- 追加写入 ---")
with open(example_file, 'a', encoding='utf-8') as f:
    f.write("第四行：追加的内容\n")
print("已追加一行")

# 覆盖写入
print("--- 覆盖写入 ---")
with open(example_file, 'w', encoding='utf-8') as f:
    f.write("这是新内容\n")
    f.write("覆盖了原来的所有内容\n")
print("文件已覆盖")

print("\n=== 2. JSON 文件读写 ===")

# 创建实例数据
users = [
    {"id": 1, "name": "Alice", "age": 25, "city": "Beijing"},
    {"id": 2, "name": "Bob", "age": 30, "city": "Shanghai"},
    {"id": 3, "name": "Charlie", "age": 28, "city": "Shenzhen"}
]

json_file = "users.json"

# 写入 JSON 文件
print("--- 写入 JSON 文件 ---")
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(users, f, ensure_ascii=False, indent=2)
print(f"JSON 数据已保存到 '{json_file}'")

# 读取 JSON 文件
print("--- 读取 JSON 文件 ---")
with open(json_file, 'r', encoding='utf-8') as f:
    loaded_users = json.load(f)
print(f"加载的数据: {loaded_users}")

# 美化输出 JSON
print("--- 美化输出 JSON ---")
with open(json_file, 'r', encoding='utf-8') as f:
    content = f.read()
print(content)

# JSON 字符串与 Python 对象互换
print("--- JSON 字符串转换 ---")
json_string = '{"name": "Diana", "age": 26, "city": "Hangzhou"}'
user_dict = json.loads(json_string)  # 字符串 -> 字典
print(f"从 JSON 字符串解析: {user_dict}")

new_json_string = json.dumps(user_dict, ensure_ascii=False)  # 字典 -> 字符串
print(f"转换为 JSON 字符串: {new_json_string}")

print("\n=== 3. try/except/finally 异常处理 ===")

# 基本异常处理
print("--- 基本异常处理 ---")
try:
    num = int("abc")  # 这会抛出 ValueError
except ValueError:
    print("错误: 无法将字符串转换为整数")

# 多个异常处理
print("--- 多个异常处理 ---")
try:
    data = {"name": "Alice"}
    age = data["age"]  # KeyError
except KeyError:
    print("错误: 字典中没有 'age' 键")
except ValueError:
    print("错误: 值的类型不正确")

# 捕获所有异常
print("--- 捕获所有异常 ---")
try:
    result = 10 / 0  # ZeroDivisionError
except Exception as e:
    print(f"捕获异常: {type(e).__name__}: {e}")

# 异常对象信息
print("--- 获取异常详情 ---")
try:
    file = open("nonexistent_file.txt", 'r')
except FileNotFoundError as e:
    print(f"异常类型: {type(e).__name__}")
    print(f"异常信息: {e}")
    print(f"错误码: {e.errno}")

# finally 块
print("--- try/except/finally ---")
try:
    f = open(example_file, 'r', encoding='utf-8')
    content = f.read()
    print(f"读取文件成功，内容长度: {len(content)}")
except FileNotFoundError:
    print("错误: 文件不存在")
finally:
    f.close()
    print("文件已关闭（finally 块执行）")

# else 块（异常未发生时执行）
print("--- try/except/else/finally ---")
try:
    num = int("123")
except ValueError:
    print("错误: 无法转换")
else:
    print(f"成功转换: {num}")
finally:
    print("处理完成")

print("\n=== 4. 路径处理 ===")

# os.path 方法
print("--- os.path 方法 ---")
file_path = "users.json"
print(f"文件名: {os.path.basename(file_path)}")
print(f"目录名: {os.path.dirname(file_path)}")
print(f"绝对路径: {os.path.abspath(file_path)}")
print(f"文件是否存在: {os.path.exists(file_path)}")
print(f"是否是文件: {os.path.isfile(file_path)}")
print(f"是否是目录: {os.path.isdir('.')}")

# 路径拼接
print("--- 路径拼接 ---")
dir_path = "/home/user"
filename = "document.txt"
full_path = os.path.join(dir_path, filename)
print(f"拼接结果: {full_path}")

# 获取文件大小
print("--- 文件信息 ---")
if os.path.exists(json_file):
    size = os.path.getsize(json_file)
    print(f"文件大小: {size} 字节")

# pathlib.Path 方法（更现代）
print("--- pathlib.Path 方法 ---")
p = Path(json_file)
print(f"Name: {p.name}")
print(f"Parent: {p.parent}")
print(f"Absolute: {p.absolute()}")
print(f"Suffix: {p.suffix}")
print(f"Exists: {p.exists()}")
print(f"Is file: {p.is_file()}")

# 创建目录
print("--- 创建目录 ---")
new_dir = "data_folder"
if not os.path.exists(new_dir):
    os.makedirs(new_dir)
    print(f"目录 '{new_dir}' 已创建")
else:
    print(f"目录 '{new_dir}' 已存在")

# 列出目录内容
print("--- 列出目录内容 ---")
files = os.listdir('.')
print(f"当前目录包含: {[f for f in files if not f.startswith('.')][:5]}...")

print("\n=== 5. 基础日志输出 ===")

# 配置日志
log_file = "app.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 不同日志级别
logger.debug("这是调试信息")
logger.info("这是普通信息")
logger.warning("这是警告")
logger.error("这是错误")
logger.critical("这是严重错误")

print(f"\n日志已保存到 '{log_file}'")

# 自定义日志格式
print("--- 自定义日志 ---")
custom_logger = logging.getLogger("custom")
handler = logging.StreamHandler()
formatter = logging.Formatter('【%(levelname)s】 %(message)s')
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.INFO)

custom_logger.info("自定义格式的日志信息")

print("\n=== 清理示例文件 ===")
# 删除测试文件
for file in [example_file, json_file, new_dir]:
    try:
        if os.path.isfile(file):
            os.remove(file)
            print(f"已删除文件: {file}")
        elif os.path.isdir(file):
            os.rmdir(file)
            print(f"已删除目录: {file}")
    except Exception as e:
        print(f"删除 {file} 失败: {e}")
