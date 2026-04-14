# 第4月第1周学习代码示例
# 根据第4月第1周的学习内容（Socket基础），这些示例覆盖了socket模块、TCP/UDP区别、客户端与服务端基础。

import socket
import struct

print("=== 1. Socket 基础概念 ===\n")

print("--- 网络通信的本质 ---")
print("""
网络通信 = 字节流传输

Socket（套接字）：
  - 是网络通信的端点
  - 通过文件描述符表示
  - 可以认为是一个"管道"

两个进程通信的模式：
  1. 建立连接（TCP）
  2. 发送数据
  3. 接收数据
  4. 关闭连接
""")

print("\n--- Socket 类型 ---")
print("""
1. TCP Socket (SOCK_STREAM)
   - 面向连接
   - 保证数据顺序和完整性
   - 速度略慢，可靠性高

2. UDP Socket (SOCK_DGRAM)
   - 无连接
   - 不保证数据顺序
   - 速度快，用于实时应用

3. Raw Socket
   - 直接访问网络层
   - 很少使用
""")

print("\n=== 2. TCP Socket 基础 ===\n")

print("--- TCP 服务端示例 ---")
print("""
import socket

# 创建 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定端口
server_socket.bind(('localhost', 5000))

# 监听连接（最多5个等待连接）
server_socket.listen(5)
print("服务器启动，监听 localhost:5000")

# 接受连接
while True:
    client_socket, client_address = server_socket.accept()
    print(f"客户端连接: {client_address}")
    
    # 接收数据
    data = client_socket.recv(1024)
    print(f"接收数据: {data.decode()}")
    
    # 发送数据
    response = "Hello from server"
    client_socket.send(response.encode())
    
    # 关闭连接
    client_socket.close()

server_socket.close()
""")

print("\n--- TCP 客户端示例 ---")
print("""
import socket

# 创建 Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
client_socket.connect(('localhost', 5000))

# 发送数据
message = "Hello from client"
client_socket.send(message.encode())

# 接收数据
response = client_socket.recv(1024)
print(f"收到响应: {response.decode()}")

# 关闭连接
client_socket.close()
""")

print("\n=== 3. UDP Socket 基础 ===\n")

print("--- UDP 服务端示例 ---")
print("""
import socket

# 创建 UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定端口
server_socket.bind(('localhost', 5001))
print("UDP 服务器启动，监听 localhost:5001")

# 接收数据
while True:
    # recvfrom 返回数据和发送方地址
    data, client_address = server_socket.recvfrom(1024)
    print(f"收到数据: {data.decode()}, 来自: {client_address}")
    
    # 发送响应
    response = "UDP response"
    server_socket.sendto(response.encode(), client_address)

server_socket.close()
""")

print("\n--- UDP 客户端示例 ---")
print("""
import socket

# 创建 UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送数据（不需要连接）
message = "Hello from UDP client"
client_socket.sendto(message.encode(), ('localhost', 5001))

# 接收响应
response, server_address = client_socket.recvfrom(1024)
print(f"收到: {response.decode()}, 来自: {server_address}")

client_socket.close()
""")

print("\n=== 4. Socket 编程的关键点 ===\n")

print("--- 数据发送与接收 ---")
print("""
发送：
  socket.send(data)          # 发送字节
  socket.sendto(data, addr)  # UDP 发送到指定地址
  socket.sendall(data)       # 确保全部发送

接收：
  socket.recv(bufsize)       # TCP 接收数据
  socket.recvfrom(bufsize)   # UDP 接收数据和地址
""")

print("\n--- 常见的 Socket 选项 ---")
print("""
socket.setsockopt(level, optname, value)

常用选项：
  SO_REUSEADDR              # 快速重启服务器
  SO_KEEPALIVE              # TCP 心跳包
  TCP_NODELAY               # 禁用 Nagle 算法
  SO_RCVTIMEO/SO_SNDTIMEO   # 接收/发送超时
""")

print("\n=== 5. 实用 Socket 工具 ===\n")

class SimpleSocketServer:
    """简单的 Socket 服务器"""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
    
    def start(self):
        """启动服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"服务器启动: {self.host}:{self.port}")
    
    def accept_connection(self):
        """接受连接"""
        if self.socket:
            client_socket, client_address = self.socket.accept()
            print(f"新连接: {client_address}")
            return client_socket, client_address
        return None, None
    
    def close(self):
        """关闭服务器"""
        if self.socket:
            self.socket.close()
            print("服务器已关闭")

class SimpleSocketClient:
    """简单的 Socket 客户端"""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """连接到服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"已连接到: {self.host}:{self.port}")
    
    def send(self, data):
        """发送数据"""
        if isinstance(data, str):
            data = data.encode()
        self.socket.send(data)
    
    def recv(self, bufsize=1024):
        """接收数据"""
        return self.socket.recv(bufsize)
    
    def close(self):
        """关闭连接"""
        if self.socket:
            self.socket.close()
            print("连接已关闭")

print("--- 工具类使用示例 ---")
print("(实际运行需要同时运行服务端和客户端)")

# 服务端示例（伪代码）
# server = SimpleSocketServer('0.0.0.0', 5000)
# server.start()
# client_socket, client_addr = server.accept_connection()
# data = client_socket.recv(1024)
# print(f"收到: {data.decode()}")
# server.close()

# 客户端示例（伪代码）
# client = SimpleSocketClient('localhost', 5000)
# client.connect()
# client.send("Hello Server")
# response = client.recv()
# print(f"收到: {response.decode()}")
# client.close()

print("\n=== 6. TCP vs UDP 对比 ===\n")

print("""
特性              TCP           UDP
-------------------------------------------
连接              需要建立        无需建立
可靠性            高             低
顺序保证          有             无
速度              慢             快
开销              大             小
应用场景          文件传输      实时通话
                  邮件           游戏
                  Web            DNS
                                语音
""")

print("\n=== 7. Socket 错误处理 ===\n")

print("""
常见错误：
  ConnectionRefused     # 连接被拒绝
  TimeoutError         # 连接超时
  BrokenPipeError      # 管道破裂（对端断开）
  OSError              # 操作系统错误

处理方式：
  try:
      socket.connect(address)
  except ConnectionRefusedError:
      print("连接被拒绝")
  except socket.timeout:
      print("连接超时")
  except Exception as e:
      print(f"错误: {e}")
""")
