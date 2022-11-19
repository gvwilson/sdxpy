from struct import unpack

def unpack_string(buffer):
   header, body = buffer[:4], buffer[4:]
   length = unpack("i", header)[0]
   format = f"{length}s"
   result = unpack(format, body)[0]
   return str(result, "utf-8")

if __name__ == "__main__":
    # [omit]
    from pack_str import pack_string
    buffer = pack_string("hello")
    # [/omit]
    result = unpack_string(buffer)
    print(result)
