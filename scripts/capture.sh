#!/usr/bin/env bash
# Capture actual Kitty windows on an X11 display, or under xvfb-run.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

NVIM_BIN=${NVIM_BIN:-nvim}
if [[ -z ${DISPLAY:-} ]]; then
  echo 'No X11 display. Run: xvfb-run -a bash scripts/capture.sh' >&2
  exit 1
fi
for tool in kitty xdotool import fc-match "$NVIM_BIN"; do
  if ! command -v "$tool" >/dev/null; then
    printf 'Missing command: %s\n' "$tool" >&2
    exit 1
  fi
done
if [[ $(fc-match -f '%{family}' 'JetBrains Mono') != *'JetBrains Mono'* ]]; then
  echo 'Install JetBrains Mono before capturing previews' >&2
  exit 1
fi

capture_dir=$(mktemp -d)
terminal_pid=
cleanup() {
  if [[ -n $terminal_pid ]]; then
    kill "$terminal_pid" 2>/dev/null || true
    wait "$terminal_pid" 2>/dev/null || true
  fi
  rm -f -- "$capture_dir/lua.ready" "$capture_dir/python.ready" "$capture_dir/ui.ready"
  rmdir -- "$capture_dir"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p assets
for view in lua python ui; do
  export MORELLO_VIEW="$view"
  export MORELLO_READY="$capture_dir/$view.ready"
  rows=36
  if [[ $view == python ]]; then rows=28; fi
  kitty --config scripts/capture.conf \
    --override "initial_window_height=${rows}c" --title "Morello $view" \
    "$NVIM_BIN" -u NONE -n -i NONE -c 'lua dofile("scripts/capture.lua")' &
  terminal_pid=$!
  for ((attempt = 0; attempt < 150; attempt++)); do
    if [ -f "$MORELLO_READY" ]; then break; fi
    if ! kill -0 "$terminal_pid" 2>/dev/null; then
      echo "Terminal exited before capture" >&2; exit 1
    fi
    sleep 0.1
  done
  if [[ ! -f $MORELLO_READY ]]; then
    echo 'Timed out waiting for Neovim to redraw' >&2
    exit 1
  fi
  window_id=$(xdotool search --pid "$terminal_pid" --class kitty | head -n 1)
  import -window "$window_id" "assets/neovim-$view.png"
  kill "$terminal_pid"
  wait "$terminal_pid" || true
  terminal_pid=

done
