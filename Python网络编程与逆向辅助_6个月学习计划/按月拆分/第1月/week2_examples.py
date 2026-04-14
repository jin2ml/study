# 第2周学习代码示例
# 根据第2周的学习内容（函数与模块），这些示例覆盖了函数定义、参数传递、模块导入、内置函数等。

print("=== 1. 函数定义与返回值 ===")
# 基本函数定义
def greet(name):
    """这是一个简单的问候函数"""
    return f"Hello, {name}!"

result = greet("Alice")
print(result)

# 多个返回值
def get_user_info():
    name = "Bob"
    age = 30
    city = "Beijing"
    return name, age, city

name, age, city = get_user_info()
print(f"用户: {name}, 年龄: {age}, 城市: {city}")

# 没有返回值的函数（隐式返回 None）
def print_separator():
    print("-" * 40)

print_separator()

print("\n=== 2. 默认参数 ===")
# 函数定义时设置默认参数值
def create_greeting(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(create_greeting("Alice"))  # 使用默认参数
print(create_greeting("Bob", "Hi"))  # 覆盖默认参数

# 多个默认参数
def calculate_total(price, quantity=1, tax_rate=0.1):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal + tax

print(f"总价: {calculate_total(100)}")  # 默认数量1，税率10%
print(f"总价: {calculate_total(100, 5)}")  # 数量5，税率10%
print(f"总价: {calculate_total(100, 5, 0.05)}")  # 数量5，税率5%

print("\n=== 3. 关键字参数 ===")
# 使用关键字参数调用函数
def create_profile(name, age, city, job=None):
    info = f"名字: {name}, 年龄: {age}, 城市: {city}"
    if job:
        info += f", 职位: {job}"
    return info

# 位置参数
print(create_profile("Alice", 25, "Beijing"))

# 关键字参数（顺序可以不同）
print(create_profile(name="Bob", age=30, city="Shanghai", job="Engineer"))
print(create_profile(age=28, name="Charlie", city="Shenzhen"))

# 混合位置参数和关键字参数
print(create_profile("Diana", 26, city="Hangzhou", job="Designer"))

print("\n=== 4. *args 和 **kwargs（可变参数）===")
# *args：接收任意数量的位置参数（作为元组）
def sum_numbers(*args):
    """计算任意数量的数字之和"""
    print(f"接收到的参数: {args}")
    return sum(args)

print(f"总和: {sum_numbers(1, 2, 3)}")
print(f"总和: {sum_numbers(1, 2, 3, 4, 5)}")

# **kwargs：接收任意数量的关键字参数（作为字典）
def print_user_info(**kwargs):
    """打印用户信息"""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print("用户信息:")
print_user_info(name="Alice", age=25, city="Beijing", job="Engineer")

# 混合 *args 和 **kwargs
def flexible_function(a, b, *args, **kwargs):
    print(f"必须参数 a: {a}, b: {b}")
    print(f"可变位置参数 *args: {args}")
    print(f"可变关键字参数 **kwargs: {kwargs}")

flexible_function(1, 2, 3, 4, 5, name="Alice", age=25)

print("\n=== 5. 模块导入 ===")
# 导入整个模块
import math
print(f"π的值: {math.pi}")
print(f"计算根号16: {math.sqrt(16)}")

# 从模块导入特定函数/变量
from datetime import datetime, timedelta
now = datetime.now()
print(f"当前时间: {now}")

tomorrow = now + timedelta(days=1)
print(f"明天: {tomorrow.strftime('%Y-%m-%d')}")

# 导入并别名
import random as rnd
print(f"随机数: {rnd.randint(1, 100)}")

# 从模块导入并别名
from os.path import join as path_join
print(f"路径: {path_join('home', 'user', 'file.txt')}")

print("\n=== 6. 常用内置函数 ===")
# len()：获取长度
items = [1, 2, 3, 4, 5]
print(f"列表长度: {len(items)}")

# range()：生成数字序列
print(f"range(5)生成: {list(range(5))}")
print(f"range(2, 8)生成: {list(range(2, 8))}")
print(f"range(1, 10, 2)生成: {list(range(1, 10, 2))}")

# map()：对所有元素应用函数
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(f"平方后: {squared}")

# filter()：过滤元素
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

# zip()：合并多个序列
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 28]
combined = list(zip(names, ages))
print(f"合并后: {combined}")

# sorted()：排序
scores = [85, 92, 78, 95, 88]
print(f"排序: {sorted(scores)}")
print(f"降序: {sorted(scores, reverse=True)}")

# enumerate()：获取下标和值
for index, name in enumerate(names):
    print(f"  {index}: {name}")

print("\n=== 7. if __name__ == '__main__' ===")
# 这个条件检查脚本是否直接运行（而不是被导入）
# 通常用于定义 main() 函数

def main():
    """主函数"""
    print("这是主程序执行的代码")
    print("如果这个脚本被导入到其他脚本中，这段代码不会执行")

if __name__ == "__main__":
    print("脚本直接运行，执行 main() 函数")
    main()
else:
    print("脚本被导入到其他模块中")

print("\n=== 8. 函数作为参数 ===")
# 函数可以作为参数传递给其他函数
def apply_operation(a, b, operation):
    """对两个数字应用操作"""
    return operation(a, b)

def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

print(f"加法: {apply_operation(5, 3, add)}")
print(f"乘法: {apply_operation(5, 3, multiply)}")

# 使用 lambda 函数
print(f"减法: {apply_operation(5, 3, lambda x, y: x - y)}")
print(f"除法: {apply_operation(10, 2, lambda x, y: x / y)}")

print("\n=== 9. 函数的文档 ===")
def calculate_area(radius):
    """
    计算圆的面积
    
    参数:
        radius: 圆的半径（必须为正数）
    
    返回:
        圆的面积
    """
    import math
    return math.pi * radius ** 2

# 查看函数文档
print("函数文档:")
print(calculate_area.__doc__)

# 调用函数
area = calculate_area(5)
print(f"半径为5的圆的面积: {area:.2f}")
