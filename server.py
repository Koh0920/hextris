from __future__ import annotations

import http.server
import json
import os
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
UPSTREAM_COMMIT = "3f4847dc8fd7dab3d1c87e6324b9159d92fbd396"


class CapsuleHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        request_url = urlsplit(self.path)
        path = request_url.path
        if path == "/health":
            self._json({"status": "ok"})
            return
        if path == "/__ato/state":
            required = ["index.html", "js/main.js", "js/initialization.js"]
            self._json(
                {
                    "app": "hextris",
                    "upstream_commit": UPSTREAM_COMMIT,
                    "demo_mode": True,
                    "assets_ready": all((ROOT / item).is_file() for item in required),
                    "runtime_downloads": False,
                }
            )
            return
        if path == "/" and request_url.query != "ato-demo=1":
            self.send_response(302)
            self.send_header("Location", "/?ato-demo=1")
            self.end_headers()
            return
        super().do_GET()

    def _json(self, payload: dict[str, object]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


port = int(os.environ.get("ATO_PORT", "8080"))
http.server.ThreadingHTTPServer(("0.0.0.0", port), CapsuleHandler).serve_forever()
