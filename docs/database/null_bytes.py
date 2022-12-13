import struct

FORMAT = "8s"

original = "test"
buf = bytes(original, "utf-8")

packed = struct.pack(FORMAT, buf)
print("packed data", repr(packed))

unpacked = struct.unpack(FORMAT, packed)[0]
print("unpacked data", repr(str(unpacked)))

final = str(unpacked, "utf-8")
print("final data", repr(final))
