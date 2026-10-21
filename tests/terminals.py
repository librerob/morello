"""Query the colors actually loaded by Kitty, Alacritty, Xfce and Konsole.

Run under dbus-run-session and xvfb-run on Linux. All application settings and
probe results live in a temporary directory; existing user profiles are unused.
"""
from pathlib import Path
import json
import os
import re
import select
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def probe(destination):
    import termios
    import tty
    fd = sys.stdin.fileno()
    previous = termios.tcgetattr(fd)
    received = b''
    colors = {}
    pattern = rb'\x1b\](4;\d+|10|11);rgb:([0-9a-fA-F]+)/([0-9a-fA-F]+)/([0-9a-fA-F]+)(?:\x07|\x1b\\)'
    try:
        tty.setraw(fd)
        queries = ['10', '11'] + [f'4;{index}' for index in range(16)]
        os.write(sys.stdout.fileno(), ''.join(f'\x1b]{key};?\x1b\\' for key in queries).encode())
        deadline = time.monotonic() + 8
        while len(colors) < 18 and time.monotonic() < deadline:
            if select.select([fd], [], [], 0.2)[0]:
                received += os.read(fd, 65536)
                for match in re.finditer(pattern, received):
                    key, *channels = match.groups()
                    colors[key.decode()] = '#' + ''.join(
                        f'{round(int(channel, 16) * 255 / (16 ** len(channel) - 1)):02X}'
                        for channel in channels)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, previous)
        Path(destination).write_text(json.dumps({'colors': colors, 'raw': repr(received)}))


def main():
    failures = []
    for variant in ('dark', 'light'):
        suffix = '-light' if variant == 'light' else ''
        data = json.loads((ROOT / f'palette{suffix}.json').read_text())
        expected = {'10': data['colors']['fg'], '11': data['colors']['bg']}
        expected.update({f'4;{index}': color for index, color in enumerate(data['ansi'])})
        for app in ('kitty', 'alacritty', 'xfce4-terminal', 'konsole'):
            with tempfile.TemporaryDirectory(prefix='morello-terminal-') as directory:
                home = Path(directory)
                config, share = home / '.config', home / '.local/share'
                config.mkdir()
                share.mkdir(parents=True)
                env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(config), XDG_DATA_HOME=str(share),
                           LIBGL_ALWAYS_SOFTWARE='1', QT_X11_NO_MITSHM='1')
                result = home / 'colors.json'
                child = [sys.executable, str(Path(__file__).resolve()), '--probe', str(result)]
                if app == 'kitty':
                    command = [app, '--config', str(ROOT / f'ports/kitty/kitty{suffix}.conf'), *child]
                elif app == 'alacritty':
                    command = [app, '--config-file', str(ROOT / f'ports/alacritty/alacritty{suffix}.toml'), '-e', *child]
                elif app == 'konsole':
                    target = share / 'konsole'
                    target.mkdir()
                    shutil.copyfile(ROOT / f'ports/konsole/{data["name"]}.colorscheme', target / f'{data["name"]}.colorscheme')
                    command = [app, '--separate', '--nofork', '-p', f'ColorScheme={data["name"]}', '-e', *child]
                else:
                    # Xfce's preset importer copies Scheme properties into its
                    # preferences. Exercise those same keys through terminalrc.
                    target = config / 'xfce4/terminal'
                    target.mkdir(parents=True)
                    scheme = (ROOT / f'ports/xfce-terminal/{data["name"]}.theme').read_text()
                    (target / 'terminalrc').write_text(scheme.replace('[Scheme]', '[Configuration]', 1))
                    command = [app, '--disable-server', '--execute', *child]
                try:
                    completed = subprocess.run(command, env=env, cwd=ROOT, capture_output=True, text=True, timeout=25)
                    assert result.is_file(), f'No probe result; exit {completed.returncode}: {completed.stderr}'
                    actual = json.loads(result.read_text())
                    assert actual['colors'] == expected, f'Expected {expected}, received {actual}'
                    assert completed.returncode == 0, completed.stderr
                    assert not re.search(r'(?i)(unused config key|unknown config key|invalid configuration)', completed.stderr), completed.stderr
                    print(f'{app} {variant}: foreground, background and all 16 ANSI colors passed', flush=True)
                except (AssertionError, subprocess.TimeoutExpired) as error:
                    failures.append(f'{app} {variant}: {error}')
    if failures:
        raise AssertionError('\n'.join(failures))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--probe':
        probe(sys.argv[2])
    else:
        main()
