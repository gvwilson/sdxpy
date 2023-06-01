from struct import calcsize

for format in ["4s", "3i4s5d"]:
    print(f"format '{format}' needs {calcsize(format)} bytes")
