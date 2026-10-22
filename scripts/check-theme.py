#!/usr/bin/env python3
"""Validate theme CSS syntax, preset tokens, and generated-file placeholders."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import tinycss2

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
PLACEHOLDER = re.compile(r"\{\{.*?\}\}", re.DOTALL)


def report(path: Path, message: str) -> None:
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def check_stylesheet(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    # Template placeholders are intentionally not valid CSS tokens. Substitute
    # a valid color only for parsing; placeholder validation runs separately.
    source = PLACEHOLDER.sub("#000000", source)
    rules = tinycss2.parse_stylesheet(
        source, skip_comments=True, skip_whitespace=True
    )
    for rule in rules:
        if rule.type == "error":
            report(path, f"CSS parse error: {rule.message}")
            continue
        if rule.type == "qualified-rule":
            declarations = tinycss2.parse_declaration_list(
                rule.content, skip_comments=True, skip_whitespace=True
            )
            for declaration in declarations:
                if declaration.type == "error":
                    report(path, f"declaration parse error: {declaration.message}")


def check_theme_presets() -> None:
    colors_css = ROOT / "gtk-4.0" / "colors.css"
    source = colors_css.read_text(encoding="utf-8")
    available = set(re.findall(r"--([a-zA-Z0-9_-]+)\s*:", source))
    for path in sorted((ROOT / "themes").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            report(path, f"invalid JSON: {error}")
            continue

        colors = data.get("colors")
        if not isinstance(colors, dict):
            report(path, "expected a top-level 'colors' object")
            continue

        missing = sorted(set(colors) - available)
        if missing:
            report(path, "missing GTK4 CSS variables: " + ", ".join(missing))


def check_placeholders() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".css", ".scss"}:
            continue
        if "template" in path.name.lower():
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            report(path, f"cannot read stylesheet: {error}")
            continue
        if PLACEHOLDER.search(source):
            report(path, "unexpanded {{...}} template placeholder found")


def main() -> int:
    stylesheets = sorted(
        path for path in ROOT.rglob("*.css")
        if ".git" not in path.parts
    )
    for stylesheet in stylesheets:
        check_stylesheet(stylesheet)
    check_theme_presets()
    check_placeholders()

    if ERRORS:
        print("\n".join(f"ERROR: {error}" for error in ERRORS), file=sys.stderr)
        print(f"\n{len(ERRORS)} validation error(s).", file=sys.stderr)
        return 1

    print(
        f"Validated {len(stylesheets)} CSS files and "
        f"{len(list((ROOT / 'themes').glob('*.json')))} theme presets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
