#!/usr/bin/env python3
"""Generate a static gallery of every bundled preset.

No third-party dependencies: reads themes/*.json and writes
docs/preview/index.html with one card per preset.
"""

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRESETS = ROOT / "themes"
OUTPUT = ROOT / "docs" / "preview" / "index.html"

SWATCHES = (
    "primary",
    "on_primary",
    "surface",
    "on_surface",
    "secondary",
    "on_secondary",
    "error",
    "background",
)

CSS = """
:root { color-scheme: dark; }
body { margin: 0; padding: 24px; background: #101010; color: #e0e0e0;
       font: 13px/1.4 system-ui, sans-serif; }
h1 { font-size: 22px; margin: 0 0 6px; }
p.note { margin: 0 0 20px; color: #aaa; }
.grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(208px, 1fr)); }
.card { background: #1b1b1b; border: 1px solid #333; border-radius: 10px; padding: 10px; }
.name { font-weight: 600; word-break: break-all; margin-bottom: 2px; }
.meta { color: #999; font-size: 11px; margin-bottom: 8px; }
.swatches { display: grid; grid-template-columns: repeat(8, 1fr); gap: 3px; }
.sw { height: 26px; border-radius: 4px; border: 1px solid rgba(255,255,255,.12); }
.hex { font-family: ui-monospace, monospace; font-size: 10px; color: #888; margin-top: 6px;
       word-break: break-all; }
"""

HEADER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Material GNOME preset gallery</title>
<style>%s</style>
</head>
<body>
<h1>Material GNOME presets</h1>
<p class="note">%s presets. Apply one with <code>python scripts/apply-theme.py themes/&lt;filename&gt;</code>.</p>
<div class="grid">
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail if the checked-in gallery is out of date")
    args = parser.parse_args()

    cards = []
    for path in sorted(PRESETS.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        meta = data.get("_meta", {}) if isinstance(data, dict) else {}
        colors = data.get("colors", {}) if isinstance(data, dict) else {}
        swatches = []
        for token in SWATCHES:
            value = colors.get(token, {}).get("default", {}).get("color", "")
            if not (isinstance(value, str) and value.startswith("#")):
                value = "transparent"
            swatches.append(
                '<div class="sw" style="background:{}" title="{}: {}"></div>'.format(
                    html.escape(value), html.escape(token), html.escape(value)))
        hex_line = " ".join(
            colors.get(token, {}).get("default", {}).get("color", "")
            for token in SWATCHES[:4])
        cards.append(
            '<div class="card"><div class="name">{}</div>'
            '<div class="meta">{} · {}</div>'
            '<div class="swatches">{}</div>'
            '<div class="hex">{}</div></div>'.format(
                html.escape(path.name),
                html.escape(str(meta.get("name", ""))),
                html.escape(str(meta.get("variant", ""))),
                "".join(swatches),
                html.escape(hex_line)))

    content = HEADER % (CSS, len(cards)) + "\n".join(cards) + "\n</div>\n</body>\n</html>\n"

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            print("Gallery is out of date; run scripts/generate-preview.py", file=__import__("sys").stderr)
            return 1
        print("Gallery matches bundled presets.")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")
    print("Generated {} presets -> {} ({} bytes)".format(len(cards), OUTPUT, len(content)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
