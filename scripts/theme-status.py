#!/usr/bin/env python3
"""Report the currently applied preset and whether generated files are consistent.

Read-only: never modifies files. Output is concise and suitable for issue reports.

Usage:
  python scripts/theme-status.py            # infer the applied preset
  python scripts/theme-status.py <preset>   # check a specific preset
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import theme_lib  # noqa: E402

OUTPUTS = theme_lib.OUTPUTS


def load_palette(preset_path: Path) -> dict:
    return theme_lib.load_palette(preset_path)


def render(source: str, palette: dict) -> str:
    return theme_lib.render(source, palette)


def file_state(output_path: Path, expected: str) -> str:
    if not output_path.exists():
        return "missing"
    try:
        current = output_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return "unreadable"
    return "matches" if current == expected else "drift"


def infer_preset() -> tuple[Path | None, list[tuple[Path, str]]]:
    """Find which preset (if any) currently matches the generated files.

    Returns (preset_path_or_None, per-file states for that preset).
    """
    themes = sorted((ROOT / "themes").glob("*.json"))
    for preset in themes:
        try:
            palette = load_palette(preset)
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, ValueError):
            continue
        all_match = True
        states = []
        for template_path, output_path in OUTPUTS:
            try:
                source = template_path.read_text(encoding="utf-8")
                expected = render(source, palette)
            except (OSError, UnicodeError, ValueError):
                states.append((output_path, "unreadable"))
                all_match = False
                continue
            state = file_state(output_path, expected)
            states.append((output_path, state))
            if state != "matches":
                all_match = False
        if all_match:
            return preset, states
    return None, []


def check_specific(preset_path: Path) -> int:
    try:
        palette = load_palette(preset_path)
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"status: cannot load preset {preset_path.name}: {error}", file=sys.stderr)
        return 1

    print(f"Preset: {preset_path.name}")
    mismatches = []
    for template_path, output_path in OUTPUTS:
        relative = output_path.relative_to(ROOT)
        try:
            source = template_path.read_text(encoding="utf-8")
            expected = render(source, palette)
        except (OSError, UnicodeError, ValueError) as error:
            print(f"  UNREADABLE  {relative}  ({error})")
            mismatches.append(relative)
            continue
        state = file_state(output_path, expected)
        label = {"matches": "MATCHES   ", "drift": "DRIFT     ",
                 "missing": "MISSING   ", "unreadable": "UNREADABLE"}[state]
        print(f"  {label}{relative}")
        if state != "matches":
            mismatches.append(relative)

    if mismatches:
        print("\nGenerated files do not match the selected preset.")
        return 1
    print("\nAll generated files match the selected preset.")
    return 0


def infer() -> int:
    preset, states = infer_preset()
    if preset is None:
        print("Preset: (none fully matches the generated files)")
        print("No bundled preset fully matches the current generated files.")
        print("Either no preset was applied, or generated files drifted.")
        return 1

    print(f"Preset: {preset.name}  (inferred)")
    for output_path, state in states:
        relative = output_path.relative_to(ROOT)
        label = {"matches": "MATCHES   ", "drift": "DRIFT     ",
                 "missing": "MISSING   ", "unreadable": "UNREADABLE"}[state]
        print(f"  {label}{relative}")
    print(f"\nInferred from {preset.name}; all checked files match.")
    return 0


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] != "-h" and sys.argv[1] != "--help":
        preset = Path(sys.argv[1])
        if not preset.is_absolute():
            preset = ROOT / preset
        return check_specific(preset)
    if len(sys.argv) != 1:
        print(__doc__, file=sys.stderr)
        return 1
    return infer()


if __name__ == "__main__":
    raise SystemExit(main())
