import struct

# [exception]
class DBError(Exception):
    def __init__(self, message):
        self.message = message
# [/exception]

MACHINE_LEN = 16
FORMAT = f"!i{MACHINE_LEN}si"
PAGE_SIZE = 1024

def record_pack(userid, machine, timestamp):
    machine = bytes(machine, "utf-8")
    assert len(machine) <= MACHINE_LEN
    return struct.pack(FORMAT, userid, machine, timestamp)

def record_unpack(buf):
    userid, machine, timestamp = struct.unpack(FORMAT, buf)
    machine = str(machine.split(b"\0", 1)[0], "utf-8")
    return userid, machine, timestamp

def record_size():
    return struct.calcsize(FORMAT)
