#!/usr/bin/env bash
# Capture actual Kitty windows on an X11 display, or under xvfb-run.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

NVIM_BIN=${NVIM_BIN:-nvim}
if [[ -z ${DISPLAY:-} ]]; then
  echo 'No X11 display. Run: xvfb-run -a bash scripts/capture.sh' >&2
  exit 1
fi
for tool in kitty xdotool import fc-match python3 "$NVIM_BIN"; do
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
  rm -f -- "$capture_dir/ready" "$capture_dir/preview.png"
  rmdir -- "$capture_dir"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p assets
# The preview sets background and truecolor explicitly; skip startup probes on CI.
export NVIM_NOTTYFAST=1
for variant in dark light; do
  export MORELLO_VARIANT="$variant"
  port=ports/kitty/kitty.conf
  suffix=
  if [[ $variant == light ]]; then
    port=ports/kitty/kitty-light.conf
    suffix=-light
  fi
for view in lua python typescript ui; do
  export MORELLO_VIEW="$view"
  export MORELLO_READY="$capture_dir/ready"
  rm -f -- "$MORELLO_READY"
  rows=36
  if [[ $view == python ]]; then rows=28; fi
  kitty --config scripts/capture.conf \
    --config "$port" --override "initial_window_height=${rows}c" --title "Morello $variant $view" \
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
  window_id=$(xdotool search --onlyvisible --pid "$terminal_pid" --class kitty | head -n 1)
  # Neovim can be ready before Kitty's first rendered frame reaches X11.
  # Capture into a temporary file; never replace a preview with a blank frame.
  captured=false
  for ((attempt = 0; attempt < 40; attempt++)); do
    import -window "$window_id" "$capture_dir/preview.png"
    if python3 scripts/check_capture.py "$capture_dir/preview.png" "$variant" 2>/dev/null; then
      captured=true
      break
    fi
    sleep 0.1
  done
  if [[ $captured != true ]]; then
    python3 scripts/check_capture.py "$capture_dir/preview.png" "$variant"
    exit 1
  fi
  cp -- "$capture_dir/preview.png" "assets/neovim$suffix-$view.png"
  kill "$terminal_pid"
  wait "$terminal_pid" || true
  terminal_pid=

done
done
