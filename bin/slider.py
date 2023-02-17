import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_ADDRESS = ("", 4000)
SETTINGS = None


def get_settings():
    settings = {
        "template": None,
        "res": None,
        "content": None,
    }

    for arg in sys.argv[1:]:
        key, value = arg.split("=")
        settings[key] = value

    with open(settings["template"], "r") as reader:
        template = reader.read()
        settings["template"] = template.replace("@res", settings["res"])

    return settings


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(SETTINGS["content"], "r") as reader:
            content = reader.read()
        page = SETTINGS["template"].replace("@content", content)
        page = bytes(page, "utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


if __name__ == "__main__":
    SETTINGS = get_settings()
    server = HTTPServer(SERVER_ADDRESS, RequestHandler)
    server.serve_forever()
