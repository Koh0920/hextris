from __future__ import annotations

import json
import sys
import urllib.request


base_url = sys.argv[1].rstrip("/")
with urllib.request.urlopen(f"{base_url}/__ato/state", timeout=5) as response:
    state = json.load(response)

assert state["app"] == "hextris"
assert state["upstream_commit"] == "3f4847dc8fd7dab3d1c87e6324b9159d92fbd396"
assert state["demo_mode"] is True
assert state["assets_ready"] is True
assert state["runtime_downloads"] is False
