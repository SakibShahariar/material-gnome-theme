#!/usr/bin/env python3
"""Diagnose common Material GNOME installation and color-generation problems.

Read-only: this command never modifies files. Each failed check prints an
actionable, paste-safe explanation (no secrets, no home path).

Usage:
  python scripts/theme-doctor.py
  python scripts/theme-doctor.py --preset themes/abyss-dark.json   # also check drift
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# Reuse the shared rendering helpers so drift checks agree with apply-theme.py.
sys.path.insert(0, str(SCRIPTS))
import theme_lib  # noqa: E402

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
RESULTS: list[tuple[str, str, str]] = []


def record(status: str, check: str, detail: str) -> None:
    RESULTS.append((status, check, detail))


# --------------------------------------------------------------------------
# Check 1: run check-theme.py's validations (CSS syntax, tokens, presets).
# --------------------------------------------------------------------------
def run_check_theme() -> None:
    try:
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "check-theme.py")],
            capture_output=True, text=True, timeout=300,
        )
        if proc.returncode == 0:
            summary = proc.stdout.strip().splitlines()
            record(PASS, "check-theme.py", summary[-1] if summary else "ok")
            return
        # Distinguish "a real validation error" from "missing dependency".
        combined = (proc.stderr or "") + (proc.stdout or "")
        if "ModuleNotFoundError" in combined:
            record(
                WARN, "check-theme.py",
                "skipped: tinycss2 is not installed in this environment.\n"
                "    Fix: pip install tinycss2 (CI installs it automatically).",
            )
            return
        first_lines = "\n    ".join(combined.strip().splitlines()[:20])
        record(
            FAIL, "check-theme.py",
            f"validation failed.\n    {first_lines}\n"
            "    Fix: resolve the reported CSS/token/preset errors, then re-run.",
        )
    except (OSError, subprocess.SubprocessError) as error:
        record(FAIL, "check-theme.py", f"could not run: {error}")


# --------------------------------------------------------------------------
# Check 2: theme JSON validity + required semantic tokens.
# --------------------------------------------------------------------------
REQUIRED_TOKENS = {
    "primary", "on_primary", "surface", "on_surface",
    "secondary", "on_secondary",
}


def check_presets() -> None:
    themes_dir = ROOT / "themes"
    if not themes_dir.is_dir():
        record(FAIL, "themes/", "directory not found.")
        return
    bad = []
    for path in sorted(themes_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            bad.append(f"{path.name} (invalid JSON: {error})")
            continue
        colors = data.get("colors", {})
        missing = sorted(REQUIRED_TOKENS - set(colors))
        if missing:
            bad.append(f"{path.name} (missing tokens: {', '.join(missing)})")
    if bad:
        detail = "\n    ".join(bad[:20])
        suffix = "\n    ..." if len(bad) > 20 else ""
        record(FAIL, "theme presets", f"{len(bad)} problem(s):\n    {detail}{suffix}")
    else:
        record(PASS, "theme presets", f"all {len(list(themes_dir.glob('*.json')))} presets valid")


# --------------------------------------------------------------------------
# Check 3: CSS/template syntax + unresolved placeholders (quick, no tinycss2).
# --------------------------------------------------------------------------
PLACEHOLDER = re.compile(r"\{\{.*?\}\}", re.DOTALL)


def check_placeholders() -> None:
    offenders = []
    for path in ROOT.rglob("*.css"):
        # Template directories (e.g. gnome-shell/layout-templates/) intentionally
        # contain matugen placeholders, just like *-template.css files.
        if (".git" in path.parts
                or "template" in path.name.lower()
                or "template" in str(path.relative_to(ROOT).parent).lower()):
            continue
        try:
            if PLACEHOLDER.search(path.read_text(encoding="utf-8")):
                offenders.append(path.relative_to(ROOT).as_posix())
        except (OSError, UnicodeError):
            continue
    if offenders:
        record(FAIL, "template placeholders",
               f"unexpanded {{...}} in: {', '.join(offenders[:10])}")
    else:
        record(PASS, "template placeholders", "no unresolved {{...}} in generated CSS")


# --------------------------------------------------------------------------
# Check 4: GTK4 colors.css symlink/import availability.
# --------------------------------------------------------------------------
def check_gtk4_symlink() -> None:
    config = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    link = config / "gtk-4.0" / "colors.css"
    if link.is_symlink():
        target = link.resolve()
        if target.exists():
            record(PASS, "GTK4 colors.css symlink", "present and resolvable")
        else:
            record(FAIL, "GTK4 colors.css symlink",
                   "broken symlink. Fix: re-run ./install.sh (or --force).")
    else:
        record(WARN, "GTK4 colors.css symlink",
               "not installed yet (run ./install.sh). Not a problem if you have not installed.")


# --------------------------------------------------------------------------
# Check 5: installed theme path + GNOME Shell version compatibility.
# --------------------------------------------------------------------------
def check_install_and_shell() -> None:
    installed = Path.home() / ".themes" / "Material-Gnome"
    if installed.is_dir():
        record(PASS, "installed theme", f"found at ~/.themes/Material-Gnome")
    else:
        record(WARN, "installed theme",
               "not installed. Fix: run ./install.sh from the repo.")

    # Detect running GNOME Shell version if possible (best-effort, read-only).
    shell_version = None
    for cmd in (
        ["gdbus", "call", "--session", "--dest", "org.gnome.Shell",
         "--object-path", "/org/gnome/Shell", "--method",
         "org.freedesktop.Dbus.Properties.Get", "org.gnome.Shell", "Version"],
    ):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            m = re.search(r"'(\d+\.\d+)'", out.stdout)
            if m:
                shell_version = m.group(1)
                break
        except (OSError, subprocess.SubprocessError):
            continue
    if shell_version:
        major = int(shell_version.split(".")[0])
        supported = 49 <= major <= 51
        if supported:
            record(PASS, "GNOME Shell version",
                   f"v{shell_version} (supported range 49-51)")
        else:
            record(
                WARN, "GNOME Shell version",
                f"v{shell_version} outside the 49-51 supported range.\n"
                "    Fix: re-test the generated gnome-shell.css on your version; "
                "see issue #78.",
            )
    else:
        record(WARN, "GNOME Shell version",
               "could not detect running Shell version.\n"
               "    Fix: confirm your GNOME release is in the 49-51 range (see #78).")


# --------------------------------------------------------------------------
# Check 6 (optional): generated-file drift for a given preset.
# --------------------------------------------------------------------------
def check_drift(preset_path: Path) -> None:
    try:
        data = json.loads(preset_path.read_text(encoding="utf-8"))
        palette = data["colors"]
        if not isinstance(palette, dict):
            raise ValueError("preset must contain a 'colors' object")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, ValueError) as error:
        record(FAIL, "drift (preset)", f"cannot load preset: {error}")
        return

    mismatches = []
    for template_path, output_path in theme_lib.OUTPUTS:
        try:
            source = template_path.read_text(encoding="utf-8")
            expected = theme_lib.render(source, palette)
        except (OSError, UnicodeError, ValueError) as error:
            mismatches.append(f"{output_path.relative_to(ROOT)} ({error})")
            continue
        if output_path.exists() and output_path.read_text(encoding="utf-8") != expected:
            mismatches.append(output_path.relative_to(ROOT).as_posix())
        elif not output_path.exists():
            mismatches.append(f"{output_path.relative_to(ROOT)} (missing)")

    if mismatches:
        record(FAIL, f"drift vs {preset_path.name}",
               "out of date:\n    " + "\n    ".join(mismatches) +
               "\n    Fix: re-run ./scripts/apply-theme.py <preset>.")
    else:
        record(PASS, f"drift vs {preset_path.name}", "generated files match the preset")


def print_report() -> None:
    print("Material GNOME doctor report")
    print("=" * 40)
    for status, check, detail in RESULTS:
        print(f"[{status}] {check}")
        for line in detail.splitlines():
            print(f"    {line}")
    failures = [c for s, c, _ in RESULTS if s == FAIL]
    warns = [c for s, c, _ in RESULTS if s == WARN]
    print("=" * 40)
    print(f"{len(RESULTS) - len(failures) - len(warns)} passed, "
          f"{len(warns)} warning(s), {len(failures)} failed.")
    if failures:
        print("Failed checks: " + ", ".join(failures))


def main() -> int:
    preset = None
    if "--preset" in sys.argv:
        idx = sys.argv.index("--preset")
        if idx + 1 < len(sys.argv):
            preset = Path(sys.argv[idx + 1])
            if not preset.is_absolute():
                preset = ROOT / preset

    run_check_theme()
    check_presets()
    check_placeholders()
    check_gtk4_symlink()
    check_install_and_shell()
    if preset:
        check_drift(preset)

    print_report()
    return 1 if any(s == FAIL for s, _, _ in RESULTS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
