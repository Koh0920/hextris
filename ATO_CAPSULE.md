# Hextris Ato Capsule

- Upstream: `Hextris/hextris`
- Pinned upstream commit: `3f4847dc8fd7dab3d1c87e6324b9159d92fbd396`
- License: GPL-3.0 (`LICENSE.md`)
- Surface: Web
- Authentication: none
- External services: disabled

The Ato overlay starts upstream Hextris directly in gameplay for every fresh
browser. It removes analytics, ads, the retired score endpoint, and remote font
loading so the accepted Snapshot does not depend on runtime network access.
The game mechanics are unchanged.

`tests/interactive.spec.js` verifies a rendered canvas, gameplay state, board
rotation, and a falling block from a fresh Playwright context. `verify.py`
provides the restored-guest `seal_at` check and validates the pinned asset set.
