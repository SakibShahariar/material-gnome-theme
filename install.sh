#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
theme_dir="${HOME}/.themes/Material-Gnome"
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/gtk-4.0"
force=0
flatpak_support=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [--force] [--flatpak]

Install Material GNOME for the current user.
  --force    Back up regular GTK4 config files before replacing them.
  --flatpak  Grant Flatpak apps read-only access to theme/config files.
  -h, --help Show this help.
EOF
}

while (($#)); do
  case "$1" in
    --force) force=1 ;;
    --flatpak) flatpak_support=1 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

for path in gtk-3.0 gtk-4.0 gnome-shell themes index.theme; do
  if [[ ! -e "$script_dir/$path" ]]; then
    printf 'Required theme path is missing: %s\n' "$path" >&2
    exit 1
  fi
done

mkdir -p "$HOME/.themes" "$theme_dir" "$config_dir"
cp -a "$script_dir/gtk-3.0" "$script_dir/gtk-4.0" \
  "$script_dir/gnome-shell" "$script_dir/themes" "$script_dir/index.theme" \
  "$theme_dir/"

link_config_file() {
  local name="$1"
  local source="$theme_dir/gtk-4.0/$name"
  local target="$config_dir/$name"

  if [[ ! -e "$source" ]]; then
    printf 'Cannot link missing source file: %s\n' "$source" >&2
    return 1
  fi

  if [[ -e "$target" && ! -L "$target" ]]; then
    if ((force == 0)); then
      printf 'Refusing to replace existing file: %s (use --force to back it up)\n' "$target" >&2
      return 1
    fi
    cp -a -- "$target" "$target.bak"
  fi

  ln -sfn -- "$source" "$target"
}

link_config_file gtk.css
link_config_file gtk-dark.css
link_config_file colors.css

if ((flatpak_support)); then
  if ! command -v flatpak >/dev/null 2>&1; then
    printf 'The --flatpak option requires the flatpak command.\n' >&2
    exit 1
  fi
  flatpak override --user --unset-env=GTK_THEME
  flatpak override --user \
    --filesystem=xdg-config/gtk-4.0:ro \
    --filesystem=xdg-config/gtk-3.0:ro \
    --filesystem=xdg-data/themes:ro \
    --filesystem="$HOME/.themes:ro"
fi

printf 'Material GNOME installed to %s\n' "$theme_dir"
printf 'GTK4 stylesheets linked in %s\n' "$config_dir"
if ((flatpak_support)); then
  printf 'Flatpak theme access enabled for the current user.\n'
fi
