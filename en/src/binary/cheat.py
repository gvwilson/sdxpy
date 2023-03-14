import struct

text = "abcd"
temp = struct.pack("4s", bytes(text, "utf-8"))
num = struct.unpack("i", temp)[0]
print(f"result: {num} (0x{num:x})")
