from http import HTTPStatus

from testable_server import ApplicationRequestHandler
from mock_handler import MockRequestHandler

# [combined]
class MockHandler(
        MockRequestHandler,
        ApplicationRequestHandler
):
    pass
# [/combined]

def test_nonexistent_path():
    handler = MockHandler("/nonexistent.txt")
    handler.do_GET()
    assert handler.status == int(HTTPStatus.NOT_FOUND)
    assert "Content-Type" in handler.headers
    assert "Content-Length" in handler.headers

# [example]
def test_existing_path(fs):
    content_str = "actual"
    content_bytes = bytes(content_str, "utf-8")
    fs.create_file("/actual.txt", contents=content_str)
    handler = MockHandler("/actual.txt")
    handler.do_GET()
    assert handler.status == int(HTTPStatus.OK)
    assert handler.headers["Content-Type"] == \
        ["text/html; charset=utf-8"]
    assert handler.headers["Content-Length"] == \
        [str(len(content_bytes))]
    assert handler.wfile.getvalue() == content_bytes
# [/example]
