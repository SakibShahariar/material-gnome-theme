# Layout templates

Matugen-variable counterparts to the static presets in `../layouts/`.

Each file mirrors one static layout but replaces palette colors with
`{{colors.*.default.*}}` placeholders, so the top bar follows the active
wallpaper scheme instead of a bundled preset.

The static `layouts/*.css` files are kept unchanged — they are standalone
presets for the bundled `themes/*.json` palettes.

## Usage

1. Add an entry to `~/.config/matugen/config.toml` (see
   `matugen-templates.example.toml`), pointing at the layout template you want
   and outputting to `layouts/active-layout.css`.
2. Merge the rendered layout into `gnome-shell.css` (e.g. the
   `merge-layout.sh` hook used by the Material-Gnome dotfiles pipeline).
3. Reload GNOME Shell.

To switch layouts, point `input_path` at a different file in this folder.
