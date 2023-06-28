from struct import pack

# [pack]
def pack_string(as_string):
    as_bytes = bytes(as_string, "utf-8")
    header = pack("i", len(as_bytes))
    format = f"{len(as_bytes)}s"
    body = pack(format, as_bytes)
    return header + body
# [/pack]

# [main]
if __name__ == "__main__":
    result = pack_string("hello!")
    print(repr(result))
# [/main]
