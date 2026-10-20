"""Check shared colors and structural validity in the extra ports."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
pdata = json.loads((ROOT / 'palette.json').read_text(encoding='utf-8'))
p, ansi = pdata['colors'], pdata['ansi']
windows = json.loads((ROOT / 'ports/windows-terminal/Morello.json').read_text(encoding='utf-8'))
assert windows['background'] == p['bg']
assert windows['foreground'] == p['fg']
slots = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white',
         'brightBlack', 'brightRed', 'brightGreen', 'brightYellow', 'brightBlue',
         'brightPurple', 'brightCyan', 'brightWhite']
assert [windows[slot] for slot in slots] == ansi
ghostty = (ROOT / 'ports/ghostty/Morello').read_text(encoding='utf-8').splitlines()
assert f'background = {p["bg"]}' in ghostty
assert [line.split('=', 2)[2] for line in ghostty if line.startswith('palette = ')] == ansi
theme = json.loads((ROOT / 'ports/vscode/themes/morello-color-theme.json').read_text(encoding='utf-8'))
package = json.loads((ROOT / 'ports/vscode/package.json').read_text(encoding='utf-8'))
assert package['version'] == pdata['version']
assert (ROOT / 'ports/vscode' / package['contributes']['themes'][0]['path']).is_file()
assert theme['colors']['editor.background'] == p['bg']
assert theme['colors']['editor.foreground'] == p['fg']
assert theme['semanticTokenColors']['function'] == p['func']
assert theme['semanticTokenColors']['string'] == p['string']
for index, color in enumerate(ansi):
    slot = ['Black','Red','Green','Yellow','Blue','Magenta','Cyan','White'][index % 8]
    key = 'terminal.ansi' + ('Bright' if index > 7 else '') + slot
    assert theme['colors'][key] == color
palette_values = set(p.values()) | set(ansi)
for key, color in theme['colors'].items():
    if key == 'editor.findMatchHighlightBackground':
        assert color == p['search_bg'] + '26'
    else:
        assert color in palette_values, f'Color outside palette: {color}'
for token in theme['tokenColors']:
    color = token['settings'].get('foreground')
    assert color is None or color in palette_values
print('Ghostty, Windows Terminal and VS Code colors agree with palette.json')
