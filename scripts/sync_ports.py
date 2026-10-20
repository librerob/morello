"""Regenerate terminal ports and Lua palettes from palette.json.

Run: python scripts/sync_ports.py
The screenshot workflow handles terminal captures separately.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
paths = {
    'palette': 'palette.json',
    'alacritty': 'ports/alacritty/alacritty.toml',
    'kitty': 'ports/kitty/kitty.conf',
    'lua': 'lua/morello/palette.lua',
}

data = json.loads((ROOT / paths['palette']).read_text(encoding='utf-8'))
P, ANSI = data['colors'], data['ansi']

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + '\n', encoding='utf-8', newline='\n')

alacritty = f'''# {data["name"]}.
# Standalone color config; also safe to import under [general].
# Keep window opacity at 1.0 to retain the audited contrast ratios.

[colors]
draw_bold_text_with_bright_colors = false

[colors.primary]
background = "{P['bg']}"
foreground = "{P['fg']}"
dim_foreground = "{P['muted']}"
bright_foreground = "{P['bright']}"

[colors.cursor]
text = "{P['bg']}"
cursor = "{P['cursor']}"

[colors.vi_mode_cursor]
text = "{P['bg']}"
cursor = "{P['keyword']}"

[colors.selection]
text = "{P['fg']}"
background = "{P['selection']}"

[colors.search.matches]
foreground = "{P['search_fg']}"
background = "{P['search_bg']}"

[colors.search.focused_match]
foreground = "{P['search_current_fg']}"
background = "{P['search_current_bg']}"

[colors.hints.start]
foreground = "{P['bg']}"
background = "{P['func']}"

[colors.hints.end]
foreground = "{P['bg']}"
background = "{P['string']}"

[colors.footer_bar]
foreground = "{P['fg']}"
background = "{P['float']}"

[colors.line_indicator]
foreground = "{P['fg']}"
background = "{P['float']}"
'''
for title, offset in [('normal',0),('bright',8)]:
    alacritty += f'\n[colors.{title}]\n'
    for i,key in enumerate(['black','red','green','yellow','blue','magenta','cyan','white']):
        alacritty += f'{key} = "{ANSI[offset+i]}"\n'
write(paths['alacritty'], alacritty)

kitty = f'''# {data["name"]}.
# Include this file from kitty.conf; no font or keybinding overrides.
# Keep background_opacity at 1.0 to retain audited contrast ratios.

background {P['bg']}
foreground {P['fg']}
cursor {P['cursor']}
cursor_text_color {P['bg']}
selection_foreground {P['fg']}
selection_background {P['selection']}

active_border_color {P['focus']}
inactive_border_color {P['border']}
bell_border_color {P['error']}

active_tab_foreground {P['bg']}
active_tab_background {P['func']}
inactive_tab_foreground {P['muted']}
inactive_tab_background {P['line']}
tab_bar_background {P['bg']}

url_color {P['string']}

# Marks are available to kittens/marking commands; they are not a search UI.
mark1_foreground {P['bg']}
mark1_background {P['func']}
mark2_foreground {P['bg']}
mark2_background {P['keyword']}
mark3_foreground {P['bg']}
mark3_background {P['constant']}

# ANSI 0-15: normal, then bright.
'''
kitty += '\n'.join(f'color{i:<2} {c}' for i,c in enumerate(ANSI))
write(paths['kitty'], kitty)

lua = [f'-- Generated from {paths["palette"]} by scripts/sync_ports.py.', 'local p = {']
lua += [f'  {k} = "{v}",' for k,v in P.items()]
lua += ['  ansi = {']
lua += [f'    [{i}] = "{c}",' for i,c in enumerate(ANSI)]
lua += ['  },','}','return p']
write(paths['lua'], '\n'.join(lua))


print('Regenerated terminal ports and Neovim palette')
