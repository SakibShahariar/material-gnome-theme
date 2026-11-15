#!/usr/bin/env bash
# Switch the active GNOME Shell top-bar layout.
#
# Copies gnome-shell/layouts/<name>.css over active-layout.css, which the
# generated gnome-shell.css imports at the end. Reload the Shell afterwards.
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(cd -- "$script_dir/.." && pwd)"
layouts_dir="$root_dir/gnome-shell/layouts"
active="$layouts_dir/active-layout.css"

usage() {
  cat <<'EOF'
Usage: ./scripts/set-layout.sh <layout-name> | --list

Available layouts are the files in gnome-shell/layouts/ (excluding the
active-layout.css pointer).

  set-layout.sh unified-pill   Switch to the unified-pill layout.
  set-layout.sh --list         List available layouts.
  -h, --help                   Show this help.
EOF
}

list_layouts() {
  for path in "$layouts_dir"/*.css; do
    base="$(basename -- "$path")"
    [[ "$base" == "active-layout.css" ]] && continue
    printf '%s\n' "${base%.css}"
  done
}

if [[ ! -d "$layouts_dir" ]]; then
  printf 'Layouts directory not found: %s\n' "$layouts_dir" >&2
  exit 1
fi

if (($# == 0)); then
  usage >&2
  exit 2
fi

case "$1" in
  --list)
    list_layouts
    exit 0
    ;;
  -h|--help)
    usage
    exit 0
    ;;
esac

name="$1"
source="$layouts_dir/$name.css"

if [[ ! -f "$source" ]]; then
  {
    printf 'Unknown layout: %s\n' "$name"
    printf 'Available layouts:\n'
    list_layouts | sed 's/^/  /'
  } >&2
  exit 1
fi

cp -a -- "$source" "$active"
printf 'Active layout set to: %s\n' "$name"
printf 'Reload GNOME Shell to apply (log out/in, or Alt+F2 > r on classic).\n'
