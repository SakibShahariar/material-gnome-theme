#!/usr/bin/env python3
"""Render GTK3, GTK4, and GNOME Shell stylesheets from a theme JSON preset."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(
    r"\{\{\s*colors\.([a-zA-Z0-9_-]+)\.default\."
    r"(hex|color|red|green|blue)\s*\}\}"
)
UNRESOLVED = re.compile(r"\{\{.*?\}\}", re.DOTALL)


def color_value(palette: dict, name: str, channel: str) -> str:
    try:
        color = palette[name]["default"]["color"]
    except (KeyError, TypeError) as error:
        raise ValueError(f"preset is missing colors.{name}.default.color") from error

    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError(f"colors.{name}.default.color must be a #RRGGBB value")

    if channel in {"hex", "color"}:
        return color

    rgb = tuple(int(color[index:index + 2], 16) for index in (1, 3, 5))
    return str(rgb[{"red": 0, "green": 1, "blue": 2}[channel]])


def render(source: str, palette: dict, template_path: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        return color_value(palette, match.group(1), match.group(2))

    rendered = TOKEN.sub(replace, source)
    unresolved = UNRESOLVED.search(rendered)
    if unresolved:
        raise ValueError(
            f"unsupported or unresolved template token {unresolved.group(0)!r}"
        )
    return rendered


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as temporary:
            temporary.write(content)
            temporary_name = temporary.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply one JSON preset to GTK3, GTK4, and GNOME Shell."
    )
    parser.add_argument(
        "preset", type=Path,
        help="theme JSON file, for example themes/Aqua-Abyss.json",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run", action="store_true",
        help="render and validate outputs without changing any files",
    )
    mode.add_argument(
        "--check", action="store_true",
        help="fail if generated files differ from the selected preset",
    )
    args = parser.parse_args()

    preset_path = args.preset if args.preset.is_absolute() else ROOT / args.preset
    try:
        data = json.loads(preset_path.read_text(encoding="utf-8"))
        palette = data["colors"]
        if not isinstance(palette, dict):
            raise ValueError("preset must contain a 'colors' object")

        outputs = (
            (ROOT / "gtk-3.0/colors-template.css", ROOT / "gtk-3.0/colors.css"),
            (ROOT / "gtk-4.0/colors-template.css", ROOT / "gtk-4.0/colors.css"),
            (
                ROOT / "gnome-shell/gnome-shell-template.css",
                ROOT / "gnome-shell/gnome-shell.css",
            ),
        )
        rendered_outputs = []
        for template_path, output_path in outputs:
            source = template_path.read_text(encoding="utf-8")
            rendered_outputs.append(
                (output_path, render(source, palette, template_path))
            )
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"apply-theme: {error}", file=sys.stderr)
        return 1

    mismatches = []
    for output_path, content in rendered_outputs:
        relative_path = output_path.relative_to(ROOT)
        if args.check:
            try:
                current = output_path.read_text(encoding="utf-8")
            except OSError as error:
                print(f"apply-theme: cannot read {relative_path}: {error}", file=sys.stderr)
                mismatches.append(relative_path)
                continue
            if current != content:
                print(f"Out of date: {relative_path}", file=sys.stderr)
                mismatches.append(relative_path)
            else:
                print(f"Matches preset: {relative_path}")
        elif args.dry_run:
            print(f"Validated {relative_path} ({len(content)} bytes)")
        else:
            atomic_write(output_path, content)
            print(f"Updated {relative_path}")

    if mismatches:
        print("Generated files do not match the selected preset.", file=sys.stderr)
        return 1
    if args.dry_run:
        print("Dry run complete; no files were changed.")
    if args.check:
        print("Generated files match the selected preset.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
