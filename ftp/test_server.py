from logging_handler import LoggingHandler, BLOCK_SIZE

# mccole:request
class MockRequest:
    def __init__(self, message):
        self._message = message
        self._position = 0
        self._sent = []

    def recv(self, max_bytes):
        assert self._position <= len(self._message)
        top = min(len(self._message), self._position + BLOCK_SIZE)
        result = self._message[self._position:top]
        self._position = top
        return result

    def sendall(self, outgoing):
        self._sent.append(outgoing)
# mccole:/request

# mccole:handler
class MockHandler(LoggingHandler):
    def __init__(self, message):
        self.request = MockRequest(message)

    def debug(self, *args):
        pass
# mccole:/handler

# mccole:test
def test_short():
    msg = bytes("message", "utf-8")
    handler = MockHandler(msg)
    handler.handle()
    assert handler.request._sent == [bytes(f"{len(msg)}", "utf-8")]
# mccole:/test
