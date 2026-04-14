# 第1周学习代码示例
# 根据第1周的学习内容（语法与数据结构），这些示例覆盖了变量与动态类型、字符串、列表、元组、字典、集合、控制流（if/for/while）、切片与推导式。

print("=== 1. 变量与动态类型 ===")
# Python是动态类型语言，变量可以随时改变类型
x = 10          # 整数
print(f"x = {x}, 类型: {type(x)}")

x = "Hello"     # 字符串
print(f"x = {x}, 类型: {type(x)}")

x = [1, 2, 3]   # 列表
print(f"x = {x}, 类型: {type(x)}")

x = True        # 布尔值
print(f"x = {x}, 类型: {type(x)}")

print("\n=== 2. 字符串操作 ===")
# 字符串的基本操作
s = "Hello, World!"
print(f"字符串: {s}")
print(f"长度: {len(s)}")
print(f"大写: {s.upper()}")
print(f"小写: {s.lower()}")
print(f"替换: {s.replace('World', 'Python')}")
print(f"分割: {s.split(', ')}")
print(f"索引: {s[0]} (第一个字符)")
print(f"切片: {s[7:13]} (从索引7到13)")

print("\n=== 3. 列表、元组、字典、集合 ===")
# 列表（可变）
my_list = [1, 2, 3, 4, 5]
print(f"列表: {my_list}")
my_list.append(6)  # 添加元素
print(f"添加后: {my_list}")
my_list[0] = 10    # 修改元素
print(f"修改后: {my_list}")

# 元组（不可变）
my_tuple = (1, 2, 3, 4, 5)
print(f"元组: {my_tuple}")
# my_tuple[0] = 10  # 这会报错，因为元组不可变

# 字典（键值对）
my_dict = {"name": "Alice", "age": 25, "city": "Beijing"} 
print(f"字典: {my_dict.get('name')}")
print(f"获取值: {my_dict['name']}")
my_dict["job"] = "Engineer"  # 添加键值对
print(f"添加后: {my_dict}")

# 集合（无序、不重复）
my_set = {1, 2, 3, 4, 5, 5}  # 重复的5会被忽略
print(f"集合: {my_set}")
my_set.add(6)  # 添加元素
print(f"添加后: {my_set}")

print("\n=== 4. 控制流：if / for / while ===")
# if 语句
age = 18
if age >= 18:
    print("你是成年人")
elif age >= 13:
    print("你是青少年")
else:
    print("你是儿童")

# for 循环
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"我喜欢 {fruit}")

# while 循环
count = 0
while count < 5:
    print(f"计数: {count}")
    count += 1

print("\n=== 5. 切片与推导式 ===")
# 切片（适用于列表、字符串等）
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"原列表: {numbers}")
print(f"前5个: {numbers[:5]}")
print(f"后5个: {numbers[-5:]}")
print(f"步长2: {numbers[::2]}")
print(f"反转: {numbers[::-1]}")

# 列表推导式
squares = [x**2 for x in range(10)]  # 生成0到9的平方
print(f"平方列表: {squares}")

even_squares = [x**2 for x in range(10) if x % 2 == 0]  # 偶数的平方
print(f"偶数平方: {even_squares}")

# 字典推导式
squares_dict = {x: x**2 for x in range(5)}
print(f"平方字典: {squares_dict}")

# 集合推导式
squares_set = {x**2 for x in range(10)}
print(f"平方集合: {squares_set}")