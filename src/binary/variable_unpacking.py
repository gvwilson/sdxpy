from struct import unpack
from variable_packing import pack_string

# [main]
def unpack_string(buffer):
   header, body = buffer[:4], buffer[4:]
   length = unpack("i", header)[0]
   format = f"{length}s"
   result = unpack(format, body)[0]
   return str(result, "utf-8")

buffer = pack_string("hello!")
result = unpack_string(buffer)
print(result)
# [/main]
