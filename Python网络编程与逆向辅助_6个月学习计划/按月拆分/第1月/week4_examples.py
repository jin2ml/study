# 第4周学习代码示例
# 根据第4周的学习内容（脚本化练习），这些示例覆盖了命令行参数解析、目录遍历、关键词统计和批量处理文本文件。

import sys
import os
import json
from pathlib import Path
from collections import Counter
import argparse

print("=== 1. 命令行参数解析 ===\n")

# 方法1：使用 sys.argv（基础方式）
print("--- 方法1：sys.argv ---")
print(f"脚本名称: {sys.argv[0]}")
print(f"所有参数: {sys.argv}")
print(f"参数数量: {len(sys.argv) - 1}")

# 示例：简单的参数处理
if len(sys.argv) > 1:
    print(f"第一个参数: {sys.argv[1]}")

# 方法2：使用 argparse（推荐方式）
print("\n--- 方法2：argparse ---")

# 创建示例脚本（这在实际使用中会作为独立脚本）
def example_argparse():
    """演示 argparse 的用法"""
    parser = argparse.ArgumentParser(
        description="这是一个示例脚本，用于演示命令行参数解析",
        prog="example_script.py"
    )
    
    # 添加位置参数
    parser.add_argument('input_file', help='输入文件的路径')
    
    # 添加可选参数
    parser.add_argument('-o', '--output', help='输出文件的路径', default='output.txt')
    parser.add_argument('-v', '--verbose', action='store_true', help='启用详细输出')
    parser.add_argument('-n', '--number', type=int, default=10, help='处理数字（默认10）')
    
    # 演示参数
    test_args = ['input.txt', '-o', 'result.txt', '-v', '-n', '20']
    args = parser.parse_args(test_args)
    
    print(f"输入文件: {args.input_file}")
    print(f"输出文件: {args.output}")
    print(f"详细输出: {args.verbose}")
    print(f"数字参数: {args.number}")
    
    return args

example_argparse()

print("\n=== 2. 目录遍历 ===\n")

# 创建测试目录结构
test_dir = "test_data"
os.makedirs(f"{test_dir}/subdir1", exist_ok=True)
os.makedirs(f"{test_dir}/subdir2", exist_ok=True)

# 创建测试文件
test_files = [
    f"{test_dir}/file1.txt",
    f"{test_dir}/file2.py",
    f"{test_dir}/subdir1/file3.txt",
    f"{test_dir}/subdir2/file4.json"
]

for file in test_files:
    with open(file, 'w', encoding='utf-8') as f:
        f.write(f"这是测试文件: {file}\n")

print("--- 方法1：os.walk() ---")
for root, dirs, files in os.walk(test_dir):
    level = root.replace(test_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")

print("\n--- 方法2：pathlib.Path.glob() / rglob() ---")
p = Path(test_dir)
print("使用 glob('*.txt'):")
for file in p.glob('*.txt'):
    print(f"  {file}")

print("\n使用 rglob('*.txt')（递归）:")
for file in p.rglob('*.txt'):
    print(f"  {file}")

print("\n--- 方法3：递归函数遍历 ---")
def traverse_directory(directory, level=0):
    """递归遍历目录"""
    items = os.listdir(directory)
    for item in items:
        path = os.path.join(directory, item)
        indent = "  " * level
        if os.path.isdir(path):
            print(f"{indent}📁 {item}/")
            traverse_directory(path, level + 1)
        else:
            print(f"{indent}📄 {item}")

traverse_directory(test_dir)

print("\n=== 3. 关键词统计 ===\n")

# 创建示例文本文件
sample_text_file = "sample.txt"
sample_text = """
Python 是一种强大的编程语言。
Python 易于学习，Python 易于使用。
学习 Python，掌握编程基础。
Python 在数据分析中被广泛使用。
编程 需要 坚持，编程 需要 思考。
"""

with open(sample_text_file, 'w', encoding='utf-8') as f:
    f.write(sample_text)

# 统计关键词
print("--- 统计文本中的关键词 ---")
with open(sample_text_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 简单的分词（按空白符分割）
words = content.split()
print(f"总词数: {len(words)}")

# 统计词频
word_count = Counter(words)
print("\n词频排行（top 5）:")
for word, count in word_count.most_common(5):
    print(f"  '{word}': {count} 次")

# 统计特定关键词
print("\n--- 统计特定关键词 ---")
keywords = ['Python', '编程', '学习']
for keyword in keywords:
    count = content.count(keyword)
    print(f"'{keyword}' 出现 {count} 次")

# 按行统计
print("\n--- 按行统计 ---")
lines = content.strip().split('\n')
print(f"总行数: {len(lines)}")
for i, line in enumerate(lines, 1):
    word_count_per_line = len(line.split())
    print(f"第 {i} 行: {word_count_per_line} 个词")

print("\n=== 4. 批量处理文本文件 ===\n")

# 创建多个测试文件
batch_dir = "batch_files"
os.makedirs(batch_dir, exist_ok=True)

# 生成测试文件
for i in range(3):
    filename = f"{batch_dir}/document_{i+1}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"这是文档 {i+1}\n")
        f.write(f"包含一些内容和数据\n")
        f.write(f"用于批量处理演示\n")

print("--- 批量读取和处理文件 ---")
output_log = []

for file_path in os.listdir(batch_dir):
    if file_path.endswith('.txt'):
        full_path = os.path.join(batch_dir, file_path)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 处理内容
        lines = content.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        info = {
            'filename': file_path,
            'lines': len(non_empty_lines),
            'size': len(content)
        }
        output_log.append(info)
        
        print(f"  {file_path}: {len(non_empty_lines)} 行, {len(content)} 字节")

print("\n--- 批量处理结果保存为 JSON ---")
result_file = "batch_result.json"
with open(result_file, 'w', encoding='utf-8') as f:
    json.dump(output_log, f, ensure_ascii=False, indent=2)
print(f"结果已保存到 {result_file}")

# 显示结果
with open(result_file, 'r', encoding='utf-8') as f:
    print(f.read())

print("\n--- 批量转换文件格式 ---")
converted_dir = "converted_files"
os.makedirs(converted_dir, exist_ok=True)

# 将 .txt 转换为 .md
for file_path in os.listdir(batch_dir):
    if file_path.endswith('.txt'):
        src = os.path.join(batch_dir, file_path)
        dst_name = file_path.replace('.txt', '.md')
        dst = os.path.join(converted_dir, dst_name)
        
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 添加 Markdown 格式
        markdown_content = f"# {dst_name}\n\n{content}"
        
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  {file_path} -> {dst_name}")

print("\n--- 功能整合：创建文件处理函数 ---")

def process_directory(directory, filter_pattern=None, operation=None):
    """
    批量处理目录中的文件
    
    参数:
        directory: 目录路径
        filter_pattern: 文件名过滤器（如 '*.txt'）
        operation: 对每个文件执行的操作函数
    
    返回:
        処理文件的总数
    """
    count = 0
    p = Path(directory)
    
    pattern = filter_pattern or '*'
    for file_path in p.glob(pattern):
        if file_path.is_file():
            if operation:
                operation(file_path)
            count += 1
    
    return count

# 定义一个操作函数
def print_file_info(file_path):
    """打印文件信息"""
    size = file_path.stat().st_size
    lines = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = len(f.readlines())
    except:
        lines = 0
    print(f"  {file_path.name}: {lines} 行, {size} 字节")

print("处理所有 .txt 文件:")
total = process_directory(batch_dir, '*.txt', print_file_info)
print(f"总共处理了 {total} 个文件")

print("\n=== 实操练习：完整的文本分析脚本 ===\n")

class TextAnalyzer:
    """文本分析器类"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.words = []
        self.lines = []
    
    def load(self):
        """加载文件"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        self.lines = self.content.split('\n')
        self.words = self.content.split()
    
    def analyze(self):
        """分析文本"""
        return {
            'file': self.file_path,
            'total_chars': len(self.content),
            'total_words': len(self.words),
            'total_lines': len([l for l in self.lines if l.strip()]),
            'avg_line_length': len(self.content) / max(1, len(self.lines))
        }

# 使用分析器
analyzer = TextAnalyzer(sample_text_file)
analyzer.load()
result = analyzer.analyze()

print("文本分析结果:")
for key, value in result.items():
    if isinstance(value, float):
        print(f"  {key}: {value:.2f}")
    else:
        print(f"  {key}: {value}")

print("\n=== 清理测试文件 ===")
# 清理生成的测试文件和目录
import shutil

for item in [test_dir, batch_dir, converted_dir, sample_text_file, result_file]:
    try:
        if os.path.isfile(item):
            os.remove(item)
            print(f"已删除文件: {item}")
        elif os.path.isdir(item):
            shutil.rmtree(item)
            print(f"已删除目录: {item}")
    except Exception as e:
        print(f"删除 {item} 失败: {e}")
