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
CSS_URL = re.compile(r"url\(\s*(?:[\'\"]([^\'\"]*)[\'\"]|([^)]*))\s*\)", re.IGNORECASE)


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


def check_local_asset_references(stylesheets: list[Path]) -> None:
    """Ensure relative url(...) references resolve to files in the repository."""
    for stylesheet in stylesheets:
        source = stylesheet.read_text(encoding="utf-8")
        for match in CSS_URL.finditer(source):
            target = (match.group(1) or match.group(2) or "").strip()
            if (
                not target
                or target.startswith(("#", "/", "//"))
                or "{{" in target
                or target.startswith("var(")
                or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)
            ):
                continue

            target = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not target:
                continue
            resolved = (stylesheet.parent / target).resolve()
            if not resolved.is_file():
                report(stylesheet, f"local url() target does not exist: {target}")


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


# GTK3 and GTK4 expose the full semantic palette. GNOME Shell intentionally
# consumes only the tokens used by its stylesheet; keep that smaller surface
# explicit so adding a new shared token prompts a deliberate decision.
SHELL_INTENTIONALLY_UNUSED_TOKENS = {
    "inverse_on_surface",
    "inverse_primary",
    "inverse_surface",
    "on_error",
    "on_primary_fixed",
    "on_primary_fixed_variant",
    "on_secondary",
    "on_secondary_fixed",
    "on_secondary_fixed_variant",
    "on_tertiary",
    "on_tertiary_container",
    "on_tertiary_fixed",
    "on_tertiary_fixed_variant",
    "primary_fixed_dim",
    "scrim",
    "secondary_fixed",
    "secondary_fixed_dim",
    "shadow",
    "source_color",
    "surface",
    "surface_bright",
    "surface_container_lowest",
    "surface_dim",
    "surface_tint",
    "surface_variant",
    "tertiary",
    "tertiary_container",
    "tertiary_fixed",
    "tertiary_fixed_dim",
}


def check_semantic_token_parity() -> None:
    """Keep GTK3/GTK4 semantic tokens aligned and Shell exceptions explicit."""
    gtk3_path = ROOT / "gtk-3.0" / "colors-template.css"
    gtk4_path = ROOT / "gtk-4.0" / "colors-template.css"
    shell_path = ROOT / "gnome-shell" / "gnome-shell-template.css"

    try:
        gtk3_source = gtk3_path.read_text(encoding="utf-8")
        gtk4_source = gtk4_path.read_text(encoding="utf-8")
        shell_source = shell_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        report(ROOT / "scripts" / "check-theme.py", f"cannot read semantic color templates: {error}")
        return

    gtk3_tokens = set(re.findall(
        r"@define-color\s+([a-zA-Z0-9_-]+)\s+\{\{colors\.([a-zA-Z0-9_-]+)\.default\.hex\}\}",
        gtk3_source,
    ))
    gtk4_tokens = set(re.findall(
        r"--([a-zA-Z0-9_-]+)\s*:\s*\{\{colors\.([a-zA-Z0-9_-]+)\.default\.hex\}\}",
        gtk4_source,
    ))
    # The CSS variable / GTK color name and JSON token should match exactly.
    gtk3_names = {name for name, token in gtk3_tokens if name == token}
    gtk4_names = {name for name, token in gtk4_tokens if name == token}
    gtk3_json_tokens = {token for name, token in gtk3_tokens}
    gtk4_json_tokens = {token for name, token in gtk4_tokens}
    shell_tokens = set(re.findall(
        r"\{\{colors\.([a-zA-Z0-9_-]+)\.default\.",
        shell_source,
    ))

    if gtk3_names != gtk3_json_tokens:
        report(gtk3_path, "semantic GTK3 color names must match their JSON token names")
    if gtk4_names != gtk4_json_tokens:
        report(gtk4_path, "semantic GTK4 variable names must match their JSON token names")

    missing_gtk4 = sorted(gtk3_json_tokens - gtk4_json_tokens)
    missing_gtk3 = sorted(gtk4_json_tokens - gtk3_json_tokens)
    if missing_gtk4:
        report(gtk4_path, "missing GTK3 semantic tokens: " + ", ".join(missing_gtk4))
    if missing_gtk3:
        report(gtk3_path, "missing GTK4 semantic tokens: " + ", ".join(missing_gtk3))

    all_tokens = gtk3_json_tokens | gtk4_json_tokens
    unknown_shell = sorted(shell_tokens - all_tokens)
    if unknown_shell:
        report(shell_path, "uses semantic tokens absent from GTK3/GTK4: " + ", ".join(unknown_shell))

    unaccounted_shell_tokens = sorted(all_tokens - shell_tokens - SHELL_INTENTIONALLY_UNUSED_TOKENS)
    stale_exceptions = sorted(SHELL_INTENTIONALLY_UNUSED_TOKENS - (all_tokens - shell_tokens))
    if unaccounted_shell_tokens:
        report(shell_path, "semantic tokens need Shell use or an explicit exception: " + ", ".join(unaccounted_shell_tokens))
    if stale_exceptions:
        report(shell_path, "remove obsolete Shell token exceptions: " + ", ".join(stale_exceptions))

    for path in sorted((ROOT / "themes").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            # The existing preset validator reports JSON errors separately.
            continue
        colors = data.get("colors")
        if not isinstance(colors, dict):
            continue
        missing = sorted(all_tokens - set(colors))
        if missing:
            report(path, "missing shared semantic tokens: " + ", ".join(missing))

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
    check_local_asset_references(stylesheets)
    check_theme_presets()
    check_semantic_token_parity()
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
