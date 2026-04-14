print("=== 1. 变量与动态类型 ===")

x = 10
print(f"x = {x}, 类型: {type(x)}")
x = "Hello"
print(f"x = {x}, 类型: {type(x)}")
x = [1, 2, 3]
print(f"x = {x}, 类型: {type(x)}")
x = True
print(f"x = {x}, 类型: {type(x)}")
print("\n=== 2. 字符串操作 ===")

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
my_list = [1, 2, 3, 4, 5]
print(f"列表: {my_list}")
my_list.append(6)