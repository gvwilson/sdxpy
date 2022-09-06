from struct import pack

print(pack("3i", 1, 2, 3))
print(pack("5s", bytes("hello", "utf-8")))
print(pack("5s", bytes("a longer string", "utf-8")))
