# 第4月第3-4周学习代码示例
# 字节流处理、struct高级用法、简单协议实验、粘包/拆包处理

import struct
import io

print("=== 1. 字节流处理高级技巧 ===\n")

class ByteStream:
    """字节流处理工具"""
    
    def __init__(self, data=None):
        if data is None:
            self.buffer = io.BytesIO()
        else:
            self.buffer = io.BytesIO(data)
    
    def read(self, n):
        """读取 n 个字节"""
        return self.buffer.read(n)
    
    def write(self, data):
        """写入字节"""
        self.buffer.write(data)
    
    def read_struct(self, fmt):
        """按格式读取结构"""
        size = struct.calcsize(fmt)
        data = self.buffer.read(size)
        return struct.unpack(fmt, data)
    
    def write_struct(self, fmt, *args):
        """按格式写入结构"""
        self.buffer.write(struct.pack(fmt, *args))
    
    def read_string(self, length):
        """读取字符串"""
        data = self.buffer.read(length)
        return data.decode('utf-8')
    
    def write_string(self, s):
        """写入字符串"""
        self.buffer.write(s.encode('utf-8'))
    
    def read_cstring(self):
        """读取 C 格式字符串（以 \\0 结尾）"""
        chars = []
        while True:
            ch = self.buffer.read(1)
            if not ch or ch == b'\\x00':
                break
            chars.append(ch)
        return b''.join(chars).decode('utf-8')
    
    def get_data(self):
        """获取所有数据"""
        return self.buffer.getvalue()
    
    def seek(self, pos):
        """移动指针"""
        self.buffer.seek(pos)

print("--- 字节流示例 ---")
stream = ByteStream()

# 写入不同类型的数据
stream.write_struct('!BHI', 1, 80, 192168001)  # cmd, port, ip
stream.write_string("Hello")

# 读取数据
stream.seek(0)
cmd, port, ip = stream.read_struct('!BHI')
msg = stream.read_string(5)

print(f"读取结果: cmd={cmd}, port={port}, ip={ip}, msg={msg}")

print("\n=== 2. 消息帧处理 ===\n")

class FrameProcessor:
    """消息帧处理器"""
    
    def __init__(self):
        self.buffer = b''
    
    def add_data(self, data):
        """添加接收到的数据"""
        self.buffer += data
    
    def extract_frame(self):
        """提取一个完整的帧"""
        if len(self.buffer) < 5:  # 最小帧大小：命令(1) + 长度(2) + 类型(1) + 数据(0+)
            return None
        
        # 解析帧头 [长度(2字节)] [命令(1字节)] [类型(1字节)] [数据]
        length = struct.unpack('!H', self.buffer[:2])[0]
        
        total_size = 2 + length  # 长度字段 + 其他字段
        
        if len(self.buffer) < total_size:
            return None  # 数据不完整
        
        frame = self.buffer[:total_size]
        self.buffer = self.buffer[total_size:]
        
        return frame
    
    def parse_frame(self, frame):
        """解析帧"""
        if len(frame) < 4:
            return None
        
        length, cmd, frame_type = struct.unpack('!HBB', frame[:4])
        data = frame[4:]
        
        return {
            'length': length,
            'cmd': cmd,
            'type': frame_type,
            'data': data
        }

print("--- 帧处理示例 ---")
processor = FrameProcessor()

# 模拟接收粘在一起的多个帧
# 帧1: 长度=5, 命令=1, 类型=2, 数据=abc
frame1 = struct.pack('!HBB', 5, 1, 2) + b'abc'
# 帧2: 长度=4, 命令=3, 类型=4, 数据=def
frame2 = struct.pack('!HBB', 4, 3, 4) + b'def'

# 同时接收两个帧
processor.add_data(frame1 + frame2)

# 逐个提取帧
while True:
    frame = processor.extract_frame()
    if not frame:
        break
    
    parsed = processor.parse_frame(frame)
    print(f"帧: {parsed}")

print("\n=== 3. 二进制格式转换 ===\n")

class BinaryFormat:
    """二进制格式转换工具"""
    
    @staticmethod
    def hex_to_bytes(hex_str):
        """十六进制字符串转字节"""
        return bytes.fromhex(hex_str)
    
    @staticmethod
    def bytes_to_hex(data):
        """字节转十六进制字符串"""
        return data.hex()
    
    @staticmethod
    def bin_to_bytes(bin_str):
        """二进制字符串转字节"""
        return int(bin_str, 2).to_bytes((len(bin_str) + 7) // 8, 'big')
    
    @staticmethod
    def bytes_to_bin(data):
        """字节转二进制字符串"""
        return bin(int.from_bytes(data, 'big'))[2:].zfill(len(data) * 8)
    
    @staticmethod
    def format_bytes(data, fmt='hex'):
        """格式化字节显示"""
        if fmt == 'hex':
            return ' '.join(f'{b:02x}' for b in data)
        elif fmt == 'bin':
            return ' '.join(f'{b:08b}' for b in data)
        elif fmt == 'dec':
            return ' '.join(str(b) for b in data)

print("--- 二进制转换示例 ---")
data = b'Hello'

print(f"原始: {data}")
print(f"Hex: {BinaryFormat.bytes_to_hex(data)}")
print(f"Bin: {BinaryFormat.format_bytes(data, 'bin')[:20]}...")
print(f"Dec: {BinaryFormat.format_bytes(data, 'dec')}")

print("\n=== 4. 自定义协议实现 ===\n")

class CustomProtocol:
    """自定义应用协议"""
    
    # 消息类型
    TYPE_REQUEST = 0x01
    TYPE_RESPONSE = 0x02
    TYPE_ERROR = 0x03
    
    # 命令
    CMD_ECHO = 0x10
    CMD_GET = 0x11
    CMD_SET = 0x12
    
    class Message:
        def __init__(self, msg_type, cmd, seq, data=b''):
            self.msg_type = msg_type
            self.cmd = cmd
            self.seq = seq
            self.data = data
        
        def serialize(self):
            """序列化消息"""
            # [长度(2)] [类型(1)] [命令(1)] [序列(2)] [数据]
            length = 1 + 1 + 2 + len(self.data)
            header = struct.pack('!HBBB', length, self.msg_type, self.cmd, self.seq)
            return header + self.data
        
        @staticmethod
        def deserialize(data):
            """反序列化消息"""
            if len(data) < 6:
                return None
            
            length, msg_type, cmd, seq = struct.unpack('!HBBB', data[:6])
            payload = data[6:6+length-2]
            
            return CustomProtocol.Message(msg_type, cmd, seq, payload)

print("--- 协议使用示例 ---")

# 创建 ECHO 请求
msg = CustomProtocol.Message(
    CustomProtocol.TYPE_REQUEST,
    CustomProtocol.CMD_ECHO,
    seq=101,
    data=b'Hello Protocol'
)

serialized = msg.serialize()
print(f"序列化: {serialized.hex()}")

# 反序列化
restored = CustomProtocol.Message.deserialize(serialized)
print(f"反序列化: type={restored.msg_type}, cmd={restored.cmd}, seq={restored.seq}, data={restored.data}")

print("\n=== 5. 数据完整性验证 ===\n")

class MessageValidator:
    """消息验证器（使用校验和）"""
    
    @staticmethod
    def calculate_checksum(data):
        """计算简单校验和"""
        return sum(data) & 0xFF
    
    @staticmethod
    def calculate_crc32(data):
        """计算 CRC32 校验"""
        import zlib
        return zlib.crc32(data) & 0xFFFFFFFF
    
    @staticmethod
    def pack_with_checksum(data):
        """打包数据并添加校验和"""
        checksum = MessageValidator.calculate_checksum(data)
        return data + struct.pack('!B', checksum)
    
    @staticmethod
    def verify_checksum(data):
        """验证校验和"""
        if len(data) < 1:
            return False, None
        
        payload = data[:-1]
        checksum = data[-1]
        calculated = MessageValidator.calculate_checksum(payload)
        
        return calculated == checksum, payload

print("--- 校验和示例 ---")
data = b'Test Data'
packed = MessageValidator.pack_with_checksum(data)
print(f"添加校验和: {packed.hex()}")

valid, payload = MessageValidator.verify_checksum(packed)
print(f"验证结果: valid={valid}, data={payload}")

# 修改数据后验证失败
corrupted = packed[:-2] + b'XX'
valid, payload = MessageValidator.verify_checksum(corrupted)
print(f"损坏数据验证: valid={valid}")

print("\n=== 6. 协议调试工具 ===\n")

class ProtocolDebugger:
    """协议调试工具"""
    
    @staticmethod
    def hexdump(data, width=16):
        """十六进制转储"""
        print("Offset   Hex                              ASCII")
        print("-" * 60)
        
        for i in range(0, len(data), width):
            chunk = data[i:i+width]
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f"{i:08x}  {hex_str:<48} {ascii_str}")
    
    @staticmethod
    def analyze_message(data):
        """分析消息结构"""
        stream = ByteStream(data)
        
        print(f"总长度: {len(data)} 字节")
        print(f"Hex: {data.hex()}")
        print("\n字节分析:")
        for i, b in enumerate(data):
            print(f"  [{i:3d}] 0x{b:02x} ({b:3d}) '{chr(b) if 32 <= b < 127 else '.'}'")

print("--- 调试示例 ---")
test_data = b'\\x00\\x05\\x01\\x02\\x65Hello'
ProtocolDebugger.hexdump(test_data)
