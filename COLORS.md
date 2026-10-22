# Color contract

Material GNOME uses one semantic Material 3 palette as the source for GTK3, GTK4/Libadwaita, and GNOME Shell. Keep the token names aligned across generated files; do not maintain independent hand-edited palettes for each toolkit.

## Canonical inputs

There are two supported ways to provide the palette:

- **Matugen:** use the same Matugen color object for each of the three templates. The supported token shape is `colors.<token>.default.hex`; `red`, `green`, and `blue` channels are also used where an RGB value is needed.
- **Bundled JSON preset:** choose a file in `themes/` and run `python scripts/apply-theme.py themes/<preset>.json`. The script renders the same three templates without requiring Matugen. Use `--dry-run` to validate output without writing files, or `--check` to detect drift between the selected preset and generated files.

## Generated outputs

| Layer | Template | Generated output |
|---|---|---|
| GTK3 | `gtk-3.0/colors-template.css` | `gtk-3.0/colors.css` |
| GTK4 / Libadwaita | `gtk-4.0/colors-template.css` | `gtk-4.0/colors.css` |
| GNOME Shell | `gnome-shell/gnome-shell-template.css` | `gnome-shell/gnome-shell.css` |

GTK3 exposes tokens as `@define-color <token>`. GTK4 exposes the same names as CSS custom properties, for example `--primary`, `--on_primary`, and `--surface_container_high`. Keep the underscore spelling: it is part of the public token contract.

GTK4's `gtk.css` and `gtk-dark.css` import `colors.css` relatively. When linking these stylesheets into `~/.config/gtk-4.0/`, link `colors.css` there as well; otherwise the imported token definitions may be missing.

GNOME Shell's St stylesheet uses concrete color values rendered from the same palette input. It does not automatically read the GTK4 stylesheet at runtime, so changing only GTK4's `colors.css` does not recolor GNOME Shell. Regenerate all three outputs together.

## Extension integration

Extensions that consume GTK-style CSS custom properties should use the GTK4 token names above rather than inventing a parallel naming scheme. Extensions with their own Matugen templates should read the same semantic color object and use the same token meaning (for example, `primary` for the accent and `on_primary` for foreground content on that accent). GNOME Shell CSS values must be rendered into the extension/theme stylesheet; do not assume GTK4's `var(--...)` definitions are automatically available in St stylesheets.

## Validation

The CI workflow checks CSS syntax, checks that bundled preset tokens exist in `gtk-4.0/colors.css`, rejects unresolved template placeholders in generated stylesheets, and verifies that the checked-in default GTK3, GTK4, and Shell files match `themes/Material-Gnome.json`.
