# Compatibility and version matrix

This document records what is **supported**, what was **verified in the development environment**, what is only **reported working**, and what is merely **expected to work**. It is not a maintained multi-version CI matrix: no automated cross-version GTK or GNOME Shell test suite exists in this repository.

| Label | Meaning |
|---|---|
| Supported | The theme is designed for this component; no upper bound is imposed beyond the stated requirement. |
| Verified here | Observed locally on 2026-11-24 in the environment listed below; not a maintained test matrix. |
| Reported working | Reported by users; not independently verified by the maintainer. |
| Expected to work | Based on documented toolkit behavior; not verified in this environment. |

## Verified environment (2026-11-24)

| Component | Version | Status | Notes |
|---|---|---|---|
| GTK3 | 3.24.52 | Verified here | `gtk-3.0/gtk.css` rendered with the Material-Gnome theme in LTR and RTL; CSS validated by `scripts/check-theme.py`. |
| GTK4 / Libadwaita | 4.24.1 | Verified here | CSS custom properties (`--token`, `var(--token)`) are used by `gtk-4.0/colors.css`. |
| Matugen | 4.1.0 | Verified here | Template rendering via `matugen json` and `scripts/apply-theme.py`; see [COLORS.md](../COLORS.md). |
| GNOME Shell | 51.1 | Verified here | Panel, overview and OSD styling observed in a live session; User Themes extension active. |

## Other versions

| Component | Version / range | Status | Notes |
|---|---|---|---|
| GTK4 | 4.16 or newer | Supported | Minimum for CSS custom properties used by the palette; GTK 4.14 and older will not render the GTK4 palette correctly. |
| GTK3 | Distribution-supported GTK3 | Supported | Uses GTK3 `@define-color`; does not require GTK4 CSS variables. |
| GNOME Shell | 50.2 | Reported working | Not independently tested by the maintainer; St CSS can change between releases. |
| GNOME Shell | 48–49, or older | Expected to work | Not verified here. Check the panel, overview and OSD after upgrading. |
| Libadwaita | No enforced minimum | Expected to work | Individual apps may override or ignore third-party stylesheets. |

## Known limitations

- GTK4 older than 4.16 does not support the custom-property syntax used by this theme.
- Some applications ignore user CSS entirely; this is not a theme defect.
- Apps that draw their own canvas, such as Loupe, choose their background from the system color scheme (`org.gnome.desktop.interface color-scheme`), not from the theme stylesheet. A light backdrop in an otherwise dark setup means the system scheme is still `prefer-light`; set it to `prefer-dark` to match the dark palette.
- GNOME Shell St CSS selectors and properties change between Shell releases. A clean upgrade is not a guarantee that the panel layout or overview styling still matches.
- The Shell stylesheet does not read GTK4 `var(--...)` values at runtime. Recolor all three layers together as described in [COLORS.md](../COLORS.md).

## Post-upgrade checklist (GNOME Shell)

1. Confirm the **User Themes** extension is enabled.
2. Re-apply the desired top-bar layout (`./scripts/set-layout.sh <name>` from a checkout, or re-copy the layout CSS).
3. Regenerate colors from one palette source so GTK3, GTK4 and Shell stay in sync (`scripts/apply-theme.py` or your Matugen templates).
4. Re-run `./install.sh` (or re-copy generated files) so `~/.themes/Material-Gnome` contains the regenerated files.
5. Reload GNOME Shell (`Alt+F2`, `r` on X11). On Wayland, log out and back in if a reload is unavailable.
6. Run `python3 scripts/theme-doctor.py --preset <preset>` and visually check the panel, overview and OSD.
