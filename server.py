from __future__ import annotations

import http.server
import json
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
UPSTREAM_COMMIT = "3f4847dc8fd7dab3d1c87e6324b9159d92fbd396"


class DeterministicStaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        if urlsplit(self.path).path == "/__ato/health":
            body = json.dumps(
                {
                    "status": "ok",
                    "app": "hextris",
                    "upstream_commit": UPSTREAM_COMMIT,
                    "external_runtime_dependencies": False,
                },
                separators=(",", ":"),
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def send_header(self, keyword: str, value: str) -> None:
        if keyword.lower() in {"date", "last-modified", "server"}:
            return
        super().send_header(keyword, value)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()


http.server.ThreadingHTTPServer(
    ("127.0.0.1", 38986), DeterministicStaticHandler
).serve_forever()
