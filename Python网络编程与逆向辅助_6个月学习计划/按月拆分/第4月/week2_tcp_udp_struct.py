# 第4月第2-4周综合学习代码示例
# 覆盖TCP/UDP实操、字节流与struct、简单协议设计

import socket
import struct
import threading

print("=== 1. TCP 实操：客户端与服务端 ===\n")

class TCPServer:
    """完整的 TCP 服务端"""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
    
    def start(self):
        """启动服务器"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[服务器] 启动在 {self.host}:{self.port}")
    
    def handle_client(self, client_socket, client_address):
        """处理客户端连接"""
        print(f"[服务器] 客户端连接: {client_address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8')
                print(f"[服务器] 收到: {message}")
                
                # 回复消息
                response = f"服务器已收到: {message}"
                client_socket.send(response.encode('utf-8'))
        
        except Exception as e:
            print(f"[服务器] 错误: {e}")
        finally:
            client_socket.close()
            print(f"[服务器] 连接已关闭: {client_address}")
    
    def accept_connections(self):
        """接受连接"""
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                # 创建线程处理客户端
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                thread.daemon = True
                # thread.start()  # 实际运行时启用
        except KeyboardInterrupt:
            print("[服务器] 关闭")
        finally:
            self.server_socket.close()

class TCPClient:
    """完整的 TCP 客户端"""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """连接到服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"[客户端] 已连接到 {self.host}:{self.port}")
    
    def send_message(self, message):
        """发送消息"""
        self.socket.send(message.encode('utf-8'))
        print(f"[客户端] 发送: {message}")
        
        # 接收响应
        response = self.socket.recv(1024).decode('utf-8')
        print(f"[客户端] 收到: {response}")
    
    def close(self):
        """关闭连接"""
        self.socket.close()
        print("[客户端] 已断开连接")

print("--- TCP 示例（仅展示代码） ---")
print("实际运行需要分别启动 server 和 client")

print("\n=== 2. UDP 实操：发送与接收 ===\n")

class UDPServer:
    """UDP 服务端"""
    
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.socket = None
    
    def start(self):
        """启动 UDP 服务器"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"[UDP服务器] 启动在 {self.host}:{self.port}")
    
    def receive(self):
        """接收数据"""
        while True:
            data, client_address = self.socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"[UDP服务器] 收到来自 {client_address}: {message}")
            
            # 发送响应
            response = f"已收到: {message}"
            self.socket.sendto(response.encode('utf-8'), client_address)

class UDPClient:
    """UDP 客户端"""
    
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.socket = None
    
    def send_message(self, message):
        """发送消息"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.sendto(message.encode('utf-8'), (self.host, self.port))
        print(f"[UDP客户端] 发送到 {self.host}:{self.port}: {message}")
        
        # 接收响应
        response, server_address = self.socket.recvfrom(1024)
        print(f"[UDP客户端] 收到: {response.decode('utf-8')}")
        
        self.socket.close()

print("--- UDP 示例（仅展示代码） ---")
print("UDP 不需要建立连接，数据报可以单向发送")

print("\n=== 3. struct 模块：字节打包与解包 ===\n")

print("--- struct 基础 ---")
print("""
struct 模块用于处理字节序列和 Python 对象之间的转换
格式字符：
  'B' - unsigned char (1字节)
  'H' - unsigned short (2字节)
  'I' - unsigned int (4字节)
  'Q' - unsigned long long (8字节)
  'i' - signed int (4字节)
  'f' - float (4字节)
  'd' - double (8字节)
  's' - char[] (字节串)

字节序（Endianness）：
  '@' - 本机字节序
  '=' - 标准字节序
  '<' - 小端
  '>' - 大端
  '!' - 网络字节序（大端）
""")

print("\n--- struct 操作示例 ---")

# 打包数据
print("打包数据:")
data = struct.pack('!HHI', 80, 443, 192168001)
print(f"  格式: !HHI (big-endian, short, short, int)")
print(f"  数据: (80, 443, 192168001)")
print(f"  打包结果: {data.hex()}")

# 解包数据
print("\n解包数据:")
packed = b'\x00P\x01\xbb\x0c\xa8\x00\x01'
unpacked = struct.unpack('!HHI', packed)
print(f"  打包数据: {packed.hex()}")
print(f"  解包结果: {unpacked}")

# 结构化数据
print("\n--- 结构化消息（长度 + 类型 + 数据） ---")

class Message:
    """自定义消息类"""
    
    @staticmethod
    def pack_message(msg_type, data):
        """打包消息"""
        data_bytes = data.encode('utf-8') if isinstance(data, str) else data
        
        # 消息格式: [长度(4字节)] [类型(1字节)] [数据]
        length = len(data_bytes) + 1  # 包括类型字段
        header = struct.pack('!IB', length, msg_type)
        
        return header + data_bytes
    
    @staticmethod
    def unpack_message(data):
        """解包消息"""
        if len(data) < 5:
            return None, None, None
        
        # 解析头部
        length, msg_type = struct.unpack('!IB', data[:5])
        payload = data[5:5+length-1]
        
        return length, msg_type, payload.decode('utf-8')

print("消息打包示例:")
msg = Message.pack_message(1, "Hello, World!")
print(f"  消息: {msg.hex()}")

print("消息解包示例:")
length, msg_type, payload = Message.unpack_message(msg)
print(f"  长度: {length}, 类型: {msg_type}, 数据: {payload}")

print("\n=== 4. 简单协议设计 ===\n")

print("--- 二进制协议示例 ---")
print("""
协议结构：
┌─────────────────────────────────────────┐
│ 命令ID (1字节) │ 长度(H) │ 数据(可变) │
├─────────────────────────────────────────┤
│      B        │   H     │   DataLen  │
│    0-255      │ 0-65535 │   payload  │
└─────────────────────────────────────────┘

命令示例：
  0x01 - PING 请求
  0x02 - PING 响应
  0x03 - DATA 消息
  0x04 - ERROR 错误
""")

class SimpleProtocol:
    """简单的二进制协议"""
    
    # 命令 ID
    CMD_PING_REQ = 0x01
    CMD_PING_RSP = 0x02
    CMD_DATA = 0x03
    CMD_ERROR = 0x04
    
    @staticmethod
    def pack_ping():
        """打包 PING 请求"""
        return struct.pack('!BH', SimpleProtocol.CMD_PING_REQ, 0)
    
    @staticmethod
    def pack_data(data):
        """打包数据"""
        data_bytes = data.encode('utf-8') if isinstance(data, str) else data
        return struct.pack('!BH', SimpleProtocol.CMD_DATA, len(data_bytes)) + data_bytes
    
    @staticmethod
    def unpack_message(data):
        """解包消息"""
        if len(data) < 3:
            return None
        
        cmd, length = struct.unpack('!BH', data[:3])
        payload = data[3:3+length]
        
        return {
            'cmd': cmd,
            'length': length,
            'payload': payload
        }

print("--- 协议使用示例 ---")
ping_msg = SimpleProtocol.pack_ping()
print(f"PING 请求: {ping_msg.hex()}")

data_msg = SimpleProtocol.pack_data("Hello Protocol")
parsed = SimpleProtocol.unpack_message(data_msg)
print(f"DATA 消息: {data_msg.hex()}")
print(f"解析结果: {parsed}")

print("\n=== 5. 粘包与拆包 ===\n")

print("""
粘包/拆包问题：
  - 发送的多个消息可能会粘在一起
  - 一个消息可能分多次接收

解决方法：
  1. 固定长度：每条消息固定长度
  2. 长度字段：消息头包含数据长度
  3. 分隔符：用特殊符号分隔消息
  4. 状态机：根据协议状态解析

建议使用长度字段方案（本协议就是这样）
""")

print("\n=== 6. Socket 实用工具 ===\n")

class SocketUtils:
    """Socket 工具函数"""
    
    @staticmethod
    def send_all(sock, data):
        """确保全部数据发送"""
        total_sent = 0
        while total_sent < len(data):
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("socket 连接断开")
            total_sent += sent
    
    @staticmethod
    def recv_exactly(sock, n):
        """接收指定长度数据"""
        data = b''
        while len(data) < n:
            chunk = sock.recv(n - len(data))
            if not chunk:
                raise RuntimeError("socket 连接断开")
            data += chunk
        return data
    
    @staticmethod
    def recv_with_timeout(sock, bufsize, timeout):
        """带超时的接收"""
        sock.settimeout(timeout)
        try:
            return sock.recv(bufsize)
        except socket.timeout:
            raise TimeoutError("接收超时")
        finally:
            sock.settimeout(None)

print("Socket 工具已准备好，可用于 Socket 编程")
