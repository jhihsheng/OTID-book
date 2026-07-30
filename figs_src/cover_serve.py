"""Serve the cover preview over HTTP for tunnel viewing (port 8080).

Run:  python3 figs_src/cover_serve.py
Serves the scratchpad 'serve' directory on 0.0.0.0:8080. Ctrl-C to stop.
"""
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler

DIR = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad/serve"

handler = functools.partial(SimpleHTTPRequestHandler, directory=DIR)
srv = HTTPServer(("0.0.0.0", 8080), handler)
print("serving", DIR, "on http://0.0.0.0:8080")
srv.serve_forever()
