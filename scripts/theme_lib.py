"""Shared rendering helpers for apply-theme / theme-status / theme-doctor.

Kept dependency-free (stdlib only) so the doctor and status tools work without
any extra packages. The CLI entry points live in their own scripts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOKEN = re.compile(
    r"\{\{\s*colors\.([a-zA-Z0-9_-]+)\.default\."
    r"(hex|color|red|green|blue)\s*\}\}"
)
UNRESOLVED = re.compile(r"\{\{.*?\}\}", re.DOTALL)

OUTPUTS = (
    (ROOT / "gtk-3.0/colors-template.css", ROOT / "gtk-3.0/colors.css"),
    (ROOT / "gtk-4.0/colors-template.css", ROOT / "gtk-4.0/colors.css"),
    (
        ROOT / "gnome-shell/gnome-shell-template.css",
        ROOT / "gnome-shell/gnome-shell.css",
    ),
)


def color_value(palette: dict, name: str, channel: str) -> str:
    try:
        color = palette[name]["default"]["color"]
    except (KeyError, TypeError) as error:
        raise ValueError(f"preset is missing colors.{name}.default.color") from error

    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError(f"colors.{name}.default.color must be a #RRGGBB value")

    if channel in {"hex", "color"}:
        return color

    rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    return str(rgb[{"red": 0, "green": 1, "blue": 2}[channel]])


def render(source: str, palette: dict, template_path: Path | None = None) -> str:
    def replace(match: re.Match[str]) -> str:
        return color_value(palette, match.group(1), match.group(2))

    rendered = TOKEN.sub(replace, source)
    unresolved = UNRESOLVED.search(rendered)
    if unresolved:
        raise ValueError(
            f"unsupported or unresolved template token {unresolved.group(0)!r}"
        )
    return rendered


def load_palette(preset_path: Path) -> dict:
    data = json.loads(preset_path.read_text(encoding="utf-8"))
    palette = data["colors"]
    if not isinstance(palette, dict):
        raise ValueError(f"{preset_path.name}: preset must contain a 'colors' object")
    return palette
