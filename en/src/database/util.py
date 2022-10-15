import struct

USERNAME_LEN = 16
FORMAT = f"!i{USERNAME_LEN}si"
PAGE_SIZE = 1024


class DBError(Exception):
    def __init__(self, message):
        self.message = message


def record_pack(userid, username, timestamp):
    username = bytes(username, "utf-8")
    assert len(username) <= USERNAME_LEN
    return struct.pack(FORMAT, userid, username, timestamp)


def record_unpack(buf):
    userid, username, timestamp = struct.unpack(FORMAT, buf)
    username = str(username.split(b"\0", 1)[0], "utf-8")
    return userid, username, timestamp


def record_size():
    return struct.calcsize(FORMAT)
