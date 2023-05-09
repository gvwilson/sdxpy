"""Display slides during development."""

import argparse
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

import yaml

# Known MIME types
MIME_TYPES = {
    "css": "text/css",
    "html": "text/html",
    "js": "text/javascript",
    "svg": "image/svg+xml",
}

# Filled in later
OPTIONS = None
LINKS = None
RESOURCES = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project", required=True, help="Root directory of Git project"
    )
    parser.add_argument("--chapter", required=True, help="Root directory of chapter")
    return parser.parse_args()


def read_links():
    path = f"{OPTIONS.project}/info/links.yml"
    with open(path, "r") as reader:
        entries = yaml.load(reader, Loader=yaml.FullLoader)
        return "\n".join(f"[{e['key']}]: {e['url']}" for e in entries)


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            content, mime_type = self.do_slides()
        else:
            content, mime_type = self.do_other()
        self.send_response(200)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Content-Type", mime_type)
        self.end_headers()
        self.wfile.write(content)

    def do_other(self):
        if self.path.startswith("/@res"):
            self.path = self.path.replace("/@res", RESOURCES)
        elif self.path.startswith("/"):
            self.path = f"{OPTIONS.project}/src/{OPTIONS.chapter}{self.path}"
        with open(self.path, "rb") as reader:
            content = reader.read()
        return content, self.guess_mime_type()

    def do_slides(self):
        with open(f"{OPTIONS.project}/lib/mccole/slides.html", "r") as reader:
            template = reader.read()
        with open("./slides/index.html", "r") as reader:
            slides = reader.read()
            slides = slides.split("---", maxsplit=2)[-1]
        page = template.replace("@content", slides + "\n\n" + LINKS)
        page = bytes(page, "utf-8")
        return page, "text/html"

    def guess_mime_type(self):
        ext = self.path.split(".")[-1]
        return MIME_TYPES.get(ext, "unknown")


if __name__ == "__main__":
    OPTIONS = parse_args()
    LINKS = read_links()
    RESOURCES = f"{OPTIONS.project}/lib/mccole/resources"
    os.chdir(f"{OPTIONS.project}/src/{OPTIONS.chapter}")
    server = HTTPServer(("", 4000), RequestHandler)
    server.serve_forever()
